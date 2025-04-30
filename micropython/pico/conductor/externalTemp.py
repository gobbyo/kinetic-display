from common.config import Config
import urequests
import ujson
import time

externalLatLonAPI = const("http://ip-api.com/json/{0}")
externalOpenMeteoAPI = const("https://api.open-meteo.com/v1/forecast?latitude={0}&longitude={1}&current_weather=true&hourly=relativehumidity_2m")
# This class is used to obtain the outdoor temperature and humidity using the OpenWeatherMap API.

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
            #g = urequests.get("http://ip-api.com/json/{0}".format(self._sync.externalIPaddress))
            g = urequests.get(externalLatLonAPI.format(self._sync.externalIPaddress))
            geo = ujson.loads(g.content)
            conf.write("lat",geo['lat'])
            conf.write("lon",geo['lon'])
        except Exception as e:
            print("Exception: {}".format(e))
        finally:
            time.sleep(1)
    
    # This method is used to set the outdoor temperature and humidity. It first turns on a "connected" (green) LED,
    # then obtains the latitude and longitude of the device's external IP address. It then uses the latitude and
    # longitude to obtain the outdoor temperature and humidity. Finally, it turns off the "connected" LED.
    # The outdoor temperature and humidity are then written to the configuration file.
    def updateOutdoorTemp(self):
        try:
            conf = Config("config.json")
            lat = conf.read("lat")
            lon = conf.read("lon")
            #r = urequests.get("https://api.open-meteo.com/v1/forecast?latitude={0}&longitude={1}&current_weather=true&hourly=relativehumidity_2m".format(lat,lon))
            r = urequests.get(externalOpenMeteoAPI.format(lat,lon))
            j = ujson.loads(r.content)
            temperature = j['current_weather']['temperature']
            temp = int(temperature)
            conf.write("tempoutdoor",temp)
            current_hour = j['current_weather']['time'].split(':')[0]
            current_hour_index = 0
            for item in j['hourly']['time']:
                if item.find(current_hour) != -1:
                    break
                current_hour_index += 1
            humidity = j['hourly']['relativehumidity_2m'][current_hour_index] # last value in the list
            humid = int(humidity)
            conf.write("humidoutdoor",humid)
        except Exception as e:
            print("Exception: {}".format(e))
        finally:
            time.sleep(1)