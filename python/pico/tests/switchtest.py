from machine import Pin
import time

switch = Pin(28, Pin.IN, Pin.PULL_DOWN)

cont = True

while cont:
    if switch.value() == 1:
        print("Switch on")
    else:
        print("Switch off")
    time.sleep(1)