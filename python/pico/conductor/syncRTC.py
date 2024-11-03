from machine import RTC
import urequests
import json

externalIPAddressAPI=const("http://api.ipify.org")

# This class is used to sync the RTC with the timeapi.io service
# It is also used to obtain the external IP address of the device
# in order to determine the timezone of the device
class syncRTC:

    def __init__(self):
        self.externalIPaddress = "00.000.000.000"

    def syncclock(self, rtc):
        print("Sync clock")
        returnval = True

        try:
            self.setExternalIPAddress()
            timeAPI = "https://www.timeapi.io/api/Time/current/ip?ipAddress={0}".format(self.externalIPaddress)
            r = urequests.get(timeAPI)
            z = json.loads(r.content)
            timeAPI = "https://www.timeapi.io/api/TimeZone/zone?timeZone={0}".format(z["timeZone"])
            print(timeAPI)
            rq = urequests.get(timeAPI)
            j = json.loads(rq.content)
            t = (j["currentLocalTime"].split('T'))[1].split(':')
            print(t)
            #[year, month, day, weekday, hours, minutes, seconds, subseconds]
            rtc.datetime((int(z["year"]), int(z["month"]), int(z["day"]), 0, int(t[0]), int(t[1]), int(z["seconds"]), 0))
        except Exception as e:
            print("Exception: {}".format(e))
            returnval = False
        finally:
            return returnval

    def __del__(self):
        urequests.Response.close()

    def setExternalIPAddress(self):
        try:
            print("Obtaining external IP Address")
            ipaddress = urequests.get(externalIPAddressAPI)
            self.externalIPaddress = ipaddress.content.decode("utf-8")
            print("Obtained external IP Address: {0}".format(self.externalIPaddress))
        except Exception as e:
            print("Exception: {}".format(e))
        finally:
            pass

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