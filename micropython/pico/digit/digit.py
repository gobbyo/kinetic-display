from machine import Pin, PWM, RTC
from common.uart_protocol import commandHelper, uartCommand
import time
from common.config import Config

# System constants
LED_PWM_FREQUENCY = 1000  # Hz
LED_DEFAULT_BRIGHTNESS = 0.4  # 40% brightness
MOTOR_PWM_FREQUENCY = 50  # Hz
MOTOR_SPEED_PIN = 11  # Pin for controlling motor speed

# Array sizes
NUM_SEGMENTS = 7  # Number of segments per digit

# Time constants
DEFAULT_WAIT_TIME = 0.01  # seconds
RTC_DEFAULT_YEAR = 2000
RTC_DEFAULT_MONTH = 1
RTC_DEFAULT_DAY = 1
RTC_DEFAULT_WEEKDAY = 0

# File constants
CONFIG_FILE = "digit.json"

# Segment movement sequence constants
EXTEND_SEQUENCE = [2, 3, 4, 5, 0, 1, 6]
RETRACT_SEQUENCE = [5, 0, 1, 2, 3, 4, 6]

# Motor tuples (extend pin, retract pin)
motor1 = (12, 13)
motor2 = (14, 15)
motor3 = (16, 17)
motor4 = (18, 19)
motor5 = (20, 21)
motor6 = (22, 26)
motor7 = (27, 10)
motor_pins = [motor1, motor2, motor3, motor4, motor5, motor6, motor7]
led_pins = [2, 3, 6, 7, 8, 9, 28]

class Motoractuator:
    def __init__(self, speedPin, cwPin, ccwPin):
        self.speed = PWM(Pin(speedPin))
        self.speed.freq(MOTOR_PWM_FREQUENCY)
        self.cw = Pin(cwPin, Pin.OUT)
        self.ccw = Pin(ccwPin, Pin.OUT)
        self.stop()
    
    def extend(self, motor_speed, waitTime):
        try:
            # Convert percentage to PWM duty cycle (0-65535)
            self.speed.duty_u16(int((motor_speed / 100) * 65535))
            self.cw.on()
            time.sleep(waitTime)
        except Exception as e:
            print(f"extend error: {e}")
        finally:
            self.stop()
    
    def retract(self, motor_speed, waitTime):
        try:
            # Convert percentage to PWM duty cycle (0-65535)
            self.speed.duty_u16(int((motor_speed / 100) * 65535))
            self.ccw.on()
            time.sleep(waitTime)
        except Exception as e:
            print(f"retract error: {e}")
        finally:
            self.stop()
    
    def stop(self):
        self.speed.duty_u16(0)
        self.cw.off()
        self.ccw.off()

class Digit:
    # PWM duty cycle max value
    MAX_DUTY_CYCLE = 65535
    
    # Default values for configuration
    DEFAULT_MOTOR_SPEED = 50  # 50% speed
    DEFAULT_WAIT_TIME = 0.02  # 20ms
    DEFAULT_DIGIT = 0
    DEFAULT_TEST_DIGIT = 0
    DEFAULT_SEGMENT_STATE = [0, 0, 0, 0, 0, 0, 0]
    
    def __init__(self, led_pins, percentLED_brightness, motor_pins):
        self.leds = []
        for i in range(NUM_SEGMENTS):
            led = PWM(Pin(led_pins[i]))
            led.freq(LED_PWM_FREQUENCY)
            led.duty_u16(0)
            self.leds.append(led)
        self.conf = Config(CONFIG_FILE)
        self._previousDigitArray = self.DEFAULT_SEGMENT_STATE.copy()
        try:
            self.rtc = RTC()
            current = self.conf.read("previous")
            percentLED_brightness = float(self.conf.read("brightness", default=LED_DEFAULT_BRIGHTNESS))
            self._brightness = int(percentLED_brightness * self.MAX_DUTY_CYCLE)
            self._previousDigitArray = self.conf.read("previous", default=self.DEFAULT_SEGMENT_STATE)
            self._motorspeed = int(self.conf.read("motorspeed", default=self.DEFAULT_MOTOR_SPEED))
            self._waitTime = float(self.conf.read("waitTime", default=self.DEFAULT_WAIT_TIME))
            self._digit = int(self.conf.read("digit", default=self.DEFAULT_DIGIT))
            self._testDigit = int(self.conf.read("alien", default=self.DEFAULT_TEST_DIGIT))
        except Exception as e:
            print(f"Error loading configuration: {e}")
            self._brightness = int(LED_DEFAULT_BRIGHTNESS * self.MAX_DUTY_CYCLE)
            self._motorspeed = self.DEFAULT_MOTOR_SPEED
            self._waitTime = self.DEFAULT_WAIT_TIME
            self._digit = self.DEFAULT_DIGIT
            self._testDigit = self.DEFAULT_TEST_DIGIT
            
        self.actuators = []
        for motor in motor_pins:
            m = Motoractuator(MOTOR_SPEED_PIN, motor[0], motor[1])
            m.stop()
            self.actuators.append(m)

        time.sleep(0.5)  # Short delay before setting initial digit
        self.set_digit(current or self.DEFAULT_SEGMENT_STATE)
    
    def __del__(self):
        for led in self.leds:
            led.duty_u16(0)
        self.conf.__del__()

    @property
    def testdigit(self):
        return self._testDigit
    
    @testdigit.setter
    def testdigit(self, test):
        print(f"test digit={test}")
        self._testDigit = test
        self.conf.write("alien", test)
    
    @property
    def motorspeed(self):
        return self._motorspeed

    @motorspeed.setter
    def motorspeed(self, speed):
        self._motorspeed = speed
        self.conf.write("motorspeed", speed)
    
    @property
    def waitTime(self):
        return self._waitTime
    
    @waitTime.setter
    def waitTime(self, wt):
        self._waitTime = wt
        self.conf.write("waitTime", wt)
    
    @property
    def brightness(self):
        return self._brightness
    
    @brightness.setter
    def brightness(self, b):
        self._brightness = int(b * self.MAX_DUTY_CYCLE)
        self.conf.write("brightness", b)
        for i in range(NUM_SEGMENTS):
            if 1 == self._previousDigitArray[i]:
                self.leds[i].duty_u16(self._brightness)
                print(f"----------\nbrightness {self._brightness} seg={i}")

    def getDigitArray(self, val):
        a = [0] * NUM_SEGMENTS
        for i in range(len(a)):
            a[i] = (val & (0x01 << i)) >> i
        return a
    
    def extend_segment(self, seg):
        if(0 == self._previousDigitArray[seg]):
            self.actuators[seg].extend(self._motorspeed, self._waitTime)
            self.leds[seg].duty_u16(self._brightness)
        self._previousDigitArray[seg] = 1
        self.setPreviousDigitArray(self._previousDigitArray)
        return 1

    def retract_segment(self, seg):
        if(1 == self._previousDigitArray[seg]):
            self.actuators[seg].retract(self._motorspeed, self._waitTime)
            self.leds[seg].duty_u16(0)
        self._previousDigitArray[seg] = 0
        self.setPreviousDigitArray(self._previousDigitArray)
        return 1

    def set_digit(self, digitArray):
        actuatorMoves = 0
        print(f"set_digit: {digitArray}")
        for i in range(NUM_SEGMENTS):
            skipped = True
            if (1 == digitArray[i]) and (0 == self._previousDigitArray[i]):
                self.actuators[i].extend(self._motorspeed, self._waitTime)
                print(f"\t[1] seg {chr(i+97)} extended")  # 'a' is ASCII 97
                self.leds[i].duty_u16(self._brightness)
                actuatorMoves += 1
                skipped = False
            
            if (1 == digitArray[i]) and (1 == self._previousDigitArray[i]):
                self.leds[i].duty_u16(self._brightness)
                print(f"\t[1] seg {chr(i+97)} skipped")
                skipped = False

            if (0 == digitArray[i]) and (1 == self._previousDigitArray[i]):
                print(f"\t[0] seg {chr(i+97)} retracted")
                self.leds[i].duty_u16(0)
                self.actuators[i].retract(self._motorspeed, self._waitTime)
                actuatorMoves += 1
                skipped = False
            
            if skipped:
                print(f"\t[{self._previousDigitArray[i]}] seg {chr(i+97)} skipped")

        self.setPreviousDigitArray(digitArray)
        return actuatorMoves

    def setPreviousDigitArray(self, digitArray):
        self.conf.write('previous', digitArray)
        for i in range(NUM_SEGMENTS):
            self._previousDigitArray[i] = digitArray[i]

    def dance(self):
        actuatorMoves = 0
        for seg in EXTEND_SEQUENCE:
            self.extend_segment(seg)
            time.sleep(DEFAULT_WAIT_TIME)
            actuatorMoves += 1
        for seg in RETRACT_SEQUENCE:
            self.retract_segment(seg)
            time.sleep(DEFAULT_WAIT_TIME)
            actuatorMoves += 1
        return actuatorMoves

    def syncTime(self, h, m, s):
        # time tuple = [year, month, day, weekday, hours, minutes, seconds, subseconds]
        self.rtc.datetime((RTC_DEFAULT_YEAR, RTC_DEFAULT_MONTH, RTC_DEFAULT_DAY, 
                          RTC_DEFAULT_WEEKDAY, h, m, s, 0))
    
    # This method is used to format 12 or 24 hour time
    # parameter 'twelveHour' is a boolean value
    # time tuple = [year, month, day, weekday, hours, minutes, seconds, subseconds]
    def setTimeDisplay(self, twelveHour):
        FIRST_DIGIT_POS = 0
        SECOND_DIGIT_POS = 1
        TENS_OFFSET = 0
        ONES_OFFSET = 2  # Offset for minutes position
        TWELVE_HOUR_BLANK = 'F'  # Character to show for blank first digit in 12-hour format
        
        ready = False
        while not ready:
            t = self.rtc.datetime()
            if t[6] % 10 == self._digit:  # Check if seconds match the current digit position
                ready = True
            time.sleep(0.1)
        
        d = '0'
        if self._digit >= TENS_OFFSET and self._digit < SECOND_DIGIT_POS:
            a = '{0:02}'.format(t[4])  # Format hours as 2 digits
            d = a[self._digit]
            print(f"hours d={d}")
        else:
            a = '{0:02}'.format(t[5])  # Format minutes as 2 digits
            d = a[self._digit - ONES_OFFSET]
            print(f"minutes d={d}")

        # In 12-hour format, blank the first digit if it's 0 (e.g. "01" becomes " 1")
        if twelveHour and d == '0' and self._digit == FIRST_DIGIT_POS:
            d = TWELVE_HOUR_BLANK
        
        v = uartCommand.digitValue
        self.set_digit(self.getDigitArray(v[int(d, 16) if d.isalpha() else int(d)]))

def instructions():
    actions = ['c','d','e','h','l','r','s','t','w']

    while True:
        print("Enter a command:")
        print("\t(c)ycle through digits")
        print("\t(d)igit (d0-d9,dA-dF)")
        print("\t(e)xtend segment (e0-e6)")
        print("\t(h)uman or alien digit (h0-h1)")
        print("\t(l)uminosity(0-9)")
        print("\t(r)etract segment (r0-r6)")
        print("\t(s)peed(10-100)% of segment movement")
        print("\t(t)est digits")
        print("\t(w)ait(15-30 milliseconds) of segment movement")
        print("\t(q)uit")
        cmd = input("command: ")
        validaction = False
        for i in actions:
            if i == cmd[0].lower():
                validaction = True
                print(f"Choice={i} value={cmd[1:]}")
                break
        if validaction:
            a = cmd[0]
            if a.lower() == 'c' or a.lower() == 't':
                v = '0'
                return a.lower(), v
            else:
                v = cmd[1:]
                return a.lower(), v
        else:
            return '',0
        
def main():
    d = Digit(led_pins, LED_DEFAULT_BRIGHTNESS, motor_pins)
    helper = commandHelper()
    finished = False
    
    while not finished:
        seg, value = instructions()

        if seg == 'c':
            print("cycle through digits:")
            for i in range(0,16):
                a = helper.decodeHex(value=i)
                print(f"digit=(0x{a:02x})")
                if 1 == d.testdigit:
                    digitArray = d.getDigitArray(uartCommand.digitTest[int(a)])
                else:
                    digitArray = d.getDigitArray(uartCommand.digitValue[int(a)])
                d.set_digit(digitArray)
                time.sleep(1)
        elif seg == 'd':
            print(f"digit=({value})")
            a = helper.decodeHex(value)
            if 1 == d.testdigit:
                digitArray = d.getDigitArray(uartCommand.digitTest[a])
            else:
                digitArray = d.getDigitArray(uartCommand.digitValue[a])
            actuatorMoves = d.set_digit(digitArray)
        elif seg == 'e':
            i = int(value)
            print(f"extend segment=({i})")
            actuatorMoves = d.extend_segment(i)
        elif seg == 'h':
            d.testdigit = int(value)
            if d.testdigit == 1:
                print("digit type = 'alien'")
            else:
                print("digit type = 'human'")
        elif seg == 'l':
            print(f"luminosity=({value})")
            d.brightness = float(value)/10
        elif seg == 'r':
            i = int(value)
            print(f"retract segment=({i})")
            actuatorMoves = d.retract_segment(i)
        elif seg == 's':
            i = int(value)
            print(f"set_motor_speed({i})")
            d.motorspeed = i
        elif seg == 't':
            actuatorMoves = d.dance()
            print(f"test actuator moves={actuatorMoves}")
        elif seg == 'w':
            i = int(value)
            print(f"set_wait_time({i})")
            d.waitTime = i/100
        else:
            finished = True
    d.__del__()
    del d

if __name__ == "__main__":
    main()