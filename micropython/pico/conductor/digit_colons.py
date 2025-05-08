from machine import Pin, PWM, RTC
from common.uart_protocol import commandHelper, uartCommand
import time
from common.config import Config

# LED constants
LED_PWM_FREQUENCY = 1000  # Hz
LED_DEFAULT_BRIGHTNESS = 0.4
MAX_DUTY_CYCLE = 65535
BRIGHTNESS_LIMIT_FACTOR = 0.14
MAX_BRIGHTNESS = MAX_DUTY_CYCLE * BRIGHTNESS_LIMIT_FACTOR

# Motor constants
MOTOR_PWM_FREQUENCY = 50  # Hz
MOTOR_SPEED_PIN = 11

# Hardware configuration
# Motor tuples (extend pin, retract pin)
MOTOR1_PINS = (12, 13)
MOTOR2_PINS = (14, 15)
motor_pins = [MOTOR1_PINS, MOTOR2_PINS]

# LED pins
LED1_PIN = 2
LED2_PIN = 3
led_pins = [LED1_PIN, LED2_PIN]

# Segment constants
NUM_SEGMENTS = 2
DEFAULT_SEGMENT_STATE = [0, 0]

# Time constants
DEFAULT_DELAY = 0.5  # seconds
DANCE_DELAY = 0.01   # seconds
POLLING_DELAY = 0.1  # seconds

# RTC constants
DEFAULT_YEAR = 1970
DEFAULT_MONTH = 1
DEFAULT_DAY = 1
DEFAULT_WEEKDAY = 0
DEFAULT_SUBSECONDS = 0

# Configuration file
CONFIG_FILE = "digit.json"

# Display constants
FIRST_DIGIT_POS = 0
SECOND_DIGIT_POS = 1
TENS_OFFSET = 0
ONES_OFFSET = 2  # Offset for minutes position
TWELVE_HOUR_BLANK = 'F'  # Character to display for blank first digit in 12-hour format

class Motoractuator:
    def __init__(self, speedPin, cwPin, acwPin):
        self.speed = PWM(Pin(speedPin))
        self.speed.freq(MOTOR_PWM_FREQUENCY)
        self.cw = Pin(cwPin, Pin.OUT)
        self.ccw = Pin(acwPin, Pin.OUT)
        self.stop()
    
    def extend(self, motor_speed, wait):
        # try/except block needed as an exception may be thrown without stopping the motor
        try:
            self.speed.duty_u16(int((motor_speed/100)*MAX_DUTY_CYCLE))
            self.cw.on()
            time.sleep(wait)
        except Exception as e:
            print(f"extend error: {e}")
        finally:
            self.stop()
    
    def retract(self, motor_speed, wait):
        # try/except block needed as an exception may be thrown without stopping the motor
        try:
            self.speed.duty_u16(int((motor_speed/100)*MAX_DUTY_CYCLE))
            self.ccw.on()
            time.sleep(wait)
        except Exception as e:
            print(f"retract error: {e}")
        finally:
            self.stop()
    
    def stop(self):
        self.speed.duty_u16(0)
        self.cw.off()
        self.ccw.off()

class DigitColons:
    # Default values for configuration
    DEFAULT_MOTOR_SPEED = 50  # 50% speed
    DEFAULT_WAIT_TIME = 0.02  # 20ms
    DEFAULT_DIGIT = 0
    DEFAULT_TEST_DIGIT = 0
    
    def __init__(self, led_pins, percentLED_brightness, motor_pins):
        self.leds = []
        for i in range(NUM_SEGMENTS):
            led = PWM(Pin(led_pins[i]))
            led.freq(LED_PWM_FREQUENCY)
            led.duty_u16(0)
            self.leds.append(led)
        self.conf = Config(CONFIG_FILE)
        self._previousDigitArray = DEFAULT_SEGMENT_STATE.copy()
        try:
            self.rtc = RTC()
            current = self.conf.read("previous", default=DEFAULT_SEGMENT_STATE)
            percentLED_brightness = float(self.conf.read("brightness", default=LED_DEFAULT_BRIGHTNESS))
            self._brightness = int(percentLED_brightness*MAX_BRIGHTNESS)
            self._previousDigitArray = self.conf.read("previous", default=DEFAULT_SEGMENT_STATE)
            self._motorspeed = int(self.conf.read("speed", default=self.DEFAULT_MOTOR_SPEED))
            self._waitTime = float(self.conf.read("wait", default=self.DEFAULT_WAIT_TIME))
            self._digit = int(self.conf.read("digit", default=self.DEFAULT_DIGIT))
            self._testDigit = int(self.conf.read("alien", default=self.DEFAULT_TEST_DIGIT))
        except Exception as e:
            print(f"Error loading configuration: {e}")
            self._brightness = int(LED_DEFAULT_BRIGHTNESS * MAX_BRIGHTNESS)
            self._motorspeed = self.DEFAULT_MOTOR_SPEED
            self._waitTime = self.DEFAULT_WAIT_TIME
            self._digit = self.DEFAULT_DIGIT
            self._testDigit = self.DEFAULT_TEST_DIGIT
            
        self.actuators = []
        for motor in motor_pins:
            m = Motoractuator(MOTOR_SPEED_PIN, motor[0], motor[1])
            m.stop()
            self.actuators.append(m)

        time.sleep(DEFAULT_DELAY)
        self.set_digit(current or DEFAULT_SEGMENT_STATE)
    
    def __del__(self):
        for led in self.leds:
            led.duty_u16(0)
        self.conf.__del__()

    @property
    def testdigit(self):
        return self._testDigit
    
    @testdigit.setter
    def testdigit(self, test):
        self._testDigit = test
        self.conf.write("alien", test)
    
    @property
    def speed(self):
        return self._motorspeed

    @speed.setter
    def speed(self, speed):
        self._motorspeed = speed
        self.conf.write("speed", int(speed))
    
    @property
    def wait(self):
        return self._waitTime
    
    @wait.setter
    def wait(self, wt):
        self._waitTime = wt
        self.conf.write("wait", wt)
    
    @property
    def brightness(self):
        return self._brightness
    
    @brightness.setter
    def brightness(self, b):
        self._brightness = int(b*MAX_BRIGHTNESS)
        self.conf.write("brightness", b)
        for i in range(NUM_SEGMENTS):
            if 1 == self._previousDigitArray[i]:
                self.leds[i].duty_u16(self._brightness)

    def getDigitArray(self, val):
        a = [0] * NUM_SEGMENTS
        for i in range(NUM_SEGMENTS):
            a[i] = (val & (0x01 << i)) >> i
        return a
    
    def extendSegment(self, seg):
        if(0 == self._previousDigitArray[seg]):
            self.actuators[seg].extend(self._motorspeed, self._waitTime)
            self.leds[seg].duty_u16(self._brightness)
        self._previousDigitArray[seg] = 1
        self.setPreviousDigitArray(self._previousDigitArray)
        return 1

    def retractSegment(self, seg):
        if(1 == self._previousDigitArray[seg]):
            self.actuators[seg].retract(self._motorspeed, self._waitTime)
            self.leds[seg].duty_u16(0)
        self._previousDigitArray[seg] = 0
        self.setPreviousDigitArray(self._previousDigitArray)
        return 1

    def set_digit(self, digitArray):       
        actuatorMoves = 0
        for i in range(NUM_SEGMENTS):
            if (1 == digitArray[i]) and (0 == self._previousDigitArray[i]):
                self.actuators[i].extend(self._motorspeed, self._waitTime)
                self.leds[i].duty_u16(self._brightness)
                actuatorMoves += 1
            
            if (1 == digitArray[i]) and (1 == self._previousDigitArray[i]):
                self.leds[i].duty_u16(self._brightness)

            if (0 == digitArray[i]) and (1 == self._previousDigitArray[i]):
                self.leds[i].duty_u16(0)
                self.actuators[i].retract(self._motorspeed, self._waitTime)
                actuatorMoves += 1

        self.setPreviousDigitArray(digitArray)
        return actuatorMoves

    def setPreviousDigitArray(self, digitArray):
        self.conf.write('previous', digitArray)
        for i in range(NUM_SEGMENTS):
            self._previousDigitArray[i] = digitArray[i]

    def dance(self):
        actuatorMoves = 0
        for seg in range(NUM_SEGMENTS):
            self.extendSegment(seg)
            time.sleep(DANCE_DELAY)
            actuatorMoves += 1
        for seg in range(NUM_SEGMENTS):
            self.retractSegment(seg)
            time.sleep(DANCE_DELAY)
            actuatorMoves += 1
        return actuatorMoves

    def syncTime(self, h, m, s):
        # time tuple = [year, month, day, weekday, hours, minutes, seconds, subseconds]
        self.rtc.datetime((DEFAULT_YEAR, DEFAULT_MONTH, DEFAULT_DAY, 
                          DEFAULT_WEEKDAY, h, m, s, DEFAULT_SUBSECONDS))
    
    # This method is used to format 12 or 24 hour time
    # parameter 'twelveHour' is a boolean value
    # time tuple = [year, month, day, weekday, hours, minutes, seconds, subseconds]
    def setTimeDisplay(self, twelveHour):
        ready = False
        while not ready:
            t = self.rtc.datetime()
            if t[6]%10 == self._digit:
                ready = True
            time.sleep(POLLING_DELAY)
        
        d = '0'
        if self._digit >= TENS_OFFSET and self._digit < SECOND_DIGIT_POS:
            a = '{0:02}'.format(t[4])  # Format hours as 2 digits
            d = a[self._digit]
        else:
            a = '{0:02}'.format(t[5])  # Format minutes as 2 digits
            d = a[self._digit - ONES_OFFSET]

        # In 12-hour format, blank the first digit if it's 0 (e.g. "01" becomes " 1")
        if twelveHour and d == '0' and self._digit == FIRST_DIGIT_POS:
            d = TWELVE_HOUR_BLANK
        
        v = uartCommand.digitValue
        self.set_digit(self.getDigitArray(v[int(d, 16) if d.isalpha() else int(d)]))

# Example usage:
def main():
    # User input options
    INPUT_QUIT = 'q'
    INPUT_DANCE = 'a'
    INPUT_BRIGHTNESS = 'b'
    INPUT_DIGIT = 'd'
    INPUT_EXTEND = 'e'
    INPUT_MOTOR_SPEED = 'm'
    INPUT_WAIT_TIME = 'w'
    INPUT_RETRACT = 'r'
    
    BRIGHTNESS_SCALE = 10.0  # Divide by 10 for percentage
    WAIT_TIME_SCALE = 100.0  # Divide by 100 for seconds
    
    d = DigitColons(led_pins, LED_DEFAULT_BRIGHTNESS, motor_pins)
    
    while True:
        seg = input("Enter \n\t(d)igit (d0-2)\n\t(b)rightness\n\t(e)xtend segment (e0-e1)\n\t(t)ime\n\t(r)etract segment (r0-r1)\n\t(m)otor speed\n\t(w)ait time\n\t(q)uit\n\t>:")
        if seg == INPUT_QUIT:
            break
        elif seg[0] == INPUT_DANCE:
            actuatorMoves = d.dance()
        elif seg[0] == INPUT_BRIGHTNESS:
            b = int(seg[1])
            print(f"set_brightness({b})")
            d.brightness = b / BRIGHTNESS_SCALE  # 0-9, 9 being the brightest
        elif seg[0] == INPUT_DIGIT:
            a = commandHelper().decodeHex(value=seg[1])
            digitArray = d.getDigitArray(a)
            print(f"digit={a} array={digitArray}")
            actuatorMoves = d.set_digit(digitArray)
            time.sleep(actuatorMoves * d._waitTime)
        elif seg[0] == INPUT_EXTEND:
            i = int(seg[1])
            print(f"set_digit(0x{i:02x})")
            actuatorMoves = d.extendSegment(i)
            time.sleep(actuatorMoves * d._waitTime)
        elif seg[0] == INPUT_MOTOR_SPEED:
            i = int(seg[1:])
            print(f"set_motor_speed({i})")
            d.speed = i
            print(f"_motorspeed={d._motorspeed}")
        elif seg[0] == INPUT_WAIT_TIME:
            i = int(seg[1:])
            print(f"set_wait_time({i})")
            d.wait = i / WAIT_TIME_SCALE
        elif seg[0] == INPUT_RETRACT:
            i = int(seg[1])
            print(f"set_digit(0x{i:02x})")
            actuatorMoves = d.retractSegment(i)
            time.sleep(actuatorMoves * d._waitTime)
        else:
            print("Invalid input")
    d.__del__()

if __name__ == "__main__":
    main()