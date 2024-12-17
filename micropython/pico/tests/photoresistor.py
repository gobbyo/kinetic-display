from machine import Pin, ADC
import time

class photoresistor():
    _max = 0
    _min = 0

    @property
    def min_1k(self):
        return 60000

    @property
    def max(self):
        return self._max
    
    @max.setter
    def max(self,value):
        if value > self._max:
            self._max = value
    
    @property
    def min(self):
        return self._min

    @min.setter
    def min(self,value):
        if value < self._min:
            self._min = value
    
    def __init__(self, pin):
        self.photoRes = ADC(Pin(pin))
        self.light = 0
        self._max = 0
        self._min = 65000

    def read(self):
        k = self.photoRes.read_u16()
        self.max = k
        self.min = k

        print("raw reading {0}".format(k))
        return k

def main():
    light = photoresistor(28)

    while True:
        # Read the value from the photoresistor
        k = light.read()
        print("Current level: {0}".format(k))
        print(" 1k: {0}".format(k-light.min_1k))
        print(" max: {0}, min: {1}".format(light.max, light.min))
        time.sleep(1)

if __name__ == "__main__":
    main() 