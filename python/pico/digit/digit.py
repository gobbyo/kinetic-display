from machine import Pin, PWM, RTC
from uart_protocol import commandHelper, uartCommand
import time
from config import Config

LEDbrightness = 0.4

motorSpeedPin=11
# motor tuples (extend pin, retract pin)
motor1 = (12,13)
motor2 = (14,15)
motor3 = (16,17)
motor4 = (18,19)
motor5 = (20,21)
motor6 = (22,26)
motor7 = (27,10)
motor_pins = [motor1,motor2,motor3,motor4,motor5,motor6,motor7]
led_pins = [2,3,6,7,8,9,28]

class Motoractuator:
    def __init__(self, speedPin, cwPin, ccwPin):
        self.speed = PWM(Pin(speedPin))
        self.speed.freq(50)
        self.cw = Pin(cwPin, Pin.OUT)
        self.ccw = Pin(ccwPin, Pin.OUT)
        self.stop()
    
    def extend(self, motor_speed, waitTime):
        try:
            self.speed.duty_u16(int((motor_speed / 100) * 65536))
            self.cw.on()
            time.sleep(waitTime)
        except Exception as e:
            print(f"extend error: {e}")
        finally:
            self.stop()
            #print("extend")
    
    def retract(self, motor_speed, waitTime):
        try:
            self.speed.duty_u16(int((motor_speed / 100) * 65536))
            self.ccw.on()
            time.sleep(waitTime)
        except Exception as e:
            print(f"retract error: {e}")
        finally:
            self.stop()
            #print("retract")
    
    def stop(self):
        self.speed.duty_u16(0)
        self.cw.off()
        self.ccw.off()
        #print("stop")

class Digit:
    def __init__(self, led_pins, percentLED_brightness, motor_pins):
        self.leds = []
        self.startLED = Pin(25,Pin.OUT)
        for i in range(7):
            led = PWM(Pin(led_pins[i]))
            led.freq(1000)
            led.duty_u16(0)
            self.leds.append(led)
        self.conf = Config("digit.json")
        self._previousDigitArray = [0,0,0,0,0,0,0]
        try:
            self.rtc = RTC()
            current = self.conf.read("previous")
            percentLED_brightness = float(self.conf.read("brightness")) # 0-1, 0.5 being 50% brightness
            self._brightness = int(percentLED_brightness*65536)
            self._previousDigitArray = self.conf.read("previous")
            self._motorspeed = int(self.conf.read("motorspeed"))
            self._waitTime = float(self.conf.read("waitTime"))
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
        self._brightness = int(b*65536)
        self.conf.write("brightness", b)
        for i in range(0,7):
            if 1 == self._previousDigitArray[i]:
                self.leds[i].duty_u16(self._brightness)
                print(f"----------\nbrightness {self._brightness} seg={i}")

    def getDigitArray(self, val):
        a = [0,0,0,0,0,0,0]
        for i in range(len(a)):
            a[i] = (val & (0x01 << i)) >> i
        return a
    
    def extend_segment(self, seg):
        if(0 == self._previousDigitArray[seg]):
            self.actuators[seg].extend(self._motorspeed,self._waitTime)
            self.leds[seg].duty_u16(self._brightness)
        self._previousDigitArray[seg] = 1
        self.setPreviousDigitArray(self._previousDigitArray)
        return 1

    def retract_segment(self, seg):
        if(1 == self._previousDigitArray[seg]):
            self.actuators[seg].retract(self._motorspeed,self._waitTime)
            self.leds[seg].duty_u16(0)
        self._previousDigitArray[seg] = 0
        self.setPreviousDigitArray(self._previousDigitArray)
        return 1

    def set_digit(self, digitArray):     
        self.startLED.on()   
        actuatorMoves = 0
        print(f"set_digit: {digitArray}")
        for i in range(0,7):
            skipped = True
            if (1 == digitArray[i]) and (0 == self._previousDigitArray[i]):
                self.actuators[i].extend(self._motorspeed,self._waitTime)
                print(f"\t[1] seg {chr(i+97)} extended")
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
                self.actuators[i].retract(self._motorspeed,self._waitTime)
                actuatorMoves += 1
                skipped = False
            
            if skipped:
                print(f"\t[{self._previousDigitArray[i]}] seg {chr(i+97)} skipped")

        self.setPreviousDigitArray(digitArray)
        self.startLED.off()
        return actuatorMoves

    def setPreviousDigitArray(self, digitArray):
        self.conf.write('previous',digitArray)
        for i in range(7):
            self._previousDigitArray[i] = digitArray[i]

    def dance(self):
        self.startLED.on()
        actuatorMoves = 0
        for seg in [2,3,4,5,0,1,6]:
            self.extend_segment(seg)
            time.sleep(.01)
            actuatorMoves += 1
        for seg in [5,0,1,2,3,4,6]:
            self.retract_segment(seg)
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
            print(f"hours d={d}")
        else:
            a = '{0:02}'.format(t[5])
            d = a[self._digit - 2]
            print(f"minutes d={d}")

        if twelveHour and d == '0' and self._digit == 0:
            d = 'F'
        
        self.set_digit(self.getDigitArray(uartCommand.digitValue[int(d)]))

def main():
    d = Digit(led_pins, LEDbrightness, motor_pins)
    
    while True:
        seg = input("Enter: \n\t(d)igit (d0-d9,dA-dF)\n\t(b)rightness\n\t(e)xtend segment (e0-e6)\n\t(r)etract segment (r0-r6)\n\t(m)otor speed\n\t(w)ait time\n\t(c)ycle\n\t(t)est digit\n\t(q)uit\n\t>:")
        if seg == 'q':
            break
        elif seg[0] == 'a':
            actuatorMoves = d.dance()
        elif seg[0] == 'b':
            b = int(seg[1])
            print(f"set_brightness({b})")
            d.brightness = b/10 # 0-9, 9 being the brightest
        elif seg[0] == 'c':
            while True:
                for i in range(0,16):
                    a = commandHelper.decodeHex(i)
                    #print(f"set_digit(0x{a:02x})")
                    digitArray = d.getDigitArray(uartCommand.digitValue[a])
                    d.set_digit(digitArray)
                    time.sleep(1)
        elif seg[0] == 'd':
            a = commandHelper.decodeHex(seg[1])
            if 1 == d.testdigit:
                digitArray = d.getDigitArray(uartCommand.digitTest[a])
            else:
                digitArray = d.getDigitArray(uartCommand.digitValue[a])
            print(f"set_digit(0x{a:02x}): {digitArray}")
            actuatorMoves = d.set_digit(digitArray)
            time.sleep(actuatorMoves * d._waitTime)
        elif seg[0] == 'e':
            i = int(seg[1])
            print(f"set_digit(0x{i:02x})")
            actuatorMoves = d.extend_segment(i)
            time.sleep(actuatorMoves * d._waitTime)
        elif seg[0] == 'm':
            i = int(seg[1:])
            print(f"set_motor_speed({i})")
            d.motorspeed = i
        elif seg[0] == 'w':
            i = int(seg[1:])
            print(f"set_wait_time({i})")
            d.waitTime = i/100
        elif seg[0] == 'r':
            i = int(seg[1])
            print(f"set_digit(0x{i:02x})")
            actuatorMoves = d.retract_segment(i)
            time.sleep(actuatorMoves * d._waitTime)
        elif seg[0] == 't':
            d.dance()
        else:
            print("Invalid input")
    d.__del__()

if __name__ == "__main__":
    main()