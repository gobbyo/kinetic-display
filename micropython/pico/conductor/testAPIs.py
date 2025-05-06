from picowifiserver import PicoWifi
import syncRTC
import externalTemp
import secrets
from common.config import Config
from machine import RTC
import time

ssid = input("Enter WiFi SSID: ")
password = input("Enter WiFi Password: ")
secrets.usr = ssid
secrets.pwd = password

try:
    picowifi = PicoWifi("config.json",ssid, password)
    if(picowifi.connect_to_wifi_network()):
        rtc = RTC()
        rtc.datetime((1970, 1, 1, 0, 0, 0, 0, 0)) # Set RTC to epoch time
        sync = syncRTC.syncRTC()

        print("\n*******API Test 1*********")
        prev_ip = sync.externalIPaddress
        sync.setExternalIPAddress()
        ext_ip = sync.externalIPaddress
        if ext_ip != prev_ip:
            print(f"Success. Obtained new external IP address from {syncRTC.externalIPAddressAPI}")
            print(f"External IP address: {ext_ip}")
            print("**************************")
        else:
            print(f"Failed. No external IP address obtained from {syncRTC.externalIPAddressAPI}")
            print("**************************")
        time.sleep(1)
        
        print("\n*******API Test 2*********")
        prev_dt = rtc.datetime()
        
        # Test 2: Test syncclock() with main API endpoint
        rtc.datetime((1970, 1, 1, 0, 0, 0, 0, 0)) # Set RTC to epoch time
        sync.syncclock(rtc)
        dt = rtc.datetime()
        if dt[0] != 1970:
            print(f"Success. RTC synced with external time API {syncRTC.externalWorldTimeAPI} or {syncRTC.externalOpenTimeAPI}")
            print(f"DateTime. \n\tyear: {dt[0]}\n\tmonth: {dt[1]}\n\tday: {dt[2]}\n\tweekday: {dt[3]}\n\thours: {dt[4]}\n\tminutes: {dt[5]}\n\tseconds: {dt[6]}")
            print("**************************")         
        else:
            print(f"Failed. Could not obtain external time from {syncRTC.externalWorldTimeAPI} or {syncRTC.externalOpenTimeAPI}")
            print("**************************")
        
        # Test 3: Test with specific timezone name - America/Los_Angeles
        print("\n*******API Test 3*********")
        rtc.datetime((1970, 1, 1, 0, 0, 0, 0, 0)) # Reset RTC to epoch time
        timezone_to_test = "America/Los_Angeles"
        if sync.syncclockWithTimeZone(rtc, timezone_to_test):
            dt = rtc.datetime()
            if dt[0] != 1970:
                print(f"Success. RTC synced with TimeAPI.io using timezone {timezone_to_test}")
                print(f"DateTime ({timezone_to_test}). \n\tyear: {dt[0]}\n\tmonth: {dt[1]}\n\tday: {dt[2]}\n\tweekday: {dt[3]}\n\thours: {dt[4]}\n\tminutes: {dt[5]}\n\tseconds: {dt[6]}")
                print("**************************")
            else:
                print(f"Failed. Could not sync time using TimeAPI.io with timezone {timezone_to_test}")
                print("**************************")
        else:
            print(f"Failed. Could not connect to TimeAPI.io with timezone {timezone_to_test}")
            print("**************************")
        
        # Test 4: Test with another timezone - Europe/London
        print("\n*******API Test 4*********")
        rtc.datetime((1970, 1, 1, 0, 0, 0, 0, 0)) # Reset RTC to epoch time
        timezone_to_test = "Europe/London"
        if sync.syncclockWithTimeZone(rtc, timezone_to_test):
            dt = rtc.datetime()
            if dt[0] != 1970:
                print(f"Success. RTC synced with TimeAPI.io using timezone {timezone_to_test}")
                print(f"DateTime ({timezone_to_test}). \n\tyear: {dt[0]}\n\tmonth: {dt[1]}\n\tday: {dt[2]}\n\tweekday: {dt[3]}\n\thours: {dt[4]}\n\tminutes: {dt[5]}\n\tseconds: {dt[6]}")
                print("**************************")
            else:
                print(f"Failed. Could not sync time using TimeAPI.io with timezone {timezone_to_test}")
                print("**************************")
        else:
            print(f"Failed. Could not connect to TimeAPI.io with timezone {timezone_to_test}")
            print("**************************")
            
        # Test 5: Test saving timezone setting to config
        print("\n*******API Test 5*********")
        test_timezone = "Asia/Tokyo"
        conf = Config("config.json")
        conf.write("timeZone", test_timezone)
        new_sync = syncRTC.syncRTC("config.json")
        
        if new_sync.timeZone == test_timezone:
            print(f"Success. Timezone {test_timezone} was saved to config and loaded successfully")
            print("**************************")
        else:
            print(f"Failed. Timezone {test_timezone} was not properly stored or retrieved")
            print(f"Retrieved value: {new_sync.timeZone}")
            print("**************************")
        
        print("\n*******API Test 6*********")
        tempHumid = externalTemp.extTempHumid(sync)
        #initialize config file with lat and lon
        conf = Config("config.json")
        conf.write("lat",0)
        conf.write("lon",0)
        tempHumid.setLatLon()
        lat = conf.read("lat")
        lon = conf.read("lon")
        if lat != 0 and lon != 0:
            print(f"Success. Obtained latitude and longitude from {externalTemp.externalLatLonAPI}")
            print(f"Latitude: {lat}\nLongitude: {lon}")
            print("**************************")
        else:
            print(f"Failed. Could not obtain latitude and longitude from {externalTemp.externalLatLonAPI}")
            print("**************************")
        
        print("\n*******API Test 7*********")
        conf.write("tempoutdoor",0)
        conf.write("humidoutdoor",0)
        tempHumid.updateOutdoorTemp()
        tempoutdoor = conf.read("tempoutdoor")
        humidoutdoor = conf.read("humidoutdoor")
        if tempoutdoor != 0 and humidoutdoor != 0:
            print(f"Success. Obtained outdoor temperature and humidity from {externalTemp.externalOpenMeteoAPI}")
            print(f"Outdoor temperature: {tempoutdoor} C\nOutdoor humidity: {humidoutdoor} %")
            print("**************************")
        else:
            print(f"Failed. Could not obtain outdoor temperature and humidity from {externalTemp.externalOpenMeteoAPI}")
            print("**************************")
except Exception as e:
    print(f"An error occurred: {e}")
finally:
    picowifi.disconnect_from_wifi_network()