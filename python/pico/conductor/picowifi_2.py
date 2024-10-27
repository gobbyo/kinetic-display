import uasyncio
import usocket as socket
import uio
import ujson
import network
import time
import gc
from micropython import const
import secrets

AP_SSID = const('PicoW-AP')
AP_PASSWORD = const('picopassword')
AP_CHANNEL = const(1)
AP_URL = const('192.168.4.1')
AP_WAIT_TIME = const(30)

class TimeoutError(Exception):
    pass

class ConfigManager:
    def __init__(self, filename='wifi_config.json'):
        self.hotspotssid = AP_SSID
        self.hotspotpassword = AP_PASSWORD
        self.channel = AP_CHANNEL
        self.url = AP_URL
        self.waittime = AP_WAIT_TIME
        self.filename = filename
        self.config = self.load_config()

    def load_config(self):
        try:
            with open(self.filename, 'r') as f:
                return ujson.load(f)
        except:
            return {'ssid': '', 'password': ''}

    def save_config(self):
        with open(self.filename, 'w') as f:
            ujson.dump(self.config, f)

    def update_config(self, ssid, password):
        self.config['ssid'] = ssid
        self.config['password'] = password
        self.save_config()

class Hotspot:
    def __init__(self, config):
        """
        Initialize the Hotspot class with configuration settings.
        
        Args:
            config: Configuration object containing hotspot settings.
        """
        self.url = '192.168.4.1'  # Static IP address
        self.hotspotssid = config.hotspotssid  # Set access point name
        self.hotspotpassword = config.hotspotpassword  # Set access point password
        self.adminwebpage = 'admin.html'
        self.completedsettings = 'completedsettings.html'
        self.channel = config.channel
        self.waittime = config.waittime
        self.ssid = config.hotspotssid
        self.pwd = config.hotspotpassword
        #self.wifi = network.WLAN(network.STA_IF)
        self.wifi = network.WLAN(network.AP_IF)

    # This method connects the PICO W to the user's wifi network
    def setup_admin(self):
        gc.collect()
        # open soft wifi api mode
        self.wifi.config(ssid=self.hotspotssid,key=self.hotspotpassword,channel=self.channel,pm = 0xa11140)
        self.wifi.ifconfig([self.url, '255.255.255.0', self.url, '0.0.0.0'])
        
        i = self.waittime
        while (self.wifi.active() == False) and (i > 0):
            self.wifi.active(True)
            time.sleep(2)
            i += 1
            print("Waiting for WiFi AP to be active, attempt {0}".format(i))
            pass
            
        if i > 0:
            return True
        else:
            return False
        
    async def connectAdmin(self):
        """
        Connect to the admin interface and start the server.
        """
        try:
            # open soft wifi api mode
            if self.setup_admin():
                await self.start_server()
                await self.serve_forever()
        except Exception as e:
            print(f"Error in connectAdmin: {e}")
        finally:
            await self.cleanup()

    async def start_server(self):
        """
        Start the web server.
        """
        # Placeholder for server start logic
        print("Server started.")
                # Create an Event Loop
        loop = uasyncio.get_event_loop()
        # Create a task to run the main function
        loop.create_task(self.serve_forever())
        # Run the event loop indefinitely
        loop.run_forever()

    async def serve_forever(self):
        """
        Serve requests indefinitely.
        """
        # Placeholder for serving logic
        print("Serving requests indefinitely.")

        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)   #creating socket object
        s.bind((self.url, 80))
        s.listen(5)
        while evalResponse:
            conn, addr = s.accept()
            print('Got a connection from %s' % str(addr))
            request = conn.recv(1024).decode('utf-8')
            print('connection request received = %s' % str(request))
            returnPage = self._requestPage(request)
            if returnPage == 'wifisettings':
                print("update to wifisettings detected!")
                self.parseAdminSettings(request)
                pagebuffer = self._completed_page()
                self.sendreply(conn,pagebuffer)
                time.sleep(2)
                conn.close()
                evalResponse = False
            if returnPage == 'admin':
                print("admin page requested")
                pagebuffer = self._admin_page()
                self.sendreply(conn,pagebuffer)

        self.wifi.disconnect()
        self.wifi.active(False)

    async def cleanup(self):
        """
        Clean up resources.
        """
        try:
            self.wifi.active(False)
            print("WiFi deactivated and resources cleaned up.")
        except Exception as e:
            print(f"Error in cleanup: {e}")

    # This method renders the admin web page to the main display controller
    # The admin web page allows the user to set the wifi ssid and password, 
    # the time format, the wake and sleep times, the temperature format, 
    # and the temperature and humidity
    async def _admin_page(self):
        page = ''
        conf = ConfigManager("config.json")
        tempCF = conf.read("tempCF")
        tempWait = conf.read("wait")
        tempSpeed = conf.read("speed")
        tempTime = conf.read("time")
        findCF = '<option value="{0}">'.format(tempCF)
        findTime = '<option value="{0}">'.format(tempTime)
        findWait = 'id="wait" value="20"'
        findSpeed = 'id="speed" value="50"'
        with uio.open(self.adminwebpage, 'r') as f:
            while True:
                line = f.readline()
                if not line:
                    break
                if line.find('ssid') > 0:
                    print('Found ssid={0}'.format(secrets.usr))
                    line = line.replace('8eb5c1217eaf',secrets.usr)
                if line.find('pwd') > 0:
                    print('Found pwd={0}'.format(secrets.pwd))
                    line = line.replace('fd3b61afb36d', secrets.pwd)
                if line.find(findCF) > 0:
                    print('findCF={0}'.format(findCF))
                    line = line.replace(findCF, '<option value="{0}" selected>'.format(tempCF))
                if line.find(findWait) > 0:
                    print('findWait={0}'.format(findWait))
                    line = line.replace(findWait, 'id="wait" value="{0}"'.format(tempWait))
                if line.find(findSpeed) > 0:
                    print('findSpeed={0}'.format(findSpeed))
                    line = line.replace(findSpeed, 'id="speed" value="{0}"'.format(tempSpeed))
                if line.find(findTime) > 0:
                    print('findTime={0}'.format(findTime))
                    line = line.replace(findTime, '<option value="{0}" selected>'.format(tempTime))
                page += line
            f.close()
        return page
    
def main():
    config_manager = ConfigManager()
    hotspot = Hotspot(config_manager)
    uasyncio.run(hotspot.connectAdmin())

if __name__ == '__main__':
    main()
