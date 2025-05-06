from machine import RTC
import urequests
import ujson
import time
from common.config import Config

# list of all time zones found at https://www.zeitverschiebung.net/en/all-time-zones.html
externalIPAddressAPI = const("http://api.ipify.org")
externalWorldTimeAPI = const("http://worldtimeapi.org/api/ip")
externalOpenTimeAPI = const("https://www.timeapi.io/api/Time/current/ip?ipAddress={0}")
externalTimeZoneAPI = const("https://www.timeapi.io/api/time/current/zone?timeZone={0}")

# Maximum retry attempts for API calls
MAX_RETRIES = 3
# Base delay for exponential backoff (in seconds)
BASE_DELAY = 1

# This class is used to sync the RTC with the WorldTimeAPI service
# It is also used to obtain the external IP address of the device
# in order to determine the timezone of the device
class syncRTC:

    def __init__(self):
        self.externalIPaddress = "00.000.000.000"
        self.config = Config("config.json")

    def _create_datetime_tuple(self, response_json, is_iso_format=False):
        """
        Create a datetime tuple from API response JSON
        
        Args:
            response_json (dict): The parsed JSON response from a time API
            is_iso_format (bool): Whether the datetime is in ISO format (WorldTimeAPI)
            
        Returns:
            tuple: A datetime tuple compatible with RTC.datetime()
        """
        try:
            if is_iso_format:
                # Handle ISO format from WorldTimeAPI
                iso_time = response_json["datetime"]
                return self._iso_to_rtc_tuple(iso_time)
            else:
                # Handle direct values from TimeAPI.io
                return (
                    int(response_json["year"]),
                    int(response_json["month"]),
                    int(response_json["day"]),
                    0,  # Weekday (set to 0, can be calculated if needed)
                    int(response_json["hour"]),
                    int(response_json["minute"]),
                    int(response_json["seconds"]),  # Note: "seconds" key in TimeAPI.io response
                    0  # Subseconds set to 0
                )
        except Exception as e:
            print(f"Error creating datetime tuple: {e}")
            raise

    def _make_api_request(self, api_url):
        """
        Make a request to a time API with retry logic and return the parsed JSON response
        
        Args:
            api_url (str): The URL of the API to request
            
        Returns:
            dict: The parsed JSON response
            
        Raises:
            Exception: If all retry attempts fail
        """
        print(f"Trying API: {api_url}")
        
        retry_count = 0
        last_exception = None
        
        while retry_count < MAX_RETRIES:
            try:
                # Close any previous connections that might be lingering
                if retry_count > 0:
                    try:
                        # Attempt a garbage collection to help clear resources
                        import gc
                        gc.collect()
                        print(f"Retry attempt {retry_count}/{MAX_RETRIES}")
                    except:
                        pass
                
                # Make the request with a timeout
                response = urequests.get(api_url, timeout=10)
                
                try:
                    # Parse the JSON response
                    json_data = ujson.loads(response.content)
                    print(f"API Response: {json_data}")
                    
                    # Clean up the response
                    response.close()
                    
                    return json_data
                except Exception as e:
                    print(f"Error parsing JSON from {api_url}: {e}")
                    response.close()
                    raise
                    
            except OSError as e:
                # Handle network errors specifically
                print(f"Network error with {api_url}: [{e.__class__.__name__}] {e}")
                last_exception = e
                # Exponential backoff with jitter
                delay = (BASE_DELAY * (2 ** retry_count)) + ((BASE_DELAY * retry_count) % 1)
                print(f"Retrying in {delay} seconds...")
                time.sleep(delay)
                
            except Exception as e:
                # Handle other exceptions
                print(f"Error connecting to {api_url}: {e}")
                last_exception = e
                delay = (BASE_DELAY * (2 ** retry_count))
                print(f"Retrying in {delay} seconds...")
                time.sleep(delay)
                
            retry_count += 1
            
        # If we've exhausted all retries, raise the last exception
        print(f"All {MAX_RETRIES} retry attempts failed for {api_url}")
        raise last_exception or Exception(f"Failed to connect to {api_url} after {MAX_RETRIES} retries")

    def _detect_and_save_timezone(self, response_json, api_url):
        """
        Detect and save timezone from API response if auto-detection is enabled
        
        Args:
            response_json (dict): The parsed JSON response
            api_url (str): The API URL that was used (to determine the format)
            
        Returns:
            None
        """
        # Only save if we're in auto-detection mode (empty timezone config)
        if self.config.read("timeZone", default="") != "":
            return
            
        if api_url.startswith("https://www.timeapi.io"):
            if "timeZone" in response_json:
                detected_timezone = response_json["timeZone"]
                print(f"Detected time zone from TimeAPI.io: {detected_timezone}")
                self.config.write("timeZone", detected_timezone)
        else:
            # Assume WorldTimeAPI format
            if "timezone" in response_json:
                detected_timezone = response_json["timezone"]
                print(f"Detected time zone from WorldTimeAPI: {detected_timezone}")
                self.config.write("timeZone", detected_timezone)

    def syncclock(self, rtc):
        """
        Synchronize the RTC with one of several time APIs
        
        Args:
            rtc (machine.RTC): The RTC object to synchronize
            
        Returns:
            bool: True if successful, False otherwise
        """
        print("Sync clock")
        try:
            self.setExternalIPAddress()
        except Exception as e:
            print(f"Failed to get external IP, will try time APIs without it: {e}")
        
        # Get user's selected time zone from config
        user_timezone = self.config.read("timeZone", default="")
        use_ip_detection = user_timezone == ""
        
        if use_ip_detection:
            print("No time zone configured. Will attempt to detect based on IP address.")
        else:
            print(f"Using configured time zone: {user_timezone}")

        # Store all API attempts to avoid redundant calls if one fails
        api_attempts = {}

        # Strategy 1: Direct timezone API if a timezone is configured
        if not use_ip_detection:
            try:
                api_url = externalTimeZoneAPI.format(user_timezone)
                api_attempts[api_url] = True
                json_data = self._make_api_request(api_url)
                dt = self._create_datetime_tuple(json_data)
                rtc.datetime(dt)
                print(f"Clock synchronized using timezone API with {user_timezone}")
                return True
            except Exception as e:
                print(f"Time zone API failed: {e}")

        # Strategy 2: IP-based APIs (either as primary if no timezone is set, or as fallback)
        apis = [
            externalWorldTimeAPI
        ]
        
        # Add the IP-based TimeAPI only if we have a valid IP
        if self.externalIPaddress and self.externalIPaddress != "00.000.000.000":
            apis.append(externalOpenTimeAPI.format(self.externalIPaddress))

        for api in apis:
            # Skip APIs we've already tried
            if api in api_attempts:
                continue
                
            api_attempts[api] = True
            
            try:
                json_data = self._make_api_request(api)
                
                # Handle different response formats
                is_iso_format = not api.startswith("https://www.timeapi.io")
                dt = self._create_datetime_tuple(json_data, is_iso_format)
                
                # Save detected timezone if in auto-detection mode
                self._detect_and_save_timezone(json_data, api)
                
                # Set the RTC datetime
                rtc.datetime(dt)
                print(f"Clock synchronized using {api}")
                return True
            except Exception as e:
                print(f"Exception with API {api}: {e}")

        # Strategy 3: Try with a fallback timezone format as last resort
        if not use_ip_detection:
            try:
                fallback_timezone = self.get_fallback_timezone_format(user_timezone)
                api_url = externalTimeZoneAPI.format(fallback_timezone)
                
                # Skip if we've already tried this API
                if api_url in api_attempts:
                    raise Exception(f"Already attempted API {api_url}")
                    
                api_attempts[api_url] = True
                
                json_data = self._make_api_request(api_url)
                dt = self._create_datetime_tuple(json_data)
                rtc.datetime(dt)
                print(f"Clock synchronized using fallback timezone format")
                return True
            except Exception as e:
                print(f"Fallback time zone API attempt failed: {e}")
                
        # If all methods fail
        print("All time synchronization methods failed")
        return False

    def get_fallback_timezone_format(self, timezone_str):
        """
        Try to convert a timezone string to a different format that might be accepted by the API
        
        Args:
            timezone_str (str): The timezone string to convert
            
        Returns:
            str: A potentially more compatible timezone format
        """
        # Simple conversion of common formats - expand as needed
        if '/' in timezone_str:
            parts = timezone_str.split('/')
            if len(parts) == 2:
                return f"Etc/GMT"  # Very basic fallback
        return timezone_str

    def _iso_to_rtc_tuple(self, iso_time):
        """
        Convert ISO 8601 string to RTC-compatible tuple
        
        Args:
            iso_time (str): The ISO 8601 formatted time string
            
        Returns:
            tuple: A datetime tuple compatible with RTC.datetime()
        """
        date_part, time_part = iso_time.split("T")
        year, month, day = map(int, date_part.split("-"))
        time_parts = time_part.split(":")
        hour = int(time_parts[0])
        minute = int(time_parts[1])
        second = int(time_parts[2].split(".")[0])  # ignore milliseconds

        # Weekday is set to 0 (can be calculated if needed)
        return (year, month, day, 0, hour, minute, second, 0)

    def setExternalIPAddress(self):
        """
        Get the external IP address of the device with retry logic
        
        Returns:
            bool: True if successful, False otherwise
        """
        retry_count = 0
        
        while retry_count < MAX_RETRIES:
            try:
                ipaddress = urequests.get(externalIPAddressAPI, timeout=5)
                self.externalIPaddress = ipaddress.content.decode("utf-8")
                ipaddress.close()
                return True
            except Exception as e:
                print(f"Exception getting external IP (attempt {retry_count+1}/{MAX_RETRIES}): {e}")
                retry_count += 1
                if retry_count < MAX_RETRIES:
                    # Exponential backoff
                    delay = BASE_DELAY * (2 ** retry_count)
                    time.sleep(delay)
                
        print("Failed to get external IP address after all retry attempts")
        return False
