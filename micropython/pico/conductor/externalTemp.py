from common.config import Config
import urequests
import ujson
import time

# API endpoint constants
externalLatLonAPI = const("http://ip-api.com/json/{0}")
externalOpenMeteoAPI = const("https://api.open-meteo.com/v1/forecast?latitude={0}&longitude={1}&current_weather=true&hourly=relativehumidity_2m")
# Backup API if the primary one fails
externalBackupLatLonAPI = const("https://ipapi.co/{0}/json/")

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
        try:
            response = urequests.get(url)
            if response.status_code == 200:
                return ujson.loads(response.content)
            else:
                print(f"API request failed with status code: {response.status_code}")
                return None
        except Exception as e:
            print(f"API request error: {e}")
            return None
        
    def setLatLon(self):
        """
        Obtain the latitude and longitude based on the device's external IP address.
        The coordinates are then saved to the configuration file for future use.
        
        Returns:
            tuple: (latitude, longitude) if successful, (None, None) if failed
        """
        if not self._sync or not hasattr(self._sync, 'externalIPaddress'):
            print("Error: syncRTC instance not properly initialized or missing IP address")
            return None, None
            
        # Try primary geolocation API
        try:
            geo = self._make_api_request(externalLatLonAPI.format(self._sync.externalIPaddress))
            if geo and 'lat' in geo and 'lon' in geo:
                self.config.write("lat", geo['lat'])
                self.config.write("lon", geo['lon'])
                print(f"Location set to: {geo['lat']}, {geo['lon']}")
                return geo['lat'], geo['lon']
        except Exception as e:
            print(f"Primary geolocation API error: {e}")
            
        # Try backup geolocation API
        try:
            time.sleep(1)  # Add delay before trying backup API
            geo = self._make_api_request(externalBackupLatLonAPI.format(self._sync.externalIPaddress))
            if geo and 'latitude' in geo and 'longitude' in geo:
                self.config.write("lat", geo['latitude'])
                self.config.write("lon", geo['longitude'])
                print(f"Location set to: {geo['latitude']}, {geo['longitude']} (from backup API)")
                return geo['latitude'], geo['longitude']
        except Exception as e:
            print(f"Backup geolocation API error: {e}")
            
        print("Failed to obtain location coordinates")
        return None, None
    
    def updateOutdoorTemp(self):
        """
        Update the outdoor temperature and humidity using the Open-Meteo API.
        Location coordinates are read from the configuration file.
        
        Returns:
            tuple: (temperature, humidity) if successful, (None, None) if failed
        """
        try:
            lat = self.config.read("lat")
            lon = self.config.read("lon")
            
            # Check if coordinates are available
            if not lat or not lon:
                print("Error: Location coordinates not available. Try calling setLatLon() first.")
                return None, None
                
            weather_data = self._make_api_request(externalOpenMeteoAPI.format(lat, lon))
            if not weather_data:
                return None, None
                
            # Extract temperature
            if 'current_weather' in weather_data and 'temperature' in weather_data['current_weather']:
                temperature = int(weather_data['current_weather']['temperature'])
                self.config.write("tempoutdoor", temperature)
            else:
                print("Error: Temperature data not available in API response")
                return None, None
                
            # Extract humidity for the current hour
            if 'hourly' in weather_data and 'relativehumidity_2m' in weather_data['hourly']:
                # Find the index for the current hour
                current_hour = weather_data['current_weather']['time'].split('T')[1].split(':')[0]
                current_date = weather_data['current_weather']['time'].split('T')[0]
                current_datetime = f"{current_date}T{current_hour}:00"
                
                try:
                    hour_index = weather_data['hourly']['time'].index(current_datetime)
                    humidity = int(weather_data['hourly']['relativehumidity_2m'][hour_index])
                    self.config.write("humidoutdoor", humidity)
                    print(f"Weather updated: {temperature}°C, {humidity}% humidity")
                    return temperature, humidity
                except (ValueError, IndexError) as e:
                    print(f"Error finding current hour in API response: {e}")
                    # Fall back to first hour in the forecast
                    humidity = int(weather_data['hourly']['relativehumidity_2m'][0])
                    self.config.write("humidoutdoor", humidity)
                    return temperature, humidity
            else:
                print("Error: Humidity data not available in API response")
                
        except Exception as e:
            print(f"Error updating weather data: {e}")
            
        return None, None