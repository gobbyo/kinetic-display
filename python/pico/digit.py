from machine import Pin, PWM
import time

pause = 1
waitTime = 0.2
speed = 75

pwmPIN=11
motor1extendPin=12 
motor1retractPin=13
motor2extendPin=14
motor2retractPin=15
motor3extendPin=16
motor3retractPin=17
motor4extendPin=18
motor4retractPin=19
motor5extendPin=20
motor5retractPin=21
motor6extendPin=22
motor6retractPin=26
motor7extendPin=27
motor7retractPin=10

_percentBrightness = .30
_brightness = int(_percentBrightness*65536)

led_a_pin = 4
led_b_pin = 5
led_c_pin = 6
led_d_pin = 7
led_e_pin = 8
led_f_pin = 9
led_g_pin = 28

class motoractuator:
    def __init__(self, speedGP, cwGP, acwGP):
        self.speed = PWM(Pin(speedGP))
        self.speed.freq(50)
        self.cw = Pin(cwGP, Pin.OUT)
        self.acw = Pin(acwGP, Pin.OUT)
    
    def extend(self, speed):
        self.speed.duty_u16(int((speed/100)*65536))
        self.cw.on()
        self.acw.off()
        time.sleep(waitTime)
        self.stop()
        print("extend")
    
    def retract(self, speed):
        self.speed.duty_u16(int((speed/100)*65536))
        self.cw.off()
        self.acw.on()
        time.sleep(waitTime)
        self.stop()
        print("retract")
    
    def stop(self):
        self.speed.duty_u16(0)
        self.cw.off()
        self.acw.off()
        print("stop")

_previousDigitArray = [0,0,0,0,0,0,0]
    
# 0 = 	0011 1111   0x3F
# 1 =	0000 0110   0x06
# 2 =	0101 1011   0x5B
# 3 =	0100 1111   0x4F
# 4 =	0110 0110   0x66
# 5 =	0110 1101   0x6D
# 6 =	0111 1101   0x7D
# 7 =	0000 0111   0x07
# 8 =   0111 1111   0x7F
# 9 =   0110 0111   0x67
# A =   0110 0011   0x63  #degrees
# B =   0101 1100   0x5C  #percent
# C =   0011 1001   0x39  #celcius
# D =   0111 0001   0x71  #farhenheit
# E =   0000 0000   0x00  #clear
# F =   1000 0000   0x00  #ignore
_segnum = [0x3F,0x06,0x5B,0x4F,0x66,0x6D,0x7D,0x07,0x7F,0x67,0x63,0x5C,0x39,0x71,0x00]
_segprint = ['0','1','2','3','4','5','6','7','8','9','A (degrees)','B (percent)','C (celcius)','D (farhenheit)','E (clear)', 'F (ignore)']

def getDigitArray(val):
    a = [0,0,0,0,0,0,0]
    i = 0
    for s in a:
        a[i] = (val & (0x01 << i)) >> i
        i += 1
    return a

def set_digit(seg, actuators, leds):
    digitArray = getDigitArray(seg)
    print("set_digit(0x{0:02x}): {1}".format(seg, digitArray))

    for i in range(0,7):
        if (1 == digitArray[i]) and (0 == _previousDigitArray[i]):
            actuators[i].extend(speed)
            print("----------")
            print("extend {0} digit {1}".format(i, digitArray))
            leds[i].duty_u16(_brightness)

        if (0 == digitArray[i]) and (1 == _previousDigitArray[i]):
            print("----------")
            print("retract {0} digit {1}".format(i, digitArray))
            leds[i].duty_u16(0)
            actuators[i].retract(speed)

    setPreviousDigitArray(digitArray)

def setPreviousDigitArray(digitArray):
    for i in range(7):
        _previousDigitArray[i] = digitArray[i]

def main():
    leds = [PWM(Pin(led_a_pin)), PWM(Pin(led_b_pin)), PWM(Pin(led_c_pin)),  PWM(Pin(led_d_pin)),  PWM(Pin(led_e_pin)),  PWM(Pin(led_f_pin)),  PWM(Pin(led_g_pin))]
    for led in leds:
        led.freq(1000)
        led.duty_u16(0)
    actuators = [motoractuator(pwmPIN,motor1extendPin,motor1retractPin), motoractuator(pwmPIN,motor2extendPin,motor2retractPin), motoractuator(pwmPIN,motor3extendPin,motor3retractPin), motoractuator(pwmPIN,motor4extendPin,motor4retractPin), motoractuator(pwmPIN,motor5extendPin,motor5retractPin), motoractuator(pwmPIN,motor6extendPin,motor6retractPin), motoractuator(pwmPIN,motor7extendPin,motor7retractPin)]
    for actuator in actuators:
        actuator.stop()

    while True:
        i = 0
        for seg in _segnum:
            print('---Digit {0}---'.format(_segprint[i]))
            set_digit(seg,actuators,leds)
            time.sleep(pause)
            i += 1
        time.sleep(2)

if __name__ == "__main__":
    main()