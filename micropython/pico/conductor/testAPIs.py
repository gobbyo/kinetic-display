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
            print(f"Test 1: Success. Obtained new external IP address from {syncRTC.externalIPAddressAPI}")
            print(f"External IP address: {ext_ip}")
            print("**************************")
        else:
            print(f"Test 1: Failed. No external IP address obtained from {syncRTC.externalIPAddressAPI}")
            print("**************************")
        time.sleep(1)

        print("\n*******API Test 2*********")
        prev_dt = rtc.datetime()
        sync.syncclock(rtc)
        dt = rtc.datetime()
        if dt[0] != prev_dt[0]:
            print(f"Test 2: Success. RTC synced with external time API {syncRTC.externalWorldTimeAPI} or {syncRTC.externalOpenTimeAPI}")
            print(f"DateTime. \n\tyear: {dt[0]}\n\tmonth: {dt[1]}\n\tday: {dt[2]}\n\tweekday: {dt[3]}\n\thours: {dt[4]}\n\tminutes: {dt[5]}\n\tseconds: {dt[6]}")
            print("**************************")         
        else:
            print(f"Test 2: Failed. Could not obtain external time from {syncRTC.externalWorldTimeAPI} or {syncRTC.externalOpenTimeAPI}")
            print("**************************")
        
        print("\n*******API Test 3*********")
        tempHumid = externalTemp.extTempHumid(sync)
        #initialize config file with lat and lon
        conf = Config("config.json")
        conf.write("lat",0)
        conf.write("lon",0)
        tempHumid.setLatLon()
        lat = conf.read("lat")
        lon = conf.read("lon")
        if lat != 0 and lon != 0:
            print(f"Test 3: Success. Obtained latitude and longitude from {externalTemp.externalLatLonAPI}")
            print(f"Latitude: {lat}\nLongitude: {lon}")
            print("**************************")
        else:
            print(f"Test 3: Failed. Could not obtain latitude and longitude from {externalTemp.externalLatLonAPI}")
            print("**************************")
        
        print("\n*******API Test 4*********")
        conf.write("tempoutdoor",0)
        conf.write("humidoutdoor",0)
        tempHumid.updateOutdoorTemp()
        tempoutdoor = conf.read("tempoutdoor")
        humidoutdoor = conf.read("humidoutdoor")
        if tempoutdoor != 0 and humidoutdoor != 0:
            print(f"Test 4: Success. Obtained outdoor temperature and humidity from {externalTemp.externalOpenMeteoAPI}")
            print(f"Outdoor temperature: {tempoutdoor} C\nOutdoor humidity: {humidoutdoor} %")
            print("**************************")
        else:
            print(f"Test 4: Failed. Could not obtain outdoor temperature and humidity from {externalTemp.externalOpenMeteoAPI}")
            print("**************************")
except Exception as e:
    print(f"An error occurred: {e}")
finally:
    picowifi.disconnect_from_wifi_network()