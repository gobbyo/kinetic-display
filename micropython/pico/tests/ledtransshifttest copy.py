from machine import Pin
import time

#shift register pins
latchpin = const(8) #RCLK default
clockpin = const(9) #SRCLK default
datapin = const(10) #SER default

class shiftreg:
    def __init__(self, latchpin, clockpin, datapin):
        self.latch = Pin(latchpin, Pin.OUT)
        self.clock = Pin(clockpin, Pin.OUT)
        self.data = Pin(datapin, Pin.OUT)
        
    def set_reg(self, input):
        self.clock.low()
        self.latch.low()
        self.clock.high()
        
        for i in range(0,7):
            self.clock.low()
            self.data.value(input[i])
            self.clock.high()

        self.clock.low()
        self.latch.high()
        self.clock.high()

def main():
    leds = shiftreg(latchpin, clockpin, datapin)

    try:
        reg = [0,0,0,0,0,0,0,0]

        for i in range(0,7):
                reg[7-i] = 1
                leds.set_reg(reg)
                time.sleep(0.5)

        print("reg = {0}".format(reg))
    except Exception as e:
        print("Error: ", e)
    
    except KeyboardInterrupt:
        print("Keyboard Interrupt")
    
    finally:
        for i in range(0,7):
            reg[7-i] = 0
            leds.set_reg(reg)
            time.sleep(0.5)
        print("done")

if __name__ == "__main__":
    main()