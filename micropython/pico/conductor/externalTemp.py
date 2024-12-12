from common.config import Config
import urequests
import ujson
import time

class extTempHumid:
    # This class is used to obtain the outdoor temperature and humidity using the OpenWeatherMap API.

    def __init__(self, syncrtc):
        self._sync = syncrtc
    # This method is used to obtain the latitude and longitude of the device's external IP address.
    # The latitude and longitude are then written to the configuration file and used to obtain the
    # outdoor temperature and humidity.
    def setLatLon(self):
        try:
            conf = Config("config.json")
            print("external ip address = {0}".format(self._sync.externalIPaddress))
            g = urequests.get("http://ip-api.com/json/{0}".format(self._sync.externalIPaddress))
            geo = ujson.loads(g.content)
            conf.write("lat",geo['lat'])
            conf.write("lon",geo['lon'])
            print("lat = {0}".format(geo['lat']))
            print("lon = {0}".format(geo['lon']))
        except Exception as e:
            print("Exception: {}".format(e))
        finally:
            time.sleep(1)
    
    # This method is used to set the outdoor temperature and humidity. It first turns on a "connected" (green) LED,
    # then obtains the latitude and longitude of the device's external IP address. It then uses the latitude and
    # longitude to obtain the outdoor temperature and humidity. Finally, it turns off the "connected" LED.
    # The outdoor temperature and humidity are then written to the configuration file.
    def updateOutdoorTemp(self):
        print("kineticDisplay.updateOutdoorTemp()")
        try:
            conf = Config("config.json")
            lat = conf.read("lat")
            lon = conf.read("lon")
            print(f"lat={lat}, lon={lon}")
            r = urequests.get("https://api.open-meteo.com/v1/forecast?latitude={0}&longitude={1}&current_weather=true&hourly=relativehumidity_2m".format(lat,lon))
            j = ujson.loads(r.content)
            temperature = j['current_weather']['temperature']
            print(f"temp={temperature}")
            temp = int(temperature)
            conf.write("tempoutdoor",temp)
            print("temp sensor outdoor = {0}".format(temp))
            humidity = j['hourly']['relativehumidity_2m'][0]
            humid = int(humidity)
            conf.write("humidoutdoor",humid)
            print("humidity sensor outdoor = {0}".format(humid))
        except Exception as e:
            print("Exception: {}".format(e))
        finally:
            time.sleep(1)