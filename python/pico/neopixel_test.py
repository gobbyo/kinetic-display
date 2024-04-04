from machine import Pin
import neopixel
import time

rp2040zeroLED_pin = 16
color = [(255,255,255),(255,0,0),(0,255,0),(0,0,255),(0,0,0)]

np = neopixel.NeoPixel(Pin(rp2040zeroLED_pin), 8)

for i in range(len(color)):
    np[0] = color[i]
    np.write()
    time.sleep(1)

p = Pin(25, Pin.OUT)
p.on()
time.sleep(1)
p.off()