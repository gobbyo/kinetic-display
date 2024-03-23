from machine import Pin, PWM
import time

#shift register pins
latchpin = const(27) #RCLK default
clockpin = const(26) #SRCLK default
datapin = const(28) #SER default

pause = .5
waitTime = .3
speed = 100

pwmPIN=10
extend_a = [0,0,0,0,0,0,0,0,0,0,0,0,0,1]
retract_a = [0,0,0,0,0,0,0,0,0,0,0,0,1,0]
extend_b = [0,0,0,0,0,0,0,0,0,0,0,1,0,0]
retract_b = [0,0,0,0,0,0,0,0,0,0,1,0,0,0]
extend_c = [0,0,0,0,0,0,0,0,0,1,0,0,0,0]
retract_c = [0,0,0,0,0,0,0,0,1,0,0,0,0,0]
extend_d = [0,0,0,0,0,0,0,1,0,0,0,0,0,0]
retract_d = [0,0,0,0,0,0,1,0,0,0,0,0,0,0]
extend_e = [0,0,0,0,0,1,0,0,0,0,0,0,0,0]
retract_e = [0,0,0,0,1,0,0,0,0,0,0,0,0,0]
extend_f = [0,0,0,1,0,0,0,0,0,0,0,0,0,0]
retract_f = [0,0,1,0,0,0,0,0,0,0,0,0,0,0]
extend_g = [0,1,0,0,0,0,0,0,0,0,0,0,0,0]
retract_g = [1,0,0,0,0,0,0,0,0,0,0,0,0,0]
clear_reg = [0,0,0,0,0,0,0,0,0,0,0,0,0,0]


class motoractuator:
    def __init__(self, speedGP, sr):
        self.speed = PWM(Pin(speedGP))
        self.speed.freq(20)
        self.sr = sr
    
    def move(self, reg):
        self.speed.duty_u16(int((speed/100)*65536))
        self.sr.set_reg(reg)
        time.sleep(waitTime)
        self.sr.set_reg(clear_reg)
        print("move")
    
    def stop(self):
        self.speed.duty_u16(0)
        self.sr.set_reg(clear_reg)
        print("stop")

class shiftreg:
    def __init__(self, latchpin, clockpin, datapin):
        self.latch = Pin(latchpin, Pin.OUT)
        self.clock = Pin(clockpin, Pin.OUT)
        self.data = Pin(datapin, Pin.OUT)
        
    def set_reg(self, input):
        self.clock.low()
        self.latch.low()
        self.clock.high()
        
        for i in range(14):
            self.clock.low()
            self.data.value(input[i])
            self.clock.high()

        self.clock.low()
        self.latch.high()
        self.clock.high()

def main():
    sr = shiftreg(latchpin, clockpin, datapin)
    print("start")

    m = motoractuator(pwmPIN, sr)

    while True:
        m.move(extend_a)

        time.sleep(pause)
        m.stop()

        m.move(extend_e)

        time.sleep(pause)
        m.stop()
        
        m.move(retract_a)

        time.sleep(pause)
        m.stop()

        m.move(retract_e)

        time.sleep(pause)
        m.stop()

if __name__ == "__main__":
    main()