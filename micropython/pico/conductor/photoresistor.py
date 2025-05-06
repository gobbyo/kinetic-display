from machine import Pin, ADC
import time

class Photoresistor:
    """
    A class for reading and processing light level data from a photoresistor sensor.
    Provides automatic calibration and scaling of values to a configurable range.
    """
    
    def __init__(self, pin, min_value=0, max_value=65535, output_scale=10):
        """
        Initialize the photoresistor.
        
        Args:
            pin: GPIO pin number where the photoresistor is connected
            min_value: Minimum expected analog reading (default 0)
            max_value: Maximum expected analog reading (default 65535)
            output_scale: Scale of the output value range (default 1-10)
        """
        self.adc = ADC(Pin(pin))
        self.light_level = 0
        self.max_reading = max_value
        self.min_reading = min_value
        self.output_scale = output_scale
        self.calibration_samples = []
        self.is_calibrated = False
    
    def read_raw(self):
        """
        Read the raw ADC value from the photoresistor.
        
        Returns:
            int: Raw ADC reading (0-65535)
        """
        try:
            return self.adc.read_u16()
        except Exception as e:
            print(f"Error reading from ADC: {e}")
            return 0
    
    def calibrate(self, num_samples=10, delay_ms=100):
        """
        Auto-calibrate the sensor by taking multiple readings to determine
        minimum and maximum values.
        
        Args:
            num_samples: Number of samples to take for calibration
            delay_ms: Delay between samples in milliseconds
        
        Returns:
            tuple: (min_value, max_value) determined during calibration
        """
        print("Calibrating photoresistor...")
        self.calibration_samples = []
        
        for i in range(num_samples):
            self.calibration_samples.append(self.read_raw())
            time.sleep_ms(delay_ms)
        
        if len(self.calibration_samples) > 0:
            self.min_reading = min(self.calibration_samples)
            self.max_reading = max(self.calibration_samples)
            
            # Ensure we have a meaningful range
            if self.max_reading - self.min_reading < 100:
                # If range is too small, use default values but add offset
                current_value = sum(self.calibration_samples) // len(self.calibration_samples)
                self.min_reading = max(0, current_value - 5000)
                self.max_reading = min(65535, current_value + 5000)
            
            self.is_calibrated = True
            print(f"Calibrated: min={self.min_reading}, max={self.max_reading}")
            return (self.min_reading, self.max_reading)
        return None
    
    def read(self):
        """
        Read the photoresistor value and convert it to the configured scale (default 1-10).
        
        Returns:
            int: Scaled light level (1 to output_scale)
        """
        input_range = self.max_reading - self.min_reading
        if input_range <= 0:  # Avoid division by zero
            input_range = 1
            
        raw_value = self.read_raw()
        adjusted_value = raw_value - self.min_reading
        
        # Ensure adjusted value is at least 1
        if adjusted_value <= 0:
            adjusted_value = 1
            
        # Scale to desired output range (1 to output_scale)
        self.light_level = int((adjusted_value / input_range) * self.output_scale)
        
        # Ensure output is within bounds
        if self.light_level >= self.output_scale:
            self.light_level = self.output_scale - 1
        elif self.light_level <= 0:
            self.light_level = 1
            
        return self.light_level
        
    def get_percentage(self):
        """
        Get the current light level as a percentage (0-100%).
        
        Returns:
            int: Light level as a percentage
        """
        raw = self.read_raw()
        if self.max_reading == self.min_reading:
            return 0
            
        percentage = ((raw - self.min_reading) / (self.max_reading - self.min_reading)) * 100
        return max(0, min(100, int(percentage)))

#Example usage:
def main():
    # Initialize photoresistor on pin 28
    light_sensor = Photoresistor(28)
    
    # Auto-calibrate (optional)
    light_sensor.calibrate()
    
    # Monitor light levels
    while True:
        # Read the value from the photoresistor (1-9 scale)
        level = light_sensor.read()
        percentage = light_sensor.get_percentage()
        
        print(f"Light level: {level}/9 ({percentage}%)")
        time.sleep(1)

if __name__ == "__main__":
    main()