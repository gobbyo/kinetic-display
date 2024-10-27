from uart_protocol import uartProtocol, uartChannel, uartCommand, commandHelper, uartActions
from dht11 import DHT11, InvalidChecksum, InvalidPulseCount
from machine import Pin, RTC
import photoresistor
from time_formatter import formatHour
from picowifi import hotspot
from syncRTC import syncRTC
from externalTemp import extTempHumid
from scheduler import scheduleInfo, eventActions
import digit_colons
import config
import secrets
import time
import json
import io

photoresistorPin = 28
dhtPin = 27
dhtPowerpin = 16
hybernateswitchPin = 18
powerRelayPin = 19

# This class is the conductor of the display. It manages the various components of the system
# and orchestrates the display of the time, date, temperature, and humidity. It also manages the
# hybernation of the system and the schedule of events.
class conductor:
    def __init__(self):
        self.uart0 = uartProtocol(uartChannel.uart0, commandHelper.baudRate[3])
        time.sleep(.75)
        self.uart1 = uartProtocol(uartChannel.uart1, commandHelper.baudRate[3])
        self.light = photoresistor.photoresistor(photoresistorPin)
        self.dht = DHT11(Pin(dhtPin))
        self.dhtpower = Pin(dhtPowerpin, Pin.OUT)
        self.display12hour = True
        self.temp = 0
        self.humidity = 0
        self.rtc = RTC()
        self.hybernateswitch = Pin(hybernateswitchPin, Pin.IN, Pin.PULL_DOWN)
        self.powerRelay = Pin(powerRelayPin, Pin.OUT)
        self.schedule = []
        self.brightness = 0
        self.colons = digit_colons.Digit_Colons(digit_colons.led_pins, digit_colons.LEDbrightness, digit_colons.motor_pins)

    def checkForScheduledAction(self, s):
        #print("checkForScheduledAction for event={0}".format(s.event))
        #[year, month, day, weekday, hours, minutes, seconds, subseconds]
        dt = self.rtc.datetime()
        t = s.elapse + s.second
        if t > 60:
            t = t - 60

        if s.event == eventActions.displayTime:
            if s.hour == -1 and dt[6] >= s.second or dt[6] <= t:
                return eventActions.displayTime
        elif s.event == eventActions.hybernate:
            if dt[4] == s.hour and dt[5] == s.minute:
                return eventActions.hybernate
        elif s.event >= eventActions.displayDate or s.event <= eventActions.updateOutdoorTempHumid:
            if s.hour == -1 and dt[5] == s.minute and dt[6] >= s.second and dt[6] <= t:
                return s.event
        else:
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
            print("deadline {0}:{1}".format(deadlineinHours, deadlineinMinutes))
            while hybernating:
                dt = self.rtc.datetime()
                if deadlineinHours == dt[4] and deadlineinMinutes == dt[5]:
                    hybernating = False
                if self.hybernateswitch():
                    hybernating = False
                #Clear the display
                if not cleared:
                    print("hybernating...")
                    self.cleardisplay()
                    time.sleep(2)
                    self.powerRelay.on()
                    cleared = True
                time.sleep(1)
        except Exception as e:
            print("Error scheduledHybernation: {0}".format(e))
        finally:
            self.powerRelay.off()
            syncrtc = syncRTC()
            syncrtc.syncclock()
            #time.sleep(2)
        pass

    def checkHybernate(self):
        cleared = False
        hybernated = False
        try:
            while self.hybernateswitch():
                #Clear the display
                if not cleared:
                    self.cleardisplay()
                    print("hybernating...")
                    time.sleep(2)
                    self.powerRelay.on()
                    cleared = True
                    hybernated = True
                time.sleep(1)
        except Exception as e:
            print("Error hybernateswitch: {0}".format(e))
        finally:
            self.powerRelay.off()
            if hybernated:
                rtc = syncRTC()
                rtc.syncclock()
        return hybernated

    def updateIndoorTemp(self):
        self.dhtpower.on()
        time.sleep(1.5)
        try:
            self.dht.measure()
            self.temp = '{0:02}'.format(int(self.dht.temperature))
            self.humidity = '{0:02}'.format(int(self.dht.humidity))
            print("Temp: {0} Humidity: {1}".format(self.temp, self.humidity))
        except InvalidChecksum:
            print("Invalid checksum")
        except InvalidPulseCount:
            print("Invalid pulse count")
        except Exception as e:
            print("Error updateIndoorTemp: {0}".format(e))
        finally:
            time.sleep(.25)
            self.dhtpower.off()

    def updateOutdoorTempHumid(self):
        try:
            syncrtc = syncRTC()
            etc = extTempHumid(syncrtc)
            etc.updateOutdoorTemp()
        except Exception as e:
            print("Error conductor updateOutdoorTempHumid: {0}".format(e))
        finally:
            pass

    def updatebrightness(self):
        curlight = self.light.read()
        if curlight == self.brightness:
            return
        print("Light level: {0}".format(curlight))
        # Set the brightness of the digits
        for d in range(3,-1,-1):
            cmd = None
            if d < 2:
                if d == 1:
                    self.colons.brightness = curlight/10
                cmd = uartCommand('{0}{1}{2:02}'.format(d, uartActions.brightness, curlight))
                self.uart0.sendCommand(cmd)
                print("sending brightness command to digit {0} = {1}".format(d,cmd.cmdStr))
                time.sleep(.1)
            else:
                cmd = uartCommand('{0}{1}{2:02}'.format(d, uartActions.brightness, curlight))
                self.uart1.sendCommand(cmd)
                print("sending brightness command to digit {0} = {1}".format(d,cmd.cmdStr))
                time.sleep(.1)
        self.brightness = curlight

    def cleardisplay(self):
        # Set the brightness of the digits
        try:
            for d in range(3,-1,-1):
                cmd = None
                if d < 2:
                    if d == 1:
                        self.colons.retract_segment(0)
                        self.colons.retract_segment(1)
                    cmd = uartCommand('{0}015'.format(d))
                    self.uart0.sendCommand(cmd)
                    print("clear display: cmd={0}".format(cmd.cmdStr))
                    time.sleep(.1)
                    #cmd = self.uart0.receiveCommand()
                else:
                    cmd = uartCommand('{0}015'.format(d))
                    self.uart1.sendCommand(cmd)
                    print("clear display: cmd={0}".format(cmd.cmdStr))
                    time.sleep(.1)
                    #cmd = self.uart1.receiveCommand()
        except Exception as e:
            print("Error cleardisplay: {0}".format(e))
        finally:
            pass

    def testdigits(self):
        # Initialize/test each digit
        for d in range(3,-1,-1):
            cmd = None
            if d < 2:
                if d == 1:
                    time.sleep(.2)
                    self.colons.dance()
                cmd = uartCommand('{0}{1}{2:02}'.format(d, uartActions.dance, 0))
                self.uart0.sendCommand(cmd)
                print("sending dance command: cmd={0}".format(cmd.cmdStr))
                time.sleep(2)
                #cmd = self.uart0.receiveCommand()
            else:
                cmd = uartCommand('{0}{1}{2:02}'.format(d, uartActions.dance, 0))
                self.uart1.sendCommand(cmd)
                print("sending dance command: cmd={0}".format(cmd.cmdStr))
                time.sleep(2)
                #cmd = self.uart1.receiveCommand()
            
            if cmd is not None:
                print("received reply: cmd={0}".format(cmd.cmdStr))
            
            time.sleep(.5)

    def showIndoorTemp(self, celcius):
        try:
            print("showIndoorTemp")
            self.updateIndoorTemp()
            t = self.temp
            if not celcius:
                t = '{0:02}'.format(round((9/5)*int(self.temp))+32,0)
                print("Temp in Fahrenheit: {0}".format(t))
            
            # set the digits to show the temperature
            self.displayNumber(3,int(t[0]))
            self.colons.extend_segment(0)
            self.colons.retract_segment(1)
            self.displayNumber(2,int(t[1]))
            self.displayNumber(1,10)

            if celcius:
                self.displayNumber(0,12)
            else:
                self.displayNumber(0,13)
        except Exception as e:
            print("Error showIndoorTemp: {0}".format(e))
        finally:
            pass

    def showIndoorHumidity(self):
        try:
            print("showIndoorHumidity")
            self.updateIndoorTemp()
            # set the digits to show the temperature
            self.displayNumber(3,int(self.humidity[0]))
            self.displayNumber(2,int(self.humidity[1]))
            self.colons.extend_segment(0)
            self.colons.retract_segment(1)
            self.displayNumber(1,10)
            self.displayNumber(0,11)
        except Exception as e:
            print("Error showIndoorHumidity: {0}".format(e))
        finally:
            pass
    
    def showOutdoorTemp(self, celcius):
        try:
            print("showOutdoorTemp")
            conf = config.Config("config.json")
            temp = conf.read("tempoutdoor")
            cf = conf.read("tempCF")
            if cf == "C":
                if temp < 0:
                    temp *= -1
                print("Outdoor temp in Celcius: {0}".format(temp)) 
            else:
                f = round((9/5)*int(temp))+32
                if f < 0:
                    f *= -1
                if f > 99:
                    f -= 100
                temp = f
                print("Outdoor temp in Fahrenheit: {0}".format(temp))
            
            t = '{0}'.format(temp)
            if len(t) == 3:
                t = t[1:3]
                     
            # set the digits to show the temperature
            self.displayNumber(3,int(t[0]))
            self.colons.retract_segment(0)
            self.colons.extend_segment(1)
            self.displayNumber(2,int(t[1]))
            self.displayNumber(1,10)

            if celcius:
                self.displayNumber(0,12)
            else:
                self.displayNumber(0,13)
        except Exception as e:
            print("Error showOutdoorTemp: {0}".format(e))
        finally:
            pass
    
    def showOutdoorHumidity(self):
        try:
            print("showOutdoorHumidity")
            conf = config.Config("config.json")
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
            print("Error showOutdoorHumidity: {0}".format(e))
        finally:
            pass

    def showTime(self):
        # set the digits to show the time
        try:
            print("showTime display12hour={0}".format(self.display12hour))
            #[year, month, day, weekday, hours, minutes, seconds, subseconds]
            dt = self.rtc.datetime()
            t = "{0:02}{1:02}".format(formatHour(dt[4],self.display12hour), dt[5])
            print("t={0}".format(t))

            if int(t[0]) == 0:
                cmd = uartCommand('3015')
                self.uart1.sendCommand(cmd)
            else:
                self.displayNumber(3,int(t[0]))
            self.displayNumber(2,int(t[1]))
            self.colons.extend_segment(0)
            self.colons.extend_segment(1)
            self.displayNumber(1,int(t[2]))
            self.displayNumber(0,int(t[3]))
        except Exception as e:
            print("Error: {0}".format(e))
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
            self.colons.retract_segment(0)
            self.colons.retract_segment(1)
            self.displayNumber(1,int(t[2]))
            self.displayNumber(0,int(t[3]))
        except Exception as e:
            print("Error showDate: {0}".format(e))
        finally:
            pass

    def setMotorSpeed(self, percentSpeed):
        print("setMotorSpeed percentSpeed={0}".format(percentSpeed))
        self.colons.motorspeed = percentSpeed
        for d in range(3,-1,-1):
            cmd = None
            if d < 2:
                cmd = uartCommand('{0}{1}{2:02}'.format(d, uartActions.setmotorspeed, percentSpeed))
                print("sending setMotorSpeed command: cmd={0}".format(cmd.cmdStr))
                self.uart0.sendCommand(cmd)
                time.sleep(.1)
            else:
                cmd = uartCommand('{0}{1}{2:02}'.format(d, uartActions.setmotorspeed, percentSpeed))
                print("sending setMotorSpeed command: cmd={0}".format(cmd.cmdStr))
                self.uart1.sendCommand(cmd)
                time.sleep(.1)

    # Set the wait time for the digits to move in tenths of a second
    def setWaitTime(self, tenthsSecondWaitTime):
        print("setWaitTime tenthsSecondWaitTime={0}".format(tenthsSecondWaitTime))
        self.colons.waitTime = tenthsSecondWaitTime/100
        for d in range(3,-1,-1):
            cmd = None
            if d < 2:
                cmd = uartCommand('{0}{1}{2:02}'.format(d, uartActions.setwaittime, tenthsSecondWaitTime))
                print("sending setWaitTime command: cmd={0}".format(cmd.cmdStr))
                self.uart0.sendCommand(cmd)
                time.sleep(.1)
            else:
                cmd = uartCommand('{0}{1}{2:02}'.format(d, uartActions.setwaittime, tenthsSecondWaitTime))
                print("sending setWaitTime command: cmd={0}".format(cmd.cmdStr))
                self.uart1.sendCommand(cmd)
                time.sleep(.1)
    
    def displayNumber(self,d,n):
        cmd = uartCommand('{0}0{1:02}'.format(d,n))
        if d < 2:     
            self.uart0.sendCommand(cmd)
            print("display number: cmd={0}".format(cmd.cmdStr))
            time.sleep(.1)
            #cmd = self.uart0.receiveCommand()
        else:
            self.uart1.sendCommand(cmd)
            print("display number: cmd={0}".format(cmd.cmdStr))
            time.sleep(.1)
            #cmd = self.uart1.receiveCommand()

def loop():

    # Set up the UARTs digits 0 through 3
    controller = conductor()

    # Load the schedule
    try:
        scheduleConf = io.open("scheduleconfig.json")
        s = json.load(scheduleConf)
        for i in s["scheduledEvent"]:
            print("--schedule info--")
            controller.schedule.append(scheduleInfo(i["hour"],i["minute"],i["second"],i["elapse"],i["event"]))
    except ValueError as ve:
        print("Schedule loading value error: {0}".format(ve))
    except OSError as ioe:
        print("Schedule loading IO error: {0}".format(ioe))
    finally:
        scheduleConf.close()

    try:

        if controller.hybernateswitch(): #if the hybernate switch is in "off" position
            wifi = hotspot("7segdisplay","12oclock")
            wifi.connectAdmin()
            while controller.hybernateswitch(): #wait for the switch to be turned to the "on" position
                time.sleep(1)
       
        conf = config.Config("config.json")
        tempCF = conf.read("tempCF")
        if tempCF == "C":
            cf = True
        else:
            cf = False

        tempWait = int(conf.read("wait"))
        tempSpeed = int(conf.read("speed"))
            # set the motor speed to % (x10) of max
        print("tempSpeed={0}".format(tempSpeed))
        controller.setMotorSpeed(tempSpeed)
        # set the wait time in hundreths of a second, e.g. 15 = 0.15 seconds
        print("tempWait={0}".format(tempWait))
        controller.setWaitTime(tempWait)
        tempTime = int(conf.read("time"))
        print("tempTime={0}".format(tempTime))
        if tempTime == 12:
            print("12 hour time")
            controller.display12hour = True
        else:
            print("24 hour time")
            controller.display12hour = False
        time.sleep(.5)
        controller.testdigits()

        ssid = secrets.usr
        pwd = secrets.pwd
        wifi = hotspot(ssid,pwd)
        wifi.connectWifi()
        syncrtc = syncRTC()
        syncrtc.syncclock()
        etc = extTempHumid(syncrtc)
        etc.setLatLon()
    except Exception as e:
        print("Wifi error: {0}".format(e))
    finally:
        pass
    
    try:
        controller.updateIndoorTemp()
    except InvalidChecksum:
        print("Invalid checksum")
    except InvalidPulseCount:
        print("Invalid pulse count")
    except Exception as e:
        print("RTC error: {0}".format(e))
    finally:
        pass

    controller.updatebrightness()
    controller.showTime()

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
                    break
            
            time.sleep(1)
            if controller.checkHybernate():
                controller.showTime()

        except InvalidChecksum:
            print("Invalid checksum")
        except InvalidPulseCount:
            print("Invalid pulse count")
        except Exception as e:
            print("Error: {0}".format(e))
        finally:
            controller.updatebrightness() 
            time.sleep(1)

##############################
# Manual
##############################

def instructions():
    actions = ['A','C','D','E','H','L','R','S','T','W']

    while True:
        print("'A' = test all digits")
        print("'D(0-3,0-15)' = digit and number to display")
        print("'L' = update brightness")
        print("'C' = current time")
        print("T'(0-1)' = temp in 0 = celcius or 1 = farenheit")
        print("'H' = humidity")
        print("'W(15-30)' = motor wait time in milliseconds")
        print("'S(10-100)' = motor speed %")
        cmd = input("command: ")
        validaction = False
        for i in actions:
            if i == cmd[0].upper():
                validaction = True
                print("{0} is a valid action".format(i))
                break
        if validaction:
            a = cmd[0]
            if a.upper() == 'H':
                v = '0'
                return a.upper(), v
            elif a.upper() == 'C':
                v = '0'
                return a.upper(), v
            else:
                v = cmd[1:]  
                return a.upper(), v
        else:
            return '',0

def manual():
    controller = conductor()
    finished = False
    while not finished:
        a, v = instructions()
        print("action={0} value={1}".format(a,v))
        if a == 'A':
            controller.testdigits()
            print("Test all digits")
        elif a == 'D':
            digit = v[0]
            value = v[1:]
            print("digit={0} value={1}".format(digit,value))
            controller.displayNumber(int(digit),int(value))
        elif a == 'T':
            controller.updateIndoorTemp()
            if v == '0':
                controller.showIndoorTemp(True)
            else:
                controller.showIndoorTemp(False)
        elif a == 'H':
            controller.updateIndoorTemp()
            controller.showIndoorHumidity()
        elif a == 'L':
            controller.updatebrightness()
        elif a == 'C':
            controller.showTime()
        elif a == 'W':
            controller.setMotorSpeed(int(v))
        elif a == 'S':
            controller.setMotorSpeed(int(v))
        else:
            finished = True
            controller.cleardisplay()

if __name__ == '__main__':
    #manual()
    loop()