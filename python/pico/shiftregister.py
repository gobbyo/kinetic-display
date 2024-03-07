from machine import Pin,PWM
import time

#shift register pins
latchpin = const(7) #RCLK default
clockpin = const(6) #SRCLK default
datapin = const(8) #SER default


class shiftreg:
    def __init__(self, latchpin, clockpin, datapin):
        self.latch = Pin(latchpin, Pin.OUT)
        self.clock = Pin(clockpin, Pin.OUT)
        self.data = Pin(datapin, Pin.OUT)
        
    def set_reg(self, input):
        self.clock.low()
        self.latch.low()
        self.clock.high()
        
        for i in range(8):
            self.clock.low()
            self.data.value(input[i])
            self.clock.high()

        self.clock.low()
        self.latch.high()
        self.clock.high()

def main():
    sr = shiftreg(latchpin, clockpin, datapin)
    print("start")
    sr.set_reg([0,0,0,0,0,0,0,1])
    print("enable and 1Y output")
    time.sleep(3)
    sr.set_reg([0,0,0,0,0,0,0,0])
    print("disable 1Y output")
    time.sleep(1)
    sr.set_reg([0,0,0,0,0,0,1,0])
    print("enable and 2Y output")
    time.sleep(3)
    sr.set_reg([0,0,0,0,0,0,0,0])
    print("disable 2Y output")
    time.sleep(1)
    print("end")

if __name__ == "__main__":
    main()