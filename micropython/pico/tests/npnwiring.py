from machine import Pin
import time

def main():
    p = Pin(27, Pin.OUT)
    p.on()
    time.sleep(5)
    p.off()
    time.sleep(.5)
    for i in range(5):
        p.on()
        time.sleep(.1)
        p.off()
        time.sleep(.5)
    
if __name__ == "__main__":
    main()