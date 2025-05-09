from machine import RTC
import urequests
import ujson

# API endpoint constants
EXTERNAL_IP_ADDRESS_API = "http://api.ipify.org"
EXTERNAL_WORLD_TIME_API = "http://worldtimeapi.org/api/ip"
EXTERNAL_WORLD_TIME_ZONE_API = "http://worldtimeapi.org/api/timezone/{0}"
EXTERNAL_OPEN_TIME_API = "https://www.timeapi.io/api/Time/current/ip?ipAddress={0}"
EXTERNAL_OPEN_TIME_ZONE_API = "https://www.timeapi.io/api/Time/current/zone?timeZone={0}"

# Default values
DEFAULT_IP_ADDRESS = "00.000.000.000"
AUTO_TIMEZONE = "auto"

# Default time tuple values
DEFAULT_YEAR = 1970
DEFAULT_MONTH = 1
DEFAULT_DAY = 1
DEFAULT_WEEKDAY = 0
DEFAULT_HOUR = 0
DEFAULT_MINUTE = 0
DEFAULT_SECOND = 0
DEFAULT_SUBSECONDS = 0

# Config key constants
CONFIG_TIMEZONE_KEY = "timeZone"

# This class is used to sync the RTC with the WorldTimeAPI service
# It is also used to obtain the external IP address of the device
# in order to determine the timezone of the device
class syncRTC:

    def __init__(self, config=None):
        self._externalIPaddress = DEFAULT_IP_ADDRESS
        self.config = config
        self.timeZone = None
        if self.config:
            try:
                self.timeZone = self.config.read(CONFIG_TIMEZONE_KEY)
            except:
                self.timeZone = None

    @property
    def externalIPaddress(self):
        return self._externalIPaddress
    
    @externalIPaddress.setter
    def externalIPaddress(self, value):
        self._externalIPaddress = value
    
    def syncclock(self, rtc):
        print("Sync clock")
        returnval = True

        try:
            # Set a default date/time
            rtc.datetime((DEFAULT_YEAR, DEFAULT_MONTH, DEFAULT_DAY, 
                         DEFAULT_WEEKDAY, DEFAULT_HOUR, DEFAULT_MINUTE, 
                         DEFAULT_SECOND, DEFAULT_SUBSECONDS))
            print("RTC set to default date/time")
            
            # Always get external IP for potential use
            self.setExternalIPAddress()
            
            # Determine which API to use based on timeZone setting
            if self.timeZone and self.timeZone != AUTO_TIMEZONE:
                # Use timezone-specific API
                print(f"Using timezone from config: {self.timeZone}")
                timeAPI = EXTERNAL_OPEN_TIME_ZONE_API.format(self.timeZone)
            else:
                # Use IP-based API (auto)
                print(f"Using IP-based timezone detection: {self.externalIPaddress}")
                timeAPI = EXTERNAL_OPEN_TIME_API.format(self.externalIPaddress)
                
            # Make the API request
            r = urequests.get(timeAPI)
            z = ujson.loads(r.content)
            print(f"Time API Response: {z}")
            
            # Set the RTC datetime using response
            rtc.datetime((
                int(z["year"]),
                int(z["month"]),
                int(z["day"]),
                DEFAULT_WEEKDAY,  # Weekday (set to 0)
                int(z["hour"]),
                int(z["minute"]),
                int(z["seconds"]),
                DEFAULT_SUBSECONDS  # Subseconds set to 0
            ))
            returnval = True
            
        except Exception as e:
            print(f"Time API Exception: {e}")
            returnval = False

        return returnval

    def _iso_to_rtc_tuple(self, iso_time):
        """Convert ISO 8601 string to RTC-compatible tuple."""
        date_part, time_part = iso_time.split("T")
        year, month, day = map(int, date_part.split("-"))
        time_parts = time_part.split(":")
        hour = int(time_parts[0])
        minute = int(time_parts[1])
        second = int(time_parts[2].split(".")[0])  # ignore milliseconds

        # Weekday is set to 0 (can be calculated if needed)
        return (year, month, day, DEFAULT_WEEKDAY, hour, minute, second, DEFAULT_SUBSECONDS)

    def setExternalIPAddress(self):
        returnval = True
        try:
            ipaddress = urequests.get(EXTERNAL_IP_ADDRESS_API)
            self.externalIPaddress = ipaddress.content.decode("utf-8")
        except Exception as e:
            print("Exception: {}".format(e))
            returnval = False
        finally:
            returnval

    def refresh_timezone(self):
        """Reload the timeZone from the config file."""
        if self.config:
            try:
                self.timeZone = self.config.read(CONFIG_TIMEZONE_KEY)
            except:
                self.timeZone = None
