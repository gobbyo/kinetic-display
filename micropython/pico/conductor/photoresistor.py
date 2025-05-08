from machine import Pin, ADC
import time

# Constants for photoresistor readings
MIN_ADC_VALUE = 0         # Minimum ADC reading (0%)
MAX_ADC_VALUE = 65767     # Maximum ADC reading (100%)
LIGHT_SCALE_FACTOR = 10   # Factor to scale light level to 0-10 range
MIN_LIGHT_LEVEL = 1       # Minimum light level to report
MAX_LIGHT_LEVEL = 9       # Maximum light level to report
MIN_VALID_READING = 1     # Minimum valid reading after subtracting minimum

# Constants for example usage
DEFAULT_PHOTORESISTOR_PIN = 28  # Default pin for photoresistor in example
READING_INTERVAL = 1            # Time between readings in seconds

class photoresistor():
    def __init__(self, pin):
        self.photoRes = ADC(Pin(pin))
        self.light = 0
        self.max = MAX_ADC_VALUE  # 100%
        self.min = MIN_ADC_VALUE  # 0%

    def read(self):
        range_value = self.max - self.min
        k = self.photoRes.read_u16()
        k = k - self.min
        if k <= 0:
            k = MIN_VALID_READING
        self.light = int((k/range_value) * LIGHT_SCALE_FACTOR)
        if self.light >= LIGHT_SCALE_FACTOR:
            self.light = MAX_LIGHT_LEVEL
        elif self.light <= 0:
            self.light = MIN_LIGHT_LEVEL
        return self.light

# Example usage:
def main():
    light = photoresistor(DEFAULT_PHOTORESISTOR_PIN)
    while True:
        # Read the value from the photoresistor
        print("Light level: {0}".format(light.read()))
        time.sleep(READING_INTERVAL)

if __name__ == "__main__":
    main()