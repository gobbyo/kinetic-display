from machine import Pin
import dht
import time

# See Kinetic Display main-controller schematic diagram for pinout
dhtPin = 27 # GPIO pin for DHT sensor
dhtPowerpin = 16  # GPIO pin for powering the DHT sensor

def main():
    dhtpower = Pin(dhtPowerpin, Pin.OUT)
    dhtsensor = dht.DHT22(Pin(dhtPin))

    while True:
        dhtpower.on()  # Power on the DHT sensor
        time.sleep(1.5)  # Wait for the sensor to stabilize
        try:
            # Measure temperature and humidity
            dhtsensor.measure()
            temperature = dhtsensor.temperature()
            humidity = dhtsensor.humidity()

            # Print the results
            print(f"Temperature: {temperature}°C, Humidity: {humidity}%")
        except OSError as e:
            print("Failed to read sensor data:", e)
        finally:
            dhtpower.off()
            time.sleep(1) # Wait before the next reading


if __name__ == "__main__":
    main()