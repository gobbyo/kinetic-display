import dht
from machine import Pin
import time

def main():
    dhtpower = Pin(16, Pin.OUT)
    dhtpower.on()
    time.sleep(1.2)
    t = dht.DHT11(Pin(27))
    t.measure()
    temp = t.temperature()
    humid = t.humidity()
    f = '{0:02}'.format(int(round((9/5)*temp+32,0)))
    print(f"Temperature=: {f}F")
    print(f"Temperature: {t.temperature()}C")
    print(f"Humidity: {round(humid,0)}%")
    dhtpower.off()

# Example usage
if __name__ == "__main__":
    main()