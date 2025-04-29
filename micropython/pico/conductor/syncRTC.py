from machine import RTC
import urequests
import ujson

externalIPAddressAPI = const("http://api.ipify.org")
externalWorldTimeAPI = const("http://worldtimeapi.org/api/ip")
externalOpenTimeAPI = const("https://www.timeapi.io/api/Time/current/ip?ipAddress={0}")

# This class is used to sync the RTC with the WorldTimeAPI service
# It is also used to obtain the external IP address of the device
# in order to determine the timezone of the device
class syncRTC:

    def __init__(self):
        self.externalIPaddress = "00.000.000.000"

    def syncclock(self, rtc):
        print("Sync clock")
        returnval = True

        # Try WorldTimeAPI first
        try:
            self.setExternalIPAddress()
            r = urequests.get(externalWorldTimeAPI)
            z = ujson.loads(r.content)
            print(f"WorldTimeAPI Response: {z}")

            # Parse the datetime string from WorldTimeAPI
            iso_time = z["datetime"]  # Example: "2025-04-28T20:44:06.487506+00:00"
            dt = self._iso_to_rtc_tuple(iso_time)

            # Set the RTC datetime
            rtc.datetime(dt)
        except Exception as e:
            print(f"WorldTimeAPI Exception: {e}")
            returnval = False

        # If WorldTimeAPI fails, try OpenTimeAPI
        if not returnval:
            try:
                timeAPI = externalOpenTimeAPI.format(self.externalIPaddress)
                r = urequests.get(timeAPI)
                z = ujson.loads(r.content)
                print(f"OpenTimeAPI Response: {z}")

                # Set the RTC datetime using OpenTimeAPI response
                rtc.datetime((
                    int(z["year"]),
                    int(z["month"]),
                    int(z["day"]),
                    0,  # Weekday (set to 0, can be calculated if needed)
                    int(z["hour"]),
                    int(z["minute"]),
                    int(z["seconds"]),
                    0  # Subseconds set to 0
                ))
                returnval = True
            except Exception as e:
                print(f"OpenTimeAPI Exception: {e}")
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

#Example usage:
def main():
    rtc = RTC()
    rtc2 = RTC()
    clock = syncRTC()
    clock.syncclock(rtc)
    print(rtc.datetime())
    print(rtc2.datetime())
    rtc2.datetime((2023, 1, 1, 0, 0, 0, 0, 0))
    print(rtc.datetime())
    print(rtc2.datetime())

if __name__ == "__main__":
    main()