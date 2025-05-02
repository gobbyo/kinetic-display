from machine import Pin, PWM, RTC
from common.uart_protocol import commandHelper, uartCommand
import time
from common.config import Config

# Constants
LED_BRIGHTNESS_DEFAULT = 0.4
LED_MAX_BRIGHTNESS = 10922 # 1/6th of 65535
MOTOR_SPEED_PIN = 11
PWM_FREQUENCY = 50
LED_PWM_FREQUENCY = 1000
MOTOR_SPEED_MAX = 100
WAIT_TIME_DEFAULT = 0.02
RTC_YEAR = 2000
RTC_MONTH = 1
RTC_DAY = 1
RTC_WEEKDAY = 0
RTC_SUBSECONDS = 0

# Motor tuples (extend pin, retract pin)
motor1 = (12, 13)
motor2 = (14, 15)
motor_pins = [motor1, motor2]

# LED pins
led_pins = [2, 3]

class Motoractuator:
    def __init__(self, speedPin, cwPin, acwPin):
        self.speed = PWM(Pin(speedPin))
        self.speed.freq(PWM_FREQUENCY)
        self.cw = Pin(cwPin, Pin.OUT)
        self.ccw = Pin(acwPin, Pin.OUT)
        self.stop()
    
    def extend(self, motor_speed, wait):
        try:
            self.speed.duty_u16(int((motor_speed / MOTOR_SPEED_MAX) * LED_MAX_BRIGHTNESS))
            self.cw.on()
            time.sleep(wait)
        except Exception as e:
            print(f"extend error: {e}")
        finally:
            self.stop()
    
    def retract(self, motor_speed, wait):
        try:
            self.speed.duty_u16(int((motor_speed / MOTOR_SPEED_MAX) * LED_MAX_BRIGHTNESS))
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

class Digit_Colons:
    def __init__(self, led_pins, percentLED_brightness, motor_pins):
        self.leds = []
        for pin in led_pins:
            led = PWM(Pin(pin))
            led.freq(LED_PWM_FREQUENCY)
            led.duty_u16(0)
            self.leds.append(led)
        self.config = Config("digit.json")
        self.previous_digit_array = [0, 0]
        try:
            self.rtc = RTC()
            current = self.config.read("previous") or [0, 0]
            percent_led_brightness = float(self.config.read("brightness") or LED_BRIGHTNESS_DEFAULT)
            self.brightness = int(percent_led_brightness * LED_MAX_BRIGHTNESS)
            self.previous_digit_array = current
            self.motor_speed = int(self.config.read("motorspeed") or MOTOR_SPEED_MAX)
            self.wait_time = float(self.config.read("wait") or WAIT_TIME_DEFAULT)
            self.digit = int(self.config.read("digit") or 0)
            self.test_digit = int(self.config.read("alien") or 0)
        except Exception as e:
            print(f"Error loading configuration: {e}")
        self.actuators = []
        for motor in motor_pins:
            m = Motoractuator(MOTOR_SPEED_PIN, motor[0], motor[1])
            m.stop()
            self.actuators.append(m)

        time.sleep(0.5)
        self.set_digit(current)
    
    def __del__(self):
        try:
            for led in self.leds:
                led.duty_u16(0)
            self.config.__del__()
        except Exception as e:
            print(f"Error during cleanup: {e}")

    @property
    def testdigit(self):
        return self.test_digit
    
    @testdigit.setter
    def testdigit(self, test):
        self.test_digit = test
        self.config.write("alien", test)
    
    @property
    def speed(self):
        return self.motor_speed

    @speed.setter
    def speed(self, speed):
        self.motor_speed = speed
        self.config.write("speed", int(speed))
    
    @property
    def wait(self):
        return self.wait_time
    
    @wait.setter
    def wait(self, wt):
        self.wait_time = wt
        self.config.write("wait", wt)
    
    @property
    def brightness(self):
        return self.brightness
    
    @brightness.setter
    def brightness(self, b):
        self.brightness = int(b * LED_MAX_BRIGHTNESS)
        self.config.write("brightness", b)
        for i in range(2):
            if self.previous_digit_array[i] == 1:
                self.leds[i].duty_u16(self.brightness)

    def getDigitArray(self, val):
        a = [0, 0]
        for i in range(len(a)):
            a[i] = (val & (0x01 << i)) >> i
        return a
    
    def extend_segment(self, seg):
        if not 0 <= seg < len(self.previous_digit_array):
            print(f"Error: Invalid segment index {seg}")
            return 0

        if self.previous_digit_array[seg] == 0:
            try:
                self.actuators[seg].extend(self.motor_speed, self.wait_time)
                self.leds[seg].duty_u16(self.brightness)
                self.previous_digit_array[seg] = 1
                self.setPreviousDigitArray(self.previous_digit_array)
            except Exception as e:
                print(f"Error extending segment {seg}: {e}")
        return 1

    def retract_segment(self, seg):
        if not 0 <= seg < len(self.previous_digit_array):
            print(f"Error: Invalid segment index {seg}")
            return 0

        if self.previous_digit_array[seg] == 1:
            try:
                self.actuators[seg].retract(self.motor_speed, self.wait_time)
                self.leds[seg].duty_u16(0)
                self.previous_digit_array[seg] = 0
                self.setPreviousDigitArray(self.previous_digit_array)
            except Exception as e:
                print(f"Error retracting segment {seg}: {e}")
        return 1

    def set_digit(self, digitArray):
        actuatorMoves = 0
        for i in range(2):
            if (digitArray[i] == 1 and self.previous_digit_array[i] == 0):
                self.actuators[i].extend(self.motor_speed, self.wait_time)
                self.leds[i].duty_u16(self.brightness)
                actuatorMoves += 1
            elif (digitArray[i] == 0 and self.previous_digit_array[i] == 1):
                self.actuators[i].retract(self.motor_speed, self.wait_time)
                self.leds[i].duty_u16(0)
                actuatorMoves += 1
        self.setPreviousDigitArray(digitArray)
        return actuatorMoves

    def setPreviousDigitArray(self, digitArray):
        self.config.write('previous', digitArray)
        self.previous_digit_array = digitArray

    def dance(self):
        actuatorMoves = 0
        for seg in range(2):
            self.extend_segment(seg)
            time.sleep(0.01)
            actuatorMoves += 1
        for seg in range(2):
            self.retract_segment(seg)
            time.sleep(0.01)
            actuatorMoves += 1
        return actuatorMoves

    def syncTime(self, h, m, s):
        self.rtc.datetime((RTC_YEAR, RTC_MONTH, RTC_DAY, RTC_WEEKDAY, h, m, s, RTC_SUBSECONDS))
    
    def setTimeDisplay(self, twelveHour):
        max_attempts = 100
        attempts = 0

        while attempts < max_attempts:
            t = self.rtc.datetime()
            if t[6] % 10 == self.digit:
                break
            time.sleep(0.1)
            attempts += 1

        if attempts == max_attempts:
            print("Warning: setTimeDisplay reached maximum attempts without success.")
            return

        d = '0'
        if self.digit < 2:
            d = '{0:02}'.format(t[4])[self.digit]
        else:
            d = '{0:02}'.format(t[5])[self.digit - 2]

        if twelveHour and d == '0' and self.digit == 0:
            d = 'F'

        cmd = uartCommand("default")
        self.set_digit(self.getDigitArray(cmd.digitValue[int(d)]))

#Example usage:
def main():
    d = Digit_Colons(led_pins, 0.4, motor_pins)
    
    while True:
        seg = input("Enter \n\t(d)igit (d0-2)\n\t(b)rightness\n\t(e)xtend segment (e0-e1)\n\t(t)ime\n\t(r)etract segment (r0-r1)\n\t(m)otor speed\n\t(w)ait time\n\t(q)uit\n\t>:")
        if seg == 'q':
            break
        elif seg[0] == 'a':
            actuatorMoves = d.dance()
        elif seg[0] == 'b':
            b = int(seg[1])
            print("set_brightness({0})".format(b))
            d.brightness = b/10 # 0-9, 9 being the brightest
        elif seg[0] == 'd':
            a = commandHelper().decodeHex(value=seg[1])
            digitArray = d.getDigitArray(a)
            print("digit={0} array={1}".format(a, digitArray))
            actuatorMoves = d.set_digit(digitArray)
            time.sleep(actuatorMoves * d._waitTime)
        elif seg[0] == 'e':
            i = int(seg[1])
            print("set_digit(0x{0:02x})".format(i))
            actuatorMoves = d.extend_segment(i)
            time.sleep(actuatorMoves * d._waitTime)
        elif seg[0] == 'm':
            i = int(seg[1:])
            print("set_motor_speed({0})".format(i))
            d.speed = i
            print("_motorspeed={0}".format(d._motorspeed))
        elif seg[0] == 'w':
            i = int(seg[1:])
            print("set_wait_time({0})".format(i))
            d.wait = i/100
        elif seg[0] == 'r':
            i = int(seg[1])
            print("set_digit(0x{0:02x})".format(i))
            actuatorMoves = d.retract_segment(i)
            time.sleep(actuatorMoves * d._waitTime)
        else:
            print("Invalid input")
    d.__del__()

if __name__ == "__main__":
    main()