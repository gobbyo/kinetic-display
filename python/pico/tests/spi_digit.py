import digit
from machine import Pin, SPI
import time

def decodeHex(value):
    returnVal = value
    if value == "A":
        returnVal = 10
    elif value == "B":
        returnVal = 11
    elif value == "C":
        returnVal = 12
    elif value == "D":
        returnVal = 13
    elif value == "E":
        returnVal = 14
    elif value == "F":
        returnVal = 15
    return returnVal

def main():
    try:
        # construct a SPI bus on the given pins
        # polarity is the idle state of SCK
        # phase=0 means sample on the first edge of SCK, phase=1 means the second
        spi = SPI(0, baudrate=400000)
        SPRx = Pin(3, mode=Pin.OUT, value=1)
        d = digit.Digit(digit.led_pins, 0.5, digit.motor_pins, 75)
        while True:
            try:
                SPRx(0)
                seg = bytearray(4)      # create a buffer
                spi.readinto(seg)
                num = '{0}'.format(seg.decode('utf-8'))
                if(num[0] != '\0'):
                    print('decodeHex({0}), len({1})'.format(num,len(num)))
                    #d.set_digit(digit.segnum[int(s,16)])
            finally:
                SPRx(1)
                time.sleep(1)
        
        spi.deinit()            # turn off the SPI bus

    except KeyboardInterrupt:
        pass

if __name__ == '__main__':
    main()