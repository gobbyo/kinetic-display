from common.config import Config
import urequests
import ujson
import time
import gc

# API endpoint constants
externalOpenMeteoAPI = const("https://api.open-meteo.com/v1/forecast?latitude={0}&longitude={1}&current=temperature_2m,relative_humidity_2m")

class extTempHumid:
    """
    This class is responsible for obtaining outdoor temperature and humidity data 
    using geolocation based on the device's IP address.
    """

    def __init__(self, syncrtc):
        """
        Initialize with a syncRTC instance to access the device's external IP address.
        
        Args:
            syncrtc: An instance of syncRTC that provides the external IP address
        """
        self._sync = syncrtc
        self.config = Config("config.json")
        
    def _make_api_request(self, url):
        """
        Helper method to make API requests with proper error handling
        
        Args:
            url: The URL to request
            
        Returns:
            dict: Parsed JSON response or None if request fails
        """
        response = None
        try:
            response = urequests.get(url)
            if response.status_code == 200:
                data = ujson.loads(response.content)
                return data
            else:
                print(f"API request failed with status code: {response.status_code}")
                return None
        except Exception as e:
            print(f"API request error: {e}")
            return None
        finally:
            if response:
                response.close()
        

    def updateOutdoorTemp(self):
        """
        Update the outdoor temperature and humidity using the Open-Meteo API.
        Location coordinates are read from the configuration file.
        
        Returns:
            tuple: (temperature, humidity) if successful, (None, None) if failed
        """
        gc.collect()  # Free memory before making API request
        try:
            lat = self.config.read("latitude")
            lon = self.config.read("longitude")
            
            # Check if coordinates are available
            if not lat or not lon:
                print("Error: Location coordinates not available. Try calling setLatLon() first.")
                return None, None
            
            print(f"Free memory before request: {gc.mem_free()} bytes")
            weather_data = self._make_api_request(externalOpenMeteoAPI.format(lat, lon))
            if not weather_data:
                return None, None
                
            # Extract temperature and humidity from current conditions
            if 'current' in weather_data:
                if 'temperature_2m' in weather_data['current']:
                    temperature = int(weather_data['current']['temperature_2m'])
                    self.config.write("tempoutdoor", temperature)
                else:
                    print("Error: Temperature data not available in API response")
                    return None, None
                    
                if 'relative_humidity_2m' in weather_data['current']:
                    humidity = int(weather_data['current']['relative_humidity_2m'])
                    self.config.write("humidoutdoor", humidity)
                    print(f"Weather updated: {temperature}°C, {humidity}% humidity")
                    return temperature, humidity
                else:
                    print("Error: Humidity data not available in API response")
                    return None, None
            else:
                print("Error: Current weather data not available in API response")
                return None, None
                
        except Exception as e:
            print(f"Error updating weather data: {e}")
            return None, None
        finally:
            gc.collect()  # Free memory after request
            
        return None, None