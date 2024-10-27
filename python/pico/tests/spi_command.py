import digit
from machine import Pin, SPI
import time

def main():
    try:
        # construct a SPI bus on the given pins
        # polarity is the idle state of SCK
        # phase=0 means sample on the first edge of SCK, phase=1 means the second
        spi = SPI(0, baudrate=400000)
        SPRx = Pin(3, mode=Pin.OUT, value=1)
        while True:
            i = 0
            for seg in digit.segnum:
                print('---Digit {0}---'.format(digit.segprint[i]))
                try:
                    SPRx(0) # select peripheral
                    print('seg({0})'.format(seg))
                    spi.write(bytearray('{0}'.format(seg), 'utf-8')) # write to MOSI
                finally:
                    SPRx(1) # deselect peripheral
                    time.sleep(3)
                i += 1
            time.sleep(10)
        
        spi.deinit()            # turn off the SPI bus

    except KeyboardInterrupt:
        pass

if __name__ == '__main__':
    main()