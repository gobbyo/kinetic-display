from common.uart_protocol import uartProtocol, uartChannel, uartCommand, commandHelper, uartActions, digitType
from machine import Pin, RTC, WDT  # Added WDT import
import photoresistor
from time_formatter import formatHour
from syncRTC import syncRTC
from externalTemp import extTempHumid
from scheduler import eventActions
import digit_colons
from common.config import Config
import secrets
import gc
import time

# System constants
UART_BAUD_RATE_INDEX = 3
UART_SEND_DELAY = 0.1  # seconds delay between UART commands
DIGIT_COUNT = 4  # Total number of digits (0-3)
UART0_MAX_DIGIT = 1  # Maximum digit number for UART0 (digits 0 and 1)

# Pin assignments
PHOTORESISTOR_PIN = 28
DHT_PIN = 27
DHT_POWER_PIN = 16
HYBERNATE_SWITCH_PIN = 18
POWER_RELAY_PIN = 19

# Time constants
DHT_POWER_ON_DELAY = 1.5  # seconds to wait after powering on DHT sensor
DHT_POWER_OFF_DELAY = 0.25  # seconds to wait before powering off DHT sensor
WIFI_CONNECT_DELAY = 1.0  # seconds to wait after connecting to WiFi
DIGIT_TEST_DELAY = 0.5  # seconds to wait before digit test
DANCE_DELAY = 2.0  # seconds to wait after sending dance command
COMMAND_REPLY_DELAY = 0.5  # seconds to wait for command reply

# Default values
DEFAULT_HOUR = 0
DEFAULT_MINUTE = 0
DEFAULT_SECOND = 0
DEFAULT_BRIGHTNESS_DIVISOR = 10.0  # For converting light level to brightness

# Configuration keys
CONFIG_FILE = "config.json"
CONFIG_TEMP_CF_KEY = "tempCF"
CONFIG_WAIT_KEY = "wait"
CONFIG_SPEED_KEY = "speed"
CONFIG_TIME_KEY = "time"
CONFIG_DIGIT_TYPE_KEY = "digitType"
CONFIG_TEST_ON_STARTUP_KEY = "testOnStartup"
CONFIG_SCHEDULE_KEY = "schedule"

# Add at class level
GC_THRESHOLD = 15  # Run GC every 15 iterations

# Watchdog timeout in milliseconds (8 seconds)
WATCHDOG_TIMEOUT_MS = 8000

# This class is the conductor of the display. It manages the various components of the system
# and orchestrates the display of the time, date, temperature, and humidity. It also manages the
# hybernation of the system and the schedule of events.
class Conductor:
    def __init__(self):
        self._wifi_module = None  # Used to store the actual PicoWifi instance
        self._wifihotspot = None  # Used to store the actual PicoWifi instance
        self._dht = None  # Used to store the actual DHT22 instance
        self.wifihotspot = None
        self.uart0 = uartProtocol(uartChannel.uart0, commandHelper.baudRate[UART_BAUD_RATE_INDEX])
        time.sleep(UART_SEND_DELAY * 7.5)  # Initial delay for UART setup
        self.uart1 = uartProtocol(uartChannel.uart1, commandHelper.baudRate[UART_BAUD_RATE_INDEX])
        self.light = photoresistor.photoresistor(PHOTORESISTOR_PIN)
        self.dhtpower = Pin(DHT_POWER_PIN, Pin.OUT)
        self.display12hour = True
        self.temp = 0
        self.humidity = 0
        self.rtc = RTC()
        self.syncRTC = syncRTC(Config(CONFIG_FILE))
        self.hybernateswitch = Pin(HYBERNATE_SWITCH_PIN, Pin.IN, Pin.PULL_DOWN)
        self.powerRelay = Pin(POWER_RELAY_PIN, Pin.OUT)
        self.schedule = []
        self.brightness = 0
        self.colons = digit_colons.DigitColons(digit_colons.led_pins, digit_colons.DigitColons.brightness, digit_colons.motor_pins)
        self.gc_counter = 0
        self._dt_cache = [0] * 8  # Pre-allocated array for datetime tuple
        # Add to __init__
        COMMAND_BUFFER_SIZE = 16
        self._command_buffer = bytearray(COMMAND_BUFFER_SIZE)
        # Initialize watchdog timer
        self.wdt = WDT(timeout=WATCHDOG_TIMEOUT_MS)

    # Create properties for lazy loading
    @property
    def wifi(self):
        if self._wifi_module is None:
            from picowifiserver import PicoWifi
            self._wifi_module = PicoWifi("config.json", secrets.usr, secrets.pwd)
        return self._wifi_module

    @wifi.setter
    def wifi(self, value):
        self._wifi_module = value

    @property
    def wifihotspot(self):
        if self._wifihotspot is None:
            from picowifiserver import PicoWifi
            self._wifihotspot = PicoWifi("config.json")
        return self._wifihotspot

    @wifihotspot.setter
    def wifihotspot(self, value):
        self._wifihotspot = value

    @property
    def dht(self):
        if self._dht is None:
            import dht
            self._dht = dht.DHT22(Pin(DHT_PIN))
        return self._dht

    @dht.setter
    def dht(self, value):
        self._dht = value

    def get_datetime(self):
        dt = self.rtc.datetime()
        # Copy values to pre-allocated array
        for i in range(8):
            self._dt_cache[i] = dt[i]
        return self._dt_cache

    def checkForScheduledAction(self, s):
        dt = self.get_datetime()
        
        # Extract relevant time components once
        current_hour = dt[4]
        current_minute = dt[5]
        current_second = dt[6]
        
        # Check hibernation first with direct comparison instead of string formatting
        if s.event == eventActions.hybernate:
            if (current_hour == s.hour or s.hour == -1) and (current_minute == s.minute or s.minute == -1):
                return eventActions.hybernate
        
        # For non-hibernation events
        if s.event < eventActions.hybernate:
            if (s.hour == -1 and current_minute == s.minute) or (s.hour == -1 and s.minute == -1):
                if current_second >= s.second and current_second < (s.second + s.elapse):
                    return s.event
        
        return 0
    
    def scheduledHybernation(self,s):
        print("scheduledHybernation")
        cleared = False
        hybernating = True
        try:
            dt = self.get_datetime()
            m = s.elapse + (dt[4] * 60) + dt[5]
            deadlineinHours = int(m/60) % 24 #hours
            deadlineinMinutes = int(m%60)
            print(f"deadline {deadlineinHours}:{deadlineinMinutes}")
            while hybernating:
                dt = self.get_datetime()
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
            #self.wifi = PicoWifi("config.json", secrets.usr,secrets.pwd)
            self.wifi.connect_to_wifi_network()
            self.syncRTC.refresh_timezone()
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
                #self.wifi = PicoWifi("config.json", secrets.usr,secrets.pwd)
                self.wifi.connect_to_wifi_network()
                self.syncRTC.refresh_timezone()
                self.syncRTC.syncclock(self.rtc)
        return hybernated

    def updateIndoorTemp(self):
        self.dhtpower.on()
        time.sleep(DHT_POWER_ON_DELAY)
        self.temp = 0
        self.humidity = 0
        try:
            self.dht.measure()
            self.temp = self.dht.temperature()
            self.humidity = self.dht.humidity()
        except Exception as e:
            print(f"Error updateIndoorTemp: {e}")
        finally:
            time.sleep(DHT_POWER_OFF_DELAY)
            self.dhtpower.off()

    def updateOutdoorTempHumid(self):
        try:
            # Remove the with statement since extTempHumid is not a context manager
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
        for d in range(DIGIT_COUNT - 1, -1, -1):
            cmd = None
            if d <= UART0_MAX_DIGIT:
                if d == 1:
                    self.colons.brightness = curlight / DEFAULT_BRIGHTNESS_DIVISOR
                cmd = uartCommand('{0}{1}{2:02}'.format(d, uartActions.brightness, curlight))
                self.uart0.sendCommand(cmd)
            else:
                cmd = uartCommand('{0}{1}{2:02}'.format(d, uartActions.brightness, curlight))
                self.uart1.sendCommand(cmd)
            print(f"sending brightness command to digit {d} = {cmd.cmdStr}")
            time.sleep(UART_SEND_DELAY)
        self.brightness = curlight

    def clearDisplay(self):
        # Set the brightness of the digits
        try:
            for d in range(DIGIT_COUNT - 1, -1, -1):
                cmd = None
                if d <= UART0_MAX_DIGIT:
                    if d == 1:
                        self.colons.retractSegment(0)
                        self.colons.retractSegment(1)
                    cmd = uartCommand('{0}015'.format(d))
                    self.uart0.sendCommand(cmd)
                    print(f"clear display: cmd={cmd.cmdStr}")
                    time.sleep(UART_SEND_DELAY)
                else:
                    cmd = uartCommand(f'{d}015')
                    self.uart1.sendCommand(cmd)
                    print(f"clear display: cmd={cmd.cmdStr}")
                    time.sleep(UART_SEND_DELAY)
        except Exception as e:
            print(f"Error cleardisplay: {e}")
        finally:
            pass

    def testDigits(self):
        # Initialize/test each digit
        for d in range(DIGIT_COUNT - 1, -1, -1):
            cmd = None
            if d <= UART0_MAX_DIGIT:
                if d == 1:
                    time.sleep(DIGIT_TEST_DELAY * 2)
                    self.colons.dance()
                cmd = uartCommand('{0}{1}{2:02}'.format(d, uartActions.dance, 0))
                self.uart0.sendCommand(cmd)
            else:
                cmd = uartCommand('{0}{1}{2:02}'.format(d, uartActions.dance, 0))
                self.uart1.sendCommand(cmd)
            print(f"sending dance command: cmd={cmd.cmdStr}")
            time.sleep(DANCE_DELAY)
            
            if cmd is not None:
                print(f"received reply: cmd={cmd.cmdStr}")
            
            time.sleep(COMMAND_REPLY_DELAY)

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
            self.colons.retractSegment(0)
            self.colons.extendSegment(1)
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
            dt = self.get_datetime()
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
            dt = self.get_datetime()
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
        
        # Create a single command object and reuse it
        # Fix the format string to include all three parameters
        cmd = uartCommand('{0}{1}{2:02}'.format(0, uartActions.setmotorspeed, percentSpeed))
        
        for d in range(DIGIT_COUNT - 1, -1, -1):
            # Modify the first character instead of creating new command
            cmd.cmdStr = cmd.cmdStr.replace(cmd.cmdStr[0], str(d))
            cmd.digit = d
            
            if d <= UART0_MAX_DIGIT:
                print(f"sending setMotorSpeed command: cmd={cmd.cmdStr}")
                self.uart0.sendCommand(cmd)
            else:
                print(f"sending setMotorSpeed command: cmd={cmd.cmdStr}")
                self.uart1.sendCommand(cmd)
                
            time.sleep(UART_SEND_DELAY)

    # Set the wait time for the digits to move in tenths of a second
    def setWaitTime(self, tenthsSecondWaitTime):
        print(f"setWaitTime tenthsSecondWaitTime={tenthsSecondWaitTime}")
        self.colons.wait = tenthsSecondWaitTime/100
        for d in range(DIGIT_COUNT - 1, -1, -1):
            cmd = None
            if d <= UART0_MAX_DIGIT:
                cmd = uartCommand('{0}{1}{2:02}'.format(d, uartActions.setwaittime, tenthsSecondWaitTime))
                print(f"sending setWaitTime command: cmd={cmd.cmdStr}")
                self.uart0.sendCommand(cmd)
                time.sleep(UART_SEND_DELAY)
            else:
                cmd = uartCommand('{0}{1}{2:02}'.format(d, uartActions.setwaittime, tenthsSecondWaitTime))
                print(f"sending setWaitTime command: cmd={cmd.cmdStr}")
                self.uart1.sendCommand(cmd)
                time.sleep(UART_SEND_DELAY)
    
    def setDigittype(self, digitType):
        print(f"setDigittype digitType={digitType}")
        for d in range(DIGIT_COUNT - 1, -1, -1):
            cmd = None
            if d <= UART0_MAX_DIGIT:
                cmd = uartCommand('{0}{1}{2:02}'.format(d, uartActions.digittype, digitType))
                print(f"sending setDigittype command: cmd={cmd.cmdStr}")
                self.uart0.sendCommand(cmd)
                time.sleep(UART_SEND_DELAY)
            else:
                cmd = uartCommand('{0}{1}{2:02}'.format(d, uartActions.digittype, digitType))
                print(f"sending setDigittype command: cmd={cmd.cmdStr}")
                self.uart1.sendCommand(cmd)
                time.sleep(UART_SEND_DELAY)
    
    def displayNumber(self, d, n):
        # Avoid format string allocations by using simple concatenation for small strings
        cmd_str = str(d) + '0' + ('0' + str(n))[-2:]
        cmd = uartCommand(cmd_str)
        
        if d <= UART0_MAX_DIGIT:     
            self.uart0.sendCommand(cmd)
            print("command sent on ch0 to display number: cmd=", cmd_str)
            time.sleep(UART_SEND_DELAY)
        else:
            self.uart1.sendCommand(cmd)
            print("command sent on ch1 to display number: cmd=", cmd_str)
            time.sleep(UART_SEND_DELAY)
        del cmd

    def release_resources(self):
        """Explicitly release resources to help garbage collection"""
        # Release UART resources
        if hasattr(self, 'uart0'):
            del self.uart0
        if hasattr(self, 'uart1'):
            del self.uart1
        
        # Release sensor resources
        if hasattr(self, 'dht'):
            del self.dht
        
        # Force garbage collection
        gc.collect()

def loop():

    # Initialize the watchdog timer with 8-second timeout
    wdt = WDT(timeout=WATCHDOG_TIMEOUT_MS)
    print(f"Watchdog timer initialized with {WATCHDOG_TIMEOUT_MS}ms timeout")
    
    # Set up the UARTs digits 0 through 3
    controller = Conductor()

    try:
        # Feed the watchdog after initialization
        wdt.feed()
        
        if controller.hybernateswitch(): #if the hybernate switch is in "off" position
            # Use the property instead of direct instantiation
            controller.wifihotspot.start_wifi()
            if controller.wifihotspot.ip_address != "":
                controller.wifihotspot.run_server()
                # Feed watchdog periodically during long operations
                wdt.feed()
            controller.wifihotspot.shutdown_server()
            controller.wifihotspot.shutdownWifi()
            controller.wifihotspot = None
            while controller.hybernateswitch(): #wait for the switch to be turned to the "on" position
                time.sleep(1)
                wdt.feed()  # Feed watchdog while waiting
            import machine
            machine.reset()

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
        
        # Feed watchdog after motor speed configuration
        wdt.feed()
        
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
        thetype = conf.read("digitType")
        if "Earth" in thetype:
            controller.setDigittype(digitType.human)
        else:
            controller.setDigittype(digitType.alien)
        
        # Feed watchdog after digit type configuration
        wdt.feed()
        
        # Check if digit test at startup is enabled (default to True if setting not found)
        test_on_startup = conf.read("testOnStartup")
        print(f"Test on startup setting: {test_on_startup}")
        # Convert string value to boolean properly
        if test_on_startup is not None:
            if isinstance(test_on_startup, str):
                enable_test = test_on_startup.lower() == "true"
            else:
                enable_test = bool(test_on_startup)
        else:
            # Default to False if setting not found
            enable_test = False
            
        if enable_test:
            print("Digit test at startup is enabled")
            time.sleep(.5)
            controller.testDigits()
            # Feed watchdog after digit test
            wdt.feed()
        else:
            print("Digit test at startup is disabled")

        # Load the schedule with feeding the watchdog
        try:
            path = f'schedules/{conf.read("schedule")}'
            # Import the optimized schedule loader
            from scheduler import ScheduleLoader
            import gc
            
            # Start with the most reliable method first
            print("Loading schedule...")
            controller.schedule = []
            
            # Feed watchdog before schedule loading
            wdt.feed()
            
            try:
                print("Trying simple loader...")
                controller.schedule = ScheduleLoader.load_schedule_simple(path)
                
                # If simple loader returned no events, try other methods
                if len(controller.schedule) == 0:
                    gc.collect()
                    # Feed watchdog between load attempts
                    wdt.feed()
                    print("Simple loader returned no events, trying stream loader...")
                    controller.schedule = ScheduleLoader.load_schedule_stream(path)
                    
                    if len(controller.schedule) == 0:
                        gc.collect()
                        # Feed watchdog between load attempts
                        wdt.feed()
                        print("Stream loader returned no events, trying optimized loader...")
                        controller.schedule = ScheduleLoader.load_schedule_optimized(path)
            except Exception as e:
                print(f"Schedule loading error: {e}")
                controller.schedule = []
            
            print(f"Schedule loaded - {len(controller.schedule)} events")
            
            # Dump the loaded schedule for debugging
            print("Loaded schedule events:")
            for idx, s in enumerate(controller.schedule):
                print(f"Event {idx}: hour={s.hour}, minute={s.minute}, second={s.second}, elapse={s.elapse}, event={s.event}")
                # Feed watchdog periodically during long operations
                if idx % 10 == 0:
                    wdt.feed()
                
            gc.collect()
        except Exception as e:
            print(f"Schedule loading error: {e}")
            controller.schedule = []
        
        # Feed watchdog after schedule loading
        wdt.feed()
        gc.collect()

        # Enable wifi and sync the RTC
        print("Creating wifi object")
        #controller.wifi = PicoWifi("config.json", secrets.usr,secrets.pwd)
        if(controller.wifi.connect_to_wifi_network()):
            time.sleep(1)
            # Feed watchdog during network operations
            wdt.feed()
            controller.syncRTC.refresh_timezone()
            controller.syncRTC.syncclock(controller.rtc)
            # Feed watchdog after clock sync
            wdt.feed()
            etc = extTempHumid(controller.syncRTC)
            etc.setLatLon()
    except Exception as e:
        print(f"Wifi error: {e}")
    finally:
        # Always feed the watchdog if there's an exception
        wdt.feed()
        pass

    controller.updateBrightness()

    while True:
        try:
            dt = controller.get_datetime()  # Get this once per loop instead of for each schedule item
            
            # Only process events that might be active in this minute
            current_minute = dt[5]  # Minutes from datetime
            current_hour = dt[4]    # Hours from datetime
            current_second = dt[6]  # Seconds from datetime
            
            # Initialize action variable at the start of each loop
            a = 0
            
            for s in controller.schedule:
                # Quick pre-filtering - skip events that can't possibly match current time
                if (s.minute != -1 and s.minute != current_minute and 
                    not (s.hour == -1 and s.minute == -1)):
                    continue
                
                if (s.hour != -1 and s.hour != current_hour and 
                    not (s.hour == -1 and s.minute == -1)):
                    continue
                    
                # Only for non-hibernation events, check seconds
                if s.event != eventActions.hybernate:
                    if current_second < s.second or current_second >= (s.second + s.elapse):
                        continue

                # Now do the full check for matching events
                if s.event == eventActions.hybernate:
                    if (current_hour == s.hour or s.hour == -1) and (current_minute == s.minute or s.minute == -1):
                        a = eventActions.hybernate
                else:
                    # Check for scheduled actions
                    # We can skip the second check if hour and minute are both -1
                    # We need to check for specific hour matches too
                    if ((s.hour == -1 and s.minute == current_minute) or 
                        (s.hour == -1 and s.minute == -1) or
                        (s.hour == current_hour and s.minute == current_minute)):
                        if current_second >= s.second and current_second < (s.second + s.elapse):
                            a = s.event

                # Process the scheduled action
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
                    # Feed watchdog after network operation
                    wdt.feed()
                elif a == eventActions.hybernate:
                    # Pass the watchdog to scheduledHybernation
                    controller.scheduledHybernation(s)
                    # Feed immediately after returning from hibernation
                    wdt.feed()
            
            time.sleep(1)
            if controller.checkHybernate():
                controller.updateBrightness()
                # Feed watchdog after hibernation check
                wdt.feed()

            # Add this for debugging after your event processing - make sure s is defined
            if a == 0 and len(controller.schedule) > 0:  # Only print if no action and there are scheduled events
                # Don't reference s directly here as it might be undefined if schedule was empty
                print(f"No scheduled action triggered at: hour={current_hour}, min={current_minute}, sec={current_second}")

            # Periodic garbage collection
            controller.gc_counter += 1
            if controller.gc_counter >= GC_THRESHOLD:
                gc.collect()
                controller.gc_counter = 0

            # Feed the watchdog timer at the end of each loop iteration
            wdt.feed()

        except Exception as e:
            print(f"Error: {e}")
        finally:
            controller.updateBrightness() 
            time.sleep(1)
            # Feed the watchdog in the finally block to ensure it's always fed
            wdt.feed()

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