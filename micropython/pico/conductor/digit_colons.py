from machine import Pin, PWM, RTC
from common.uart_protocol import commandHelper, uartCommand
import time
from common.config import Config

LEDbrightness = 0.4
MAX_BRIGHTNESS = 65535 * 0.14

motorSpeedPin=11
# motor tuples (extend pin, retract pin)
motor1 = (12,13)
motor2 = (14,15)
motor_pins = [motor1,motor2]
led_pins = [2,3]

class Motoractuator:
    def __init__(self, speedPin, cwPin, acwPin):
        self.speed = PWM(Pin(speedPin))
        self.speed.freq(50)
        self.cw = Pin(cwPin, Pin.OUT)
        self.ccw = Pin(acwPin, Pin.OUT)
        self.stop()
    
    def extend(self, motor_speed, wait):
        # try/except block needed as an exception may be thrown without stopping the motor
        try:
            self.speed.duty_u16(int((motor_speed/100)*65536))
            self.cw.on()
            time.sleep(wait)
        except Exception as e:
            print("extend error: {0}".format(e))
        finally:
            self.stop()
            print("extend")
    
    def retract(self, motor_speed, wait):
        # try/except block needed as an exception may be thrown without stopping the motor
        try:
            self.speed.duty_u16(int((motor_speed/100)*65536))
            self.ccw.on()
            time.sleep(wait)
        except Exception as e:
            print("retract error: {0}".format(e))
        finally:
            self.stop()
            print("retract")
    
    def stop(self):
        self.speed.duty_u16(0)
        self.cw.off()
        self.ccw.off()
        print("stop")

class DigitColons:
    def __init__(self, led_pins, percentLED_brightness, motor_pins):
        self.leds = []
        self.startLED = Pin(25,Pin.OUT)
        for i in range(2):
            led = PWM(Pin(led_pins[i]))
            led.freq(1000)
            led.duty_u16(0)
            self.leds.append(led)
        self.conf = Config("digit.json")
        self._previousDigitArray = [0,0]
        try:
            self.rtc = RTC()
            current = self.conf.read("previous")
            percentLED_brightness = float(self.conf.read("brightness")) # 0-1, 0.5 being 50% brightness
            self._brightness = int(percentLED_brightness*MAX_BRIGHTNESS)
            self._previousDigitArray = self.conf.read("previous")
            self._motorspeed = int(self.conf.read("speed"))
            self._waitTime = float(self.conf.read("wait"))
            self._digit = int(self.conf.read("digit"))
            self._testDigit = int(self.conf.read("alien"))
        finally:
            pass
        self.actuators = []
        for motor in motor_pins:
            m = Motoractuator(motorSpeedPin,motor[0],motor[1])
            m.stop()
            self.actuators.append(m)

        time.sleep(.5)
        self.set_digit(current)
    
    def __del__(self):
        for led in self.leds:
            led.duty_u16(0)
        self.startLED.off()
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
        print("speed={0}".format(self._motorspeed))
        return self._motorspeed

    @speed.setter
    def speed(self, speed):
        self._motorspeed = speed
        self.conf.write("speed", int(speed))
    
    @property
    def wait(self):
        print("wait={0}".format(self._waitTime))
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
        for i in range(2):
            if 1 == self._previousDigitArray[i]:
                self.leds[i].duty_u16(self._brightness)
                print("----------")
                print("brightness {0} seg={1}".format(self._brightness, i))

    def getDigitArray(self, val):
        a = [0,0]
        i = 0
        for s in a:
            a[i] = (val & (0x01 << i)) >> i
            i += 1
        return a
    
    def extendSegment(self, seg):
        if(0 == self._previousDigitArray[seg]):
            self.actuators[seg].extend(self._motorspeed,self._waitTime)
            self.leds[seg].duty_u16(self._brightness)
        self._previousDigitArray[seg] = 1
        self.setPreviousDigitArray(self._previousDigitArray)
        return 1

    def retractSegment(self, seg):
        if(1 == self._previousDigitArray[seg]):
            self.actuators[seg].retract(self._motorspeed,self._waitTime)
            self.leds[seg].duty_u16(0)
        self._previousDigitArray[seg] = 0
        self.setPreviousDigitArray(self._previousDigitArray)
        return 1

    def set_digit(self, digitArray):     
        self.startLED.on()   
        actuatorMoves = 0
        for i in range(2):
            if (1 == digitArray[i]) and (0 == self._previousDigitArray[i]):
                self.actuators[i].extend(self._motorspeed,self._waitTime)
                print("----------")
                print("extend {0} digit {1}".format(i, digitArray))
                self.leds[i].duty_u16(self._brightness)
                actuatorMoves += 1
            
            if (1 == digitArray[i]) and (1 == self._previousDigitArray[i]):
                self.leds[i].duty_u16(self._brightness)
                print("----------")
                print("extend {0} digit {1}".format(i, digitArray))

            if (0 == digitArray[i]) and (1 == self._previousDigitArray[i]):
                print("----------")
                print("retract {0} digit {1}".format(i, digitArray))
                self.leds[i].duty_u16(0)
                self.actuators[i].retract(self._motorspeed,self._waitTime)
                actuatorMoves += 1

        self.setPreviousDigitArray(digitArray)
        self.startLED.off()
        return actuatorMoves

    def setPreviousDigitArray(self, digitArray):
        self.conf.write('previous',digitArray)
        for i in range(2):
            self._previousDigitArray[i] = digitArray[i]

    def dance(self):
        self.startLED.on()
        actuatorMoves = 0
        for seg in range(2):
            self.extendSegment(seg)
            time.sleep(.01)
            actuatorMoves += 1
        for seg in range(2):
            self.retractSegment(seg)
            time.sleep(.01)
            actuatorMoves += 1
        self.startLED.off()
        return actuatorMoves

    def syncTime(self, h, m, s):
        # time tuple = [year, month, day, weekday, hours, minutes, seconds, subseconds]
        self.rtc.datetime((2000, 1, 1, 0, h, m, s, 0))
    
    # This method is used to format 12 or 24 hour time
    # parameter 'twelveHour' is a boolean value
    # time tuple = [year, month, day, weekday, hours, minutes, seconds, subseconds]
    def setTimeDisplay(self, twelveHour):
        ready = False
        while not ready:
            t = self.rtc.datetime()
            if t[6]%10 == self._digit:
                ready = True
            time.sleep(.1)
        
        d = '0'
        if self._digit >= 0 and self._digit < 2:
            a = '{0:02}'.format(t[4])
            d = a[self._digit]
            print("hours d={0}".format(d))
        else:
            a = '{0:02}'.format(t[5])
            d = a[self._digit - 2]
            print("minutes d={0}".format(d))

        if twelveHour and d == '0' and self._digit == 0:
            d = 'F'
        cmd = uartCommand("default")
        self.set_digit(self.getDigitArray(cmd.digitValue[int(d)]))

#Example usage:
def main():
    d = DigitColons(led_pins, LEDbrightness, motor_pins)
    
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
            actuatorMoves = d.extendSegment(i)
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
            actuatorMoves = d.retractSegment(i)
            time.sleep(actuatorMoves * d._waitTime)
        else:
            print("Invalid input")
    d.__del__()

if __name__ == "__main__":
    main()