from machine import Pin
import time

hall = Pin(13, Pin.IN, Pin.PULL_UP)

prev = 0

while True:
    val = hall.value()
    if prev != val:
        print("Hall sensor changed to: {0}", val)
        prev = val
    time.sleep(0.1)