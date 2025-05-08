import network
import time
from common.config import Config
from common.uart_protocol import uartCommand, commandHelper
import machine
import secrets
import ujson
import gc
import os
from microdot import Microdot, send_file, Request

class PicoWifi:
    def __init__(self, configfilename, ssid='kinetic-display', password='12oclock'):
        self.app = None
        self.ip_address = ""
        self.config = Config(configfilename)
        self.uart = None
        # AP_IF=Access Point interface of the network module. 
        # Used when you want your Pico W to act as a Wi-Fi access point, 
        # allowing other devices to connect to it.
        self.wifi = network.WLAN(network.AP_IF)
        self.waittime = 20
        self.ssid = ssid
        self.password = password
        Request.max_content_length = 1024 * 1024  # 1MB (change as needed)

    def __del__(self):
        print("__del__()")
        self.wifi.disconnect()
        time.sleep(1)
        machine.reset() #reset to avoid OSError: [Errno 98] EADDRINUSE

    def load_schedules(self, directory='schedules'):
        schedules = []
        for filename in os.listdir(directory):
            if filename.endswith('.json'):
                path = f'{directory}/{filename}'
                try:
                    with open(path, 'r') as file:
                        s = ujson.load(file)
                        title = s.get("title", filename)
                        schedules.append((title, filename))
                except (OSError, ValueError) as e:
                    print(f"Error loading schedule {filename}: {e}")
        return schedules
    
    def start_wifi(self):
        """
        Start the WiFi access point with the given SSID and password.
        """
        try:
            self.wifi.config(ssid=self.ssid, password=self.password)
            self.wifi.active(True)
            i = 10
            while not self.wifi.active() and i > 0:
                time.sleep(2)
                i -= 1
                print("Waiting for WiFi AP to be active")

            if self.wifi.active():
                self.ip_address = self.wifi.ifconfig()[0]
                print(f'Display wifi is active, IP={self.ip_address}')
            else:
                print("Failed to activate WiFi AP")
        except Exception as e:
            print(f"Exception occurred while starting WiFi: {e}")
            self.ip_address = ""
    
    def shutdownWifi(self):
        gc.collect()
        print("Shutting down pico WiFi AP")
        if self.wifi.isconnected():
            self.wifi.disconnect()
            print("Disconnected from WiFi")
        else:
            print("WiFi was not connected")
    
    # This method connects the PICO W to the user's wifi network
    def connect_to_wifi_network(self):
        gc.collect()
        print("Connecting to WiFi")
        # STA_IF=Station mode, the PICO W acts as a client that connects to an existing WiFi network, 
        # similar to how your phone or laptop connects to a WiFi router.
        self.wifi = network.WLAN(network.STA_IF)
        self.wifi.active(True)
        # set power mode to turn off WiFi power-saving (if needed)
        self.wifi.config(pm=0xa11140)
        
        self.wifi.connect(secrets.usr, secrets.pwd)
        max_wait = self.waittime
        while max_wait > 0:
            if self.wifi.isconnected():
                self.url = self.wifi.ifconfig()[0]
                print(f'Connected to WiFi, IP address: {self.url}')
                return True
            elif self.wifi.status() == network.STAT_WRONG_PASSWORD:
                print("Failed to connect to WiFi: Wrong password (network.STAT_WRONG_PASSWORD)")
            elif self.wifi.status() == network.STAT_NO_AP_FOUND:
                print("Failed to connect to WiFi: No access point found (network.STAT_NO_AP_FOUND)")
            elif self.wifi.status() == network.STAT_CONNECT_FAIL:
                print("Failed to connect to WiFi: Connection failed (network.STAT_CONNECT_FAIL)")
            elif self.wifi.status() == network.STAT_CONNECTING:
                print("Connecting to WiFi network (network.STAT_CONNECTING)")
            elif self.wifi.status() == network.STAT_GOT_IP:
                print(f'Connected to WiFi network (network.STAT_GOT_IP), IP address: {self.url}')
                self.url = self.wifi.ifconfig()[0]
                return True
            else:
                print(f'unknown wifi status = {self.wifi.status()}')

            max_wait -= 1
            print('Waiting for connection...')
            time.sleep(2)

        print("Failed to connect to WiFi: Timeout")
        return False
    
    def disconnect_from_wifi_network(self):
        gc.collect()
        print("Disconnecting from user's WiFi")
        self.wifi = network.WLAN(network.STA_IF)
        if self.wifi.isconnected():
            self.wifi.disconnect()
            print("Disconnected from WiFi")
        else:
            print("WiFi is not connected")

    def writeSecrets(self, ssid, pwd):
        try:
            with open('secrets.py', 'w') as f:
                print("Writing secrets to file")
                f.write(f"usr='{ssid}'\r\npwd='{pwd}'")
                f.flush()
                f.close()
        except OSError as e:
            print(f"Error writing secrets: {e}")

    def createIndex(self):
        # Collect configuration values once to avoid repeated calls
        config_tempCF = self.config.read("tempCF")
        config_time = self.config.read("time")
        config_wait = self.config.read("wait")
        config_speed = self.config.read("speed")
        config_timezone = self.config.read("timeZone", default="Europe/London")
        selected_schedule = self.config.read("schedule", default="")
        test_on_startup = self.config.read("testOnStartup")
        digit_type = self.config.read("digitType", default="Earth")  # Get digitType from config
        
        # Pre-calculate search strings to avoid string interpolation in the loop
        findCF = f'<option value="{config_tempCF}">'
        findTime = f'<option value="{config_time}">'
        findTimezone = f'<option value="{config_timezone}">'  # New search string for timezone
        
        # Load schedule data
        try:
            schedules = self.load_schedules()
        except Exception as e:
            print(f"Error loading schedules: {e}")
            schedules = []
            
        # Run garbage collection before processing large files
        gc.collect()
        
        try:
            with open("html/admin.html", 'r') as input_file, open("html/index.html", 'w') as output_file:
                for line in input_file:
                    # Process line by line with minimal string operations
                    modified = False
                    
                    if not modified and 'ssid' in line:
                        line = line.replace('ce9c7e1bb79e', secrets.usr)
                        modified = True
                        
                    if not modified and 'pwd' in line:
                        line = line.replace('ea83bcd634fa', secrets.pwd)
                        modified = True
                        
                    if not modified and findCF in line:
                        line = line.replace(findCF, f'<option value="{config_tempCF}" selected>')
                        modified = True
                    
                    # Fix timezone selection - replace this:
                    # if not modified and 'id="timeZone"' in line:
                    #    line = line.replace('id="timeZone"', f'id="timeZone" value="{config_timezone}"')
                    #    modified = True
                    
                    # With this:
                    if not modified and findTimezone in line:
                        line = line.replace(findTimezone, f'<option value="{config_timezone}" selected>')
                        modified = True
                        
                    if not modified and 'id="wait"' in line:
                        line = line.replace('id="wait"', f'id="wait" name="wait" value="{config_wait}"')
                        modified = True
                        
                    if not modified and 'id="speed"' in line:
                        line = line.replace('id="speed"', f'id="speed" name="speed" value="{config_speed}"')
                        modified = True
                        
                    if not modified and findTime in line:
                        line = line.replace(findTime, f'<option value="{config_time}" selected>')
                        modified = True
                    
                    if not modified and '<option value="true">Test</option>' in line:
                        # If test_on_startup is True, select the "Test" option
                        if test_on_startup is True or test_on_startup == "true":
                            line = line.replace('<option value="true">', '<option value="true" selected>')
                        modified = True
                    
                    if not modified and '<option value="false">No Test</option>' in line:
                        # If test_on_startup is False or None, select the "No Test" option
                        if test_on_startup is False or test_on_startup == "false" or test_on_startup is None:
                            line = line.replace('<option value="false">', '<option value="false" selected>')
                        modified = True
                    
                    # Handle digitType dropdown
                    if not modified and f'<option value="{digit_type}">' in line:
                        line = line.replace(f'<option value="{digit_type}">', f'<option value="{digit_type}" selected>')
                        modified = True
                    
                    # Fix the schedule dropdown alignment issue by modifying the line instead of
                    # writing directly to the output stream
                    if not modified and '<select name="schedule" id="schedule">' in line:
                        # Create schedule options while preserving the HTML structure
                        options_html = ''
                        for title, filename in schedules:
                            selected = 'selected' if filename == selected_schedule else ''
                            options_html += f'<option value="{filename}" data-id="{title}" {selected}>{title}</option>'
                        
                        # Replace only the inner content of the select element, preserving the surrounding HTML
                        line = line.replace('<select name="schedule" id="schedule">', 
                                          f'<select name="schedule" id="schedule">{options_html}')
                        modified = True
                    
                    # Write the processed line directly to the output file
                    output_file.write(line)
                
                # Force memory cleanup before finishing
                gc.collect()
                
            return True
        except OSError as e:
            print(f"Error processing HTML files: {e}")
            # Run garbage collection after error to free memory
            gc.collect()
            return False

    def run_server(self):
        self.app = Microdot()

        @self.app.route('/')
        async def index(request):
            print("returning index page")
            self.createIndex()
            return send_file('html/index.html')

        @self.app.get('/uploadfile')
        async def file(request):
            print("returning upload file page")
            return send_file('html/file.html')

        @self.app.post('/controllersettings')
        async def controllersettings(request):
            print('Received controller settings')
            form = request.body.decode('utf-8')
            print(f'Body: {form}')
            f = ujson.loads(form)
            self.writeSecrets(f['ssid'], f['pwd'])
            self.config.write('time', f['time'])
            self.config.write('tempCF', f['tempCF'])
            self.config.write('timeZone', f['timeZone'])
            self.config.write('wait', f['wait'])
            self.config.write('speed', f['speed'])
            self.config.write('schedule', f['schedule'])
            self.config.write('testOnStartup', "true" if f['testOnStartup'] else "false")
            self.config.write('digitType', f['digitType'])  # Save the digitType setting
            
            return ''

        @self.app.post('/upload')
        async def upload(request):
            print("uploading file")
            try:
                # obtain the filename and size from request headers
                filename = request.headers['Content-Disposition'].split('filename=')[1].strip('"')
                size = int(request.headers['Content-Length'])

                # sanitize the filename
                filename = filename.replace('/', '_')
                print(f"uploading {filename}")

                # write the file to the files directory in 1K chunks
                path = f'schedules/{filename}'
                with open(path, 'wb') as f:
                    while size > 0:
                        print(f'Remaining size: {size}')
                        chunk = await request.stream.read(min(size, 1024))
                        f.write(chunk)
                        size -= len(chunk)
                    f.flush()
                    f.close()

                print(f'Successfully saved {filename}')
                return ''
            except Exception as e:
                print(f"Error uploading file: {e}")
                return 'Error uploading file', 500

        @self.app.delete('/delete/<filename>')
        async def deleteSchedule(self, filename):
            try:
                path = f'schedules/{filename}'
                os.remove(path)
                print(f"Successfully deleted {filename}")
            except OSError as e:
                print(f"Error deleting {filename}: {e}")

        @self.app.get('/bye')
        async def bye(request):
            print('returning completed settings page')
            return send_file('html/completedsettings.html')

        @self.app.get('/shutdown')
        async def shutdown(request):
            print('shutting down microdot web service')
            request.app.shutdown()
            return 'Shutting down', 200

        self.app.run(host=self.ip_address, port=80)
    
    def shutdown_server(self):
        print("Web server shutdown")
        if self.app:
            self.app.shutdown()
        time.sleep(1)
        del self.app

# Example usage
if __name__ == "__main__":
    try:
        picowifi = PicoWifi("config.json")
        picowifi.start_wifi()
        if picowifi.ip_address != "":
            picowifi.run_server()
        picowifi.shutdown_server()
        picowifi.shutdownWifi()
    finally:
        print('deleted picowifi instance')
        time.sleep(1)

    try:
        picowifi = PicoWifi("config.json", secrets.usr, secrets.pwd)
        if(picowifi.connect_to_wifi_network()):
            time.sleep(2)
            picowifi.disconnect_from_wifi_network()
    finally:
        print('deleted picowifi instance')
        time.sleep(1)