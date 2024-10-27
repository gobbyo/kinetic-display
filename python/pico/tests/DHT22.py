from machine import Pin
import time

class SensorInterface:
    def measure(self):
        raise NotImplementedError

    def get_temperature(self):
        raise NotImplementedError

    def get_humidity(self):
        raise NotImplementedError

class DHT22(SensorInterface):
    def __init__(self, data_pin):
        print("DHT22 sensor initialized")
        self.data_pin = Pin(data_pin, Pin.IN, Pin.PULL_UP)
        self.temperature = None
        self.humidity = None

    def measure(self):
        try:
            print("Measuring temperature and humidity")
            self._read_sensor()
        except Exception as e:
            print(f"Error during measurement: {e}")

    def get_temperature(self):
        return self.temperature

    def get_humidity(self):
        return self.humidity

    def _read_sensor(self):
        # DHT22 sensor reading logic
        self.data_pin.init(Pin.OUT)
        self.data_pin.value(0)
        time.sleep_ms(20)
        self.data_pin.value(1)
        time.sleep_us(40)
        self.data_pin.init(Pin.IN)

        print("Waiting for sensor response")
        while self.data_pin.value() == 1:
            pass

        while self.data_pin.value() == 0:
            pass

        while self.data_pin.value() == 1:
            pass

        print("Reading sensor data")
        data = []
        for i in range(40):
            while self.data_pin.value() == 0:
                pass
            length = 0
            while self.data_pin.value() == 1:
                length += 1
                time.sleep_us(1)
            if length > 50:
                data.append(1)
            else:
                data.append(0)

        humidity_bits = data[0:16]
        temperature_bits = data[16:32]
        checksum_bits = data[32:40]

        humidity = 0
        for i in range(16):
            humidity += humidity_bits[i] * 2 ** (15 - i)

        temperature = 0
        for i in range(16):
            temperature += temperature_bits[i] * 2 ** (15 - i)

        checksum = 0
        for i in range(8):
            checksum += checksum_bits[i] * 2 ** (7 - i)

        if checksum == ((humidity >> 8) + (humidity & 0xFF) + (temperature >> 8) + (temperature & 0xFF)) & 0xFF:
            self.humidity = humidity / 10.0
            self.temperature = temperature / 10.0
        else:
            raise ValueError("Checksum does not match")

def main():
    dht22_sensor = DHT22(data_pin=26)
    dht22_sensor.measure()
    print(f"Temperature: {dht22_sensor.get_temperature()}°C")
    print(f"Humidity: {dht22_sensor.get_humidity()}%")

# Example usage
if __name__ == "__main__":
    main()