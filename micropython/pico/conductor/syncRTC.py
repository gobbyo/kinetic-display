from machine import RTC
import urequests
import ujson

externalIPAddressAPI = "http://api.ipify.org"
externalWorldTimeAPI = "http://worldtimeapi.org/api/ip"
externalWorldTimeZoneAPI = "http://worldtimeapi.org/api/timezone/{0}"
externalOpenTimeAPI = "https://www.timeapi.io/api/Time/current/ip?ipAddress={0}"
externalOpenTimeZoneAPI = "https://www.timeapi.io/api/Time/current/zone?timeZone={0}"

# This class is used to sync the RTC with the WorldTimeAPI service
# It is also used to obtain the external IP address of the device
# in order to determine the timezone of the device
class syncRTC:

    def __init__(self, config=None):
        self.externalIPaddress = "00.000.000.000"
        self.config = config
        self.timeZone = None
        if self.config:
            try:
                self.timeZone = self.config.read("timeZone")
            except:
                self.timeZone = None

    def syncclock(self, rtc):
        print("Sync clock")
        returnval = True

        try:
            # Set a default date/time
            rtc.datetime((1970, 1, 1, 0, 0, 0, 0, 0))
            print("RTC set to default date/time")
            
            # Always get external IP for potential use
            self.setExternalIPAddress()
            
            # Determine which API to use based on timeZone setting
            if self.timeZone and self.timeZone != "auto":
                # Use timezone-specific API
                print(f"Using timezone from config: {self.timeZone}")
                timeAPI = externalOpenTimeZoneAPI.format(self.timeZone)
            else:
                # Use IP-based API (auto)
                print(f"Using IP-based timezone detection: {self.externalIPaddress}")
                timeAPI = externalOpenTimeAPI.format(self.externalIPaddress)
                
            # Make the API request
            r = urequests.get(timeAPI)
            z = ujson.loads(r.content)
            print(f"Time API Response: {z}")
            
            # Set the RTC datetime using response
            rtc.datetime((
                int(z["year"]),
                int(z["month"]),
                int(z["day"]),
                0,  # Weekday (set to 0)
                int(z["hour"]),
                int(z["minute"]),
                int(z["seconds"]),
                0  # Subseconds set to 0
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
        return (year, month, day, 0, hour, minute, second, 0)

    def setExternalIPAddress(self):
        returnval = True
        try:
            ipaddress = urequests.get(externalIPAddressAPI)
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
                self.timeZone = self.config.read("timeZone")
            except:
                self.timeZone = None

# Example usage:
def main():
    rtc = RTC()
    rtc2 = RTC()
    
    # Example with config (normally you would import the Config class)
    class MockConfig:
        def read(self, key):
            if key == "timeZone":
                return "America/Los_Angeles"  # Replace with your desired timezone
            return None
    
    # Uncomment to test with timezone from config
    # clock = syncRTC(MockConfig())
    
    # Or use without config to default to IP-based detection
    clock = syncRTC()
    
    clock.syncclock(rtc)
    print(rtc.datetime())
    print(rtc2.datetime())
    rtc2.datetime((2023, 1, 1, 0, 0, 0, 0, 0))
    print(rtc.datetime())
    print(rtc2.datetime())

if __name__ == "__main__":
    main()