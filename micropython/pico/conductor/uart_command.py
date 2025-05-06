from common.uart_protocol import uartProtocol, uartChannel, uartCommand, commandHelper, uartActions
import dht
from machine import Pin, RTC
import photoresistor
from time_formatter import formatHour
from picowifiserver import PicoWifi
from syncRTC import syncRTC
from externalTemp import extTempHumid
from scheduler import scheduleInfo, eventActions
import digit_colons
from common.config import Config
import secrets
import gc
import time
import ujson
import uio

photoresistorPin = 28
dhtPin = 27
dhtPowerpin = 16
hybernateswitchPin = 18
powerRelayPin = 19

# This class is the conductor of the display. It manages the various components of the system
# and orchestrates the display of the time, date, temperature, and humidity. It also manages the
# hybernation of the system and the schedule of events.
class Conductor:
    def __init__(self):
        self.wifi = None
        self.wifihotspot = None
        self.uart0 = uartProtocol(uartChannel.uart0, commandHelper.baudRate[3])
        time.sleep(.75)
        self.uart1 = uartProtocol(uartChannel.uart1, commandHelper.baudRate[3])
        self.light = photoresistor.photoresistor(photoresistorPin)
        self.dht = dht.DHT22(Pin(dhtPin))
        self.dhtpower = Pin(dhtPowerpin, Pin.OUT)
        self.display12hour = True
        self.temp = 0
        self.humidity = 0
        self.rtc = RTC()
        self.syncRTC = syncRTC()
        self.hybernateswitch = Pin(hybernateswitchPin, Pin.IN, Pin.PULL_DOWN)
        self.powerRelay = Pin(powerRelayPin, Pin.OUT)
        self.schedule = []
        self.brightness = 0
        self.colons = digit_colons.DigitColons(digit_colons.led_pins, digit_colons.DigitColons.brightness, digit_colons.motor_pins)

    def checkForScheduledAction(self, s):
        #[year, month, day, weekday, hours, minutes, seconds, subseconds]
        dt = self.rtc.datetime()
                
        if s.event == eventActions.hybernate:
            if (dt[4] == s.hour or s.hour == -1) and (dt[5] == s.minute or s.minute == -1):
                print(f"h={s.hour}, m={s.minute}, s={s.second}, e={s.event}")
                return eventActions.hybernate
    
        if s.event < eventActions.hybernate:
            if (s.hour == -1 and dt[5] == (s.minute)) or (s.hour == -1 and s.minute == -1):
                if dt[6] >= s.second and dt[6] < (s.second + s.elapse):
                    print(f"h={s.hour}, m={s.minute}, s={s.second}, e={s.event}")
                    return s.event
        
        return 0
    
    def scheduledHybernation(self,s):
        print("scheduledHybernation")
        cleared = False
        hybernating = True
        try:
            dt = self.rtc.datetime()
            m = s.elapse + (dt[4] * 60) + dt[5]
            deadlineinHours = int(m/60) % 24 #hours
            deadlineinMinutes = int(m%60)
            print(f"deadline {deadlineinHours}:{deadlineinMinutes}")
            while hybernating:
                dt = self.rtc.datetime()
                if deadlineinHours == dt[4] and deadlineinMinutes == dt[5]:
                    hybernating = False
                if self.hybernateswitch():
                    hybernating = False
                #Clear the display
                if not cleared:
                    print("hybernating...")
                    self.clearDisplay() 
                    time.sleep(2)
                    self.wifi.disconnect_from_wifi_network()
                    self.powerRelay.on()
                    cleared = True
                time.sleep(1)
        except Exception as e:
            print(f"Error scheduledHybernation: {e}")
        finally:
            self.powerRelay.off()
            self.wifi = PicoWifi(secrets.usr,secrets.pwd)
            self.wifi.connect_to_wifi_network()
            self.syncRTC.syncclock(self.rtc)
        pass

    def checkHybernate(self):
        cleared = False
        hybernated = False
        try:
            while self.hybernateswitch():
                #Clear the display
                if not cleared:
                    self.clearDisplay()
                    print("hybernating...")
                    time.sleep(2)
                    self.wifi.disconnect_from_wifi_network()
                    self.powerRelay.on()
                    cleared = True
                    hybernated = True
                time.sleep(1)
        except Exception as e:
            print(f"Error hybernateswitch: {e}")
        finally:
            self.powerRelay.off()
            if hybernated:
                self.wifi = PicoWifi(secrets.usr,secrets.pwd)
                self.wifi.connect_to_wifi_network()
                self.syncRTC.syncclock(self.rtc)
        return hybernated

    def updateIndoorTemp(self):
        self.dhtpower.on()
        time.sleep(1.5)
        self.temp = 0
        self.humidity = 0
        try:
            self.dht.measure()
            self.temp = self.dht.temperature()
            self.humidity = self.dht.humidity()
        except Exception as e:
            print(f"Error updateIndoorTemp: {e}")
        finally:
            time.sleep(.25)
            self.dhtpower.off()

    def updateOutdoorTempHumid(self):
        try:
            etc = extTempHumid(self.syncRTC)
            etc.updateOutdoorTemp()
        except Exception as e:
            print(f"Error conductor updateOutdoorTempHumid: {e}")
        finally:
            pass

    def updateBrightness(self):
        curlight = self.light.read()
        if curlight == self.brightness:
            return
        print(f"Light level: {curlight}")
        # Set the brightness of the digits
        for d in range(3,-1,-1):
            cmd = None
            if d < 2:
                if d == 1:
                    self.colons.brightness = curlight/10
                cmd = uartCommand('{0}{1}{2:02}'.format(d, uartActions.brightness, curlight))
                self.uart0.sendCommand(cmd)
            else:
                cmd = uartCommand('{0}{1}{2:02}'.format(d, uartActions.brightness, curlight))
                self.uart1.sendCommand(cmd)
            print(f"sending brightness command to digit {d} = {cmd.cmdStr}")
            time.sleep(.1)
        self.brightness = curlight

    def clearDisplay(self):
        # Set the brightness of the digits
        try:
            for d in range(3,-1,-1):
                cmd = None
                if d < 2:
                    if d == 1:
                        self.colons.retractSegment(0)
                        self.colons.retractSegment(1)
                    cmd = uartCommand('{0}015'.format(d))
                    self.uart0.sendCommand(cmd)
                    print(f"clear display: cmd={cmd.cmdStr}")
                    time.sleep(.1)
                else:
                    cmd = uartCommand(f'{d}015')
                    self.uart1.sendCommand(cmd)
                    print(f"clear display: cmd={cmd.cmdStr}")
                    time.sleep(.1)
        except Exception as e:
            print(f"Error cleardisplay: {e}")
        finally:
            pass

    def testDigits(self):
        # Initialize/test each digit
        for d in range(3,-1,-1):
            cmd = None
            if d < 2:
                if d == 1:
                    time.sleep(.2)
                    self.colons.dance()
                cmd = uartCommand('{0}{1}{2:02}'.format(d, uartActions.dance, 0))
                self.uart0.sendCommand(cmd)
            else:
                cmd = uartCommand('{0}{1}{2:02}'.format(d, uartActions.dance, 0))
                self.uart1.sendCommand(cmd)
            print(f"sending dance command: cmd={cmd.cmdStr}")
            time.sleep(2)
            
            if cmd is not None:
                print(f"received reply: cmd={cmd.cmdStr}")
            
            time.sleep(.5)

    def showIndoorTemp(self, celcius):
        try:
            print("showIndoorTemp")
            self.updateIndoorTemp()
            t = '{0:02}'.format(self.temp)
            if not celcius:
                t = '{0:02}'.format(int(round((9/5)*self.temp+32,0)))
                print(f"Temp in Fahrenheit: {t}")
            
            # set the digits to show the temperature
            self.displayNumber(3,int(t[0]))
            self.colons.extendSegment(0)
            self.colons.retractSegment(1)
            self.displayNumber(2,int(t[1]))
            self.displayNumber(1,10)

            if celcius:
                self.displayNumber(0,12)
            else:
                self.displayNumber(0,13)
        except Exception as e:
            print(f"Error showIndoorTemp: {e}")
        finally:
            pass

    def showIndoorHumidity(self):
        try:
            print("showIndoorHumidity")
            self.updateIndoorTemp()
            h = str(self.humidity)
            # set the digits to show the temperature
            self.displayNumber(3,int(h[0]))
            self.displayNumber(2,int(h[1]))
            self.colons.extendSegment(0)
            self.colons.retractSegment(1)
            self.displayNumber(1,10)
            self.displayNumber(0,11)
        except Exception as e:
            print(f"Error showIndoorHumidity: {e}")
        finally:
            pass
    
    def showOutdoorTemp(self, celcius):
        try:
            print("showOutdoorTemp")
            conf = Config("config.json")
            temp = conf.read("tempoutdoor")
            cf = conf.read("tempCF")
            if cf == "C":
                if temp < 0:
                    temp *= -1
                print(f"Outdoor temp in Celcius: {temp}") 
            else:
                f = int(round((9/5)*temp+32,0))
                if f < 0:
                    f *= -1
                if f > 99:
                    f -= 100
                temp = f
                print(f"Outdoor temp in Fahrenheit: {temp}")
            
            t = '{0}'.format(temp)
            if len(t) == 3:
                t = t[1:3]
                     
            # set the digits to show the temperature
            self.displayNumber(3,int(t[0]))
            self.colons.retractSegment(0)
            self.colons.extendSegment(1)
            self.displayNumber(2,int(t[1]))
            self.displayNumber(1,10)

            if celcius:
                self.displayNumber(0,12)
            else:
                self.displayNumber(0,13)
        except Exception as e:
            print(f"Error showOutdoorTemp: {e}")
        finally:
            pass
    
    def showOutdoorHumidity(self):
        try:
            print("showOutdoorHumidity")
            conf = Config("config.json")
            humidity = conf.read("humidoutdoor")
            if humidity > 99:
                humidity = 99
            # set the digits to show the temperature
            h = str(humidity)
            self.displayNumber(3,int(h[0]))
            self.displayNumber(2,int(h[1]))
            self.displayNumber(1,10)
            self.displayNumber(0,11)
        except Exception as e:
            print(f"Error showOutdoorHumidity: {e}")
        finally:
            pass

    def showTime(self):
        # set the digits to show the time
        try:
            print(f"showTime display12hour={self.display12hour}")
            #[year, month, day, weekday, hours, minutes, seconds, subseconds]
            dt = self.rtc.datetime()
            t = "{0:02}{1:02}".format(formatHour(dt[4],self.display12hour), dt[5])
            print(f"time={t}")

            if int(t[0]) == 0:
                cmd = uartCommand('3015')
                self.uart1.sendCommand(cmd)
            else:
                self.displayNumber(3,int(t[0]))
            self.displayNumber(2,int(t[1]))
            self.colons.extendSegment(0)
            self.colons.extendSegment(1)
            self.displayNumber(1,int(t[2]))
            self.displayNumber(0,int(t[3]))
        except Exception as e:
            print(f"Error: {e}")
        finally:
            pass
    
    def showDate(self):
        # set the digits to show the date
        try:
            print("showDate")
            #[year, month, day, weekday, hours, minutes, seconds, subseconds]
            dt = self.rtc.datetime()
            t = "{0:02}{1:02}".format(dt[1],dt[2])
            self.displayNumber(3,int(t[0]))
            self.displayNumber(2,int(t[1]))
            self.colons.retractSegment(0)
            self.colons.retractSegment(1)
            self.displayNumber(1,int(t[2]))
            self.displayNumber(0,int(t[3]))
        except Exception as e:
            print(f"Error showDate: {e}")
        finally:
            pass

    def setMotorSpeed(self, percentSpeed):
        print(f"setMotorSpeed percentSpeed={percentSpeed}")
        self.colons.speed = percentSpeed
        for d in range(3,-1,-1):
            cmd = None
            if d < 2:
                cmd = uartCommand('{0}{1}{2:02}'.format(d, uartActions.setmotorspeed, percentSpeed))
                print(f"sending setMotorSpeed command: cmd={cmd.cmdStr}")
                self.uart0.sendCommand(cmd)
                time.sleep(.1)
            else:
                cmd = uartCommand('{0}{1}{2:02}'.format(d, uartActions.setmotorspeed, percentSpeed))
                print(f"sending setMotorSpeed command: cmd={cmd.cmdStr}")
                self.uart1.sendCommand(cmd)
                time.sleep(.1)

    # Set the wait time for the digits to move in tenths of a second
    def setWaitTime(self, tenthsSecondWaitTime):
        print(f"setWaitTime tenthsSecondWaitTime={tenthsSecondWaitTime}")
        self.colons.wait = tenthsSecondWaitTime/100
        for d in range(3,-1,-1):
            cmd = None
            if d < 2:
                cmd = uartCommand('{0}{1}{2:02}'.format(d, uartActions.setwaittime, tenthsSecondWaitTime))
                print(f"sending setWaitTime command: cmd={cmd.cmdStr}")
                self.uart0.sendCommand(cmd)
                time.sleep(.1)
            else:
                cmd = uartCommand('{0}{1}{2:02}'.format(d, uartActions.setwaittime, tenthsSecondWaitTime))
                print(f"sending setWaitTime command: cmd={cmd.cmdStr}")
                self.uart1.sendCommand(cmd)
                time.sleep(.1)
    
    def displayNumber(self,d,n):
        cmd = uartCommand('{0}0{1:02}'.format(d,n))
        if d < 2:     
            self.uart0.sendCommand(cmd)
            print(f"command sent on ch0 to display number: cmd={cmd.cmdStr}")
            time.sleep(.1)
            #cmd = self.uart0.receiveCommand()
        else:
            self.uart1.sendCommand(cmd)
            print(f"command sent on ch1 to display number: cmd={cmd.cmdStr}")
            time.sleep(.1)
            #cmd = self.uart1.receiveCommand()
        del cmd

def loop():

    # Set up the UARTs digits 0 through 3
    controller = Conductor()

    try:

        if controller.hybernateswitch(): #if the hybernate switch is in "off" position
            controller.wifihotspot = PicoWifi("config.json")
            controller.wifihotspot.start_wifi()
            if controller.wifihotspot.ip_address != "":
                controller.wifihotspot.run_server()
            controller.wifihotspot.shutdown_server()
            controller.wifihotspot.shutdownWifi()
            #controller.wifihotspot.__del__()
            while controller.hybernateswitch(): #wait for the switch to be turned to the "on" position
                time.sleep(1)
       
        # Load the configuration
        conf = Config("config.json")
        tempCF = conf.read("tempCF")
        if tempCF == "C":
            cf = True
        else:
            cf = False
        tempWait = int(conf.read("wait"))
        tempSpeed = int(conf.read("speed"))
            # set the motor speed to % (x10) of max
        print(f"tempSpeed={tempSpeed}")
        controller.setMotorSpeed(tempSpeed)
        # set the wait time in hundreths of a second, e.g. 15 = 0.15 seconds
        print(f"tempWait={tempWait}")
        controller.setWaitTime(tempWait)
        tempTime = int(conf.read("time"))
        print(f"tempTime={tempTime}")
        if tempTime == 12:
            print("12 hour time")
            controller.display12hour = True
        else:
            print("24 hour time")
            controller.display12hour = False
        
        # Check if digit test at startup is enabled (default to True if setting not found)
        if  conf.read("enable_test_digits"):
            print("Digit test at startup is enabled")
            time.sleep(.5)
            controller.testDigits()
        else:
            print("Digit test at startup is disabled")

        # Load the schedule 
        try:
            path = f'schedules/{conf.read("schedule")}'
            scheduleConf = uio.open(path)
            s = ujson.load(scheduleConf)
            for i in s["scheduledEvent"]:
                controller.schedule.append(scheduleInfo(i["hour"],i["minute"],i["second"],i["elapse"],i["event"]))
        except ValueError as ve:
            print(f"Schedule loading value error: {ve}")
        except OSError as ioe:
            print(f"Schedule loading IO error: {ioe}")
        finally:
            scheduleConf.close()
            print(f"schedule length={len(controller.schedule)}")

        gc.collect()
        # Enable wifi and sync the RTC
        print("Creating wifi object")
        controller.wifi = PicoWifi("config.json")
        if(controller.wifi.connect_to_wifi_network()):
            time.sleep(1)
            controller.syncRTC.syncclock(controller.rtc)
            etc = extTempHumid(controller.syncRTC)
            etc.setLatLon()
    except Exception as e:
        print(f"Wifi error: {e}")
    finally:
        pass

    controller.updateBrightness()

    while True:
        try:
            for s in controller.schedule:
                a = controller.checkForScheduledAction(s)
                if a == eventActions.displayTime:
                    controller.showTime()
                elif a == eventActions.displayDate:
                    controller.showDate()
                elif a == eventActions.displayIndoorTemp:
                    controller.showIndoorTemp(cf)
                elif a == eventActions.displayIndoorHumidity:
                    controller.showIndoorHumidity()
                elif a == eventActions.displayOutdoorTemp:
                    controller.showOutdoorTemp(cf)
                elif a == eventActions.displayOutdoorHumidity:
                    controller.showOutdoorHumidity()
                elif a == eventActions.updateOutdoorTempHumid:
                    controller.updateOutdoorTempHumid()
                elif a == eventActions.hybernate:
                    controller.scheduledHybernation(s)
                    if controller.wifi:
                        controller.wifi = PicoWifi("config.json")
                        if(controller.wifi.connect_to_wifi_network()):
                            time.sleep(1)
                            controller.syncRTC.syncclock(controller.rtc)
                            etc = extTempHumid(controller.syncRTC)
                            etc.setLatLon()
                    break
            
            time.sleep(1)
            if controller.checkHybernate():
                controller.updateBrightness()

        except Exception as e:
            print(f"Error: {e}")
        finally:
            controller.updateBrightness() 
            time.sleep(1)

##############################
# Manual
##############################

def instructions():
    actions = ['a','c','d','e','h','l','r','s','t','w']

    while True:
        print("Enter a command:")
        print("\t(a)ll digits test")
        print("\t(c)ycle through all digits on both UART channels")
        print("\t(d)igit(0-3)number(0-15)")
        print("\t(h)umidity")
        print("\t(l)uminosity")
        print("\t(r)elay (0=off,1=on)")
        print("\t(s)peed(10-100)% of segment movement")
        print("\t(t)emp(0=C,1=F)")
        print("\t(w)ait(15-30 milliseconds) of segment movement")
        print("\t(e)xit")
        cmd = input("command: ")
        validaction = False
        for i in actions:
            if i == cmd[0].lower():
                validaction = True
                print(f"Choice={i} value={cmd[1:]}")
                break
        if validaction:
            a = cmd[0]
            if a.lower() == 'h' or a.lower() == 'c' or a.lower() == 'a' or a.lower() == 'e':
                v = '0'
                return a.lower(), v
            else:
                v = cmd[1:]
                return a.lower(), v
        else:
            return '',0

#Example usage:
def manual():
    controller = Conductor()
    finished = False

    while not finished:
        a, v = instructions()
        if a == 'a':
            controller.testDigits()
            print("(a)ll digits test")
        elif a == 'c':
            for u in range(15):
                for i in range(2):
                    print("UART{0} test".format(i))
                    uart = uartProtocol(i, commandHelper.baudRate[3])
                    uart.clearQueue()
                    cmdStr = '0{0}{1:02}'.format(i,u)
                    print("sending command: {0}".format(cmdStr))
                    cmd = uartCommand(cmdStr)
                    uart.sendCommand(cmd)
                    time.sleep(1)         
                    del(uart)
        elif a == 'd':
            v = str(v)
            digit = v[0] if len(v) > 0 else '0'
            value = v[1:] if len(v) > 1 else '0'
            print(f"(d)igit={digit} value={value}")
            controller.displayNumber(int(digit), int(value))
        elif a == 't':
            controller.updateIndoorTemp()
            if v == '0':
                controller.showIndoorTemp(True)
                print(f"Outdoor temp in Celcius")
            else:
                controller.showIndoorTemp(False)
                print(f"Indoor temp in Celcius")
        elif a == 'h':
            controller.updateIndoorTemp()
            controller.showIndoorHumidity()
            print(f"Indoor humidity")
        elif a == 'l':
            controller.updateBrightness()
            print(f"Change in luminosity")
        elif a == 'w':
            controller.setWaitTime(int(v))
            print(f"Set segment movement wait time to {v} milliseconds")
        elif a == 'r':
            if v == '1': #this seems backwards but the relay is off it is switched on
                controller.powerRelay.off()
                print(f"Power relay off")
            else:
                controller.powerRelay.on()
                print(f"Power relay on")
        elif a == 's':
            controller.setMotorSpeed(int(v))
            print(f"Set segment movement speed to {v}%")
        else:
            print(f'Quitting program')
            finished = True
            controller.clearDisplay()

if __name__ == '__main__':
    #manual()
    loop()