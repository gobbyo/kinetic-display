# Filename: picowifi.py
# Author: Jeff Beman
# Date: summer 2024

import usocket as socket        #importing socket
import socket
import network            #importing network
import gc
import uio
import time
import config
import machine
import secrets

# The purpose of this class is to bootstrap the PICO W connectivity to the user's wifi network.
# This class renders administrative web pages to allow the user to set various settings for the main display controller:
# the wifi ssid and password, the time format, the wake and sleep times, the temperature format, and the temperature and humidity
# This class also renders web pages to allow the user to modify the extend and retract angles for each digit controller.
# Note the static ip address is necessary to allow the user to connect to the PICO W when it is in access point mode
class hotspot:
    def __init__(self,ssid,password):
        self.url = '192.168.4.1'  #static ip address
        self.hotspotssid = ssid                  #Set access point name
        self.hotspotpassword = password      #Set your access point password
        self.adminwebpage = 'admin.html'
        self.completedsettings = 'completedsettings.html'
        self.channel = 11
        self.waittime = 10
        self.ssid = ssid
        self.pwd = password

    def __del__(self):
        print("__del__()")
        time.sleep(1)
        machine.reset() #reset to avoid OSError: [Errno 98] EADDRINUSE
    
    # This method writes the wifi ssid and password to the secrets.py file
    # This file is used by the main display controller to connect to the user's wifi network
    def _writeSecrets(self,ssid,pwd):
        print("_secrets()")
        with uio.open('secrets.py', 'w') as f:
            f.write("usr='{0}'\r\npwd='{1}'".format(ssid,pwd))
            f.flush()
            f.close()

    # This method renders the admin web page to the main display controller
    # The admin web page allows the user to set the wifi ssid and password, 
    # the time format, the wake and sleep times, the temperature format, 
    # and the temperature and humidity
    def _admin_page(self):
        page = ''
        conf = config.Config("config.json")
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

    # This method reads the stored web pages into memory
    def _completed_page(self):
        page = ''
        with uio.open(self.completedsettings, 'r') as f:
            while True:
                line = f.readline()
                if not line:
                    break
                page += line
            f.close()
        return page
    
    # This method parses the request from the web page and returns the page to be rendered
    def _requestPage(self,request):
        returnPage = 'admin'
        print('_requestPage() {0}'.format(request))
        if request.find('admin') > 0:
            returnPage = 'admin'
        if request.find('wifisettings') > 0:
            returnPage = 'wifisettings'
        
        return returnPage

    # This method parses the form input values from the web page when the user submits the form
    def parseAdminSettings(self,request):
        print("parseAdminSettings()")
        conf = config.Config("")
        #titles=['ssid','pwd','tempCF','time','wait','speed']
        request = request.replace('GET /wifisettings/','')
        request = request.replace(' HTTP/1.1','')
        lines = request.split('&')
        for i in lines:
            t = i.split('=')
            if t[1].find('?') > 0:
                t[1] = t[1].split('?')[0]
            if t[0] == 'ssid':
                print('ssid={0}'.format(t[1]))
                self.ssid = t[1]
            if t[0] == 'pwd':
                print('pwd={0}'.format(t[1]))
                self.pwd = t[1]
            if t[0] == 'tempCF':
                print('tempCF={0}'.format(t[1][0]))
                conf.write('tempCF',t[1][0])
            if t[0] == 'time':
                print('time={0}'.format(t[1]))
                conf.write('time',int(t[1]))
            if t[0] == 'wait':
                print('wait={0}'.format(t[1]))
                conf.write('wait',int(t[1]))
            if t[0] == 'speed':
                print('speed={0}'.format(t[1]))
                conf.write('speed',int(t[1]))
        self._writeSecrets(self.ssid,self.pwd)
    
    # This method sends the reply back to the user's web browser
    def sendreply(self,conn, pagebuffer):
        print("sendreply(conn={0})".format(conn))
        response_headers = {
            'Content-Type': 'text/html; encoding=utf8',
            'Content-Length': len(pagebuffer)
        }
        response_headers_raw = ''.join('%s: %s\n' % (k, v) for k, v in \
                                                response_headers.items())

        # Reply as HTTP/1.1 server, saying "HTTP OK" (code 200).
        response_proto = 'HTTP/1.1'.encode()
        response_status = '200'.encode()
        response_status_text = 'OK'.encode() # this can be random

        conn.send(b'%s %s %s' % (response_proto, response_status,
                                                        response_status_text))
        conn.send(response_headers_raw.encode())
        conn.send(b'\n') # to separate headers from body
        conn.send(pagebuffer.encode())

    # This method connects the PICO W to the user's wifi network
    def connectWifi(self):
        wifi = network.WLAN(network.STA_IF)
        wifi.active(True)
        # set power mode to get WiFi power-saving off (if needed)
        wifi.config(pm = 0xa11140)
        print('self.ssid={0},self.pwd={1}'.format(self.ssid,self.pwd))
        wifi.connect(self.ssid,self.pwd)
        print('wifi.isconnected({0})'.format(wifi.isconnected()))

        max_wait = self.waittime
        while max_wait > 0:
            if wifi.isconnected():
                #STAT_IDLE – no connection and no activity,
                #STAT_CONNECTING – connecting in progress,
                #STAT_WRONG_PASSWORD – failed due to incorrect password,
                #STAT_NO_AP_FOUND – failed because no access point replied,
                #STAT_CONNECT_FAIL – failed due to other problems,
                #STAT_GOT_IP – connection successful
                print('wifi.status() = {0}'.format(wifi.status()))
                self.url = wifi.ifconfig()[0]
                return True
            max_wait -= 1
            print('waiting for connection...')
            time.sleep(1)
        return False
    
    def disconnectWifi(self):
        wifi = network.WLAN(network.STA_IF)
        wifi.disconnect()
        wifi.active(False)

    # This method starts the hotspot and renders the admin web page
    # The admin web page allows the user to set the wifi ssid and password,
    # the time format, the wake and sleep times, the temperature format,
    # and the temperature and humidity. Note the display doesn't work until
    # the user sets the wifi ssid and password
    #def connectAdmin(self, display):
    def connectAdmin(self):
        print('display hotspot is starting')
        evalResponse = True
        gc.collect()

        # open soft wifi api mode
        wifi = network.WLAN(network.AP_IF)
        wifi.config(ssid=self.hotspotssid,key=self.hotspotpassword,channel=self.channel,pm = 0xa11140)
        wifi.ifconfig([self.url, '255.255.255.0', self.url, '0.0.0.0'])

        i = self.waittime
        while (wifi.active() == False) and (i > 0):
            wifi.active(True)
            time.sleep(2)
            i -= 1
            print("Waiting for WiFi AP to be active, attempt {0}".format(i))
            pass

        print('display hotspot is active')
        print(wifi.ifconfig())
        self.url = wifi.ifconfig()[0]

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

        wifi.disconnect()
        wifi.active(False)

def connectToLocalWifi(connectAdmin):
    try:
        ssid = input("ssid: ")
        pwd = input("password: ")
        wifi = hotspot(ssid,pwd)
        
        if connectAdmin:
            wifi.connectAdmin()
        
        if wifi.connectWifi():
            print('Connected to wifi')
        else:
            print('Failed to connect to wifi')
            del wifi
    except Exception as e:
        print("Exception: {}".format(e))

if __name__ == '__main__':
    connectToLocalWifi(True)