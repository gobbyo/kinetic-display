from machine import Pin, PWM
import time

led_pins = [2,3,6,7,8,9,28]

b = 0.5
brightness = int(b*65536)

for p in led_pins:
    LED = PWM(Pin(p))
    LED.freq(1000)
    LED.duty_u16(brightness)
    time.sleep(1)
    LED.duty_u16(0)

print("Done")
