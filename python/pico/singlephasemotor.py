from machine import Pin, PWM
import time

#shift register pins
latchpin = const(27) #RCLK default
clockpin = const(26) #SRCLK default
datapin = const(28) #SER default

pwmPIN=8
motor1cwPin=6 
motor1acwPin=7
motor2cwPin=9
motor2acwPin=10

def motorMove(speed,direction,speedGP,cwGP,acwGP):
  if speed > 100: speed=100
  if speed < 0: speed=0
  Speed = PWM(Pin(speedGP))
  Speed.freq(50)
  cw = Pin(cwGP, Pin.OUT)
  acw = Pin(acwGP, Pin.OUT)
  Speed.duty_u16(int((speed/100)*65536))
  if direction < 0:
      cw.value(0)
      acw.value(1)
  if direction == 0:
      cw.value(0)
      acw.value(0)
  if direction > 0:
      cw.value(1)
      acw.value(0)

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
    motorMove(0,0,pwmPIN,motor1cwPin,motor1acwPin)
    time.sleep(1)
    direction = 1
    print("start")

    while True:  

        sr.set_reg([0,0,0,0,0,0,0,1])
        motorMove(100,direction,pwmPIN,motor1cwPin,motor1acwPin)
        
        time.sleep(.2)
        motorMove(0,0,pwmPIN,motor1cwPin,motor1acwPin)
        time.sleep(.2)       
        sr.set_reg([0,0,0,0,0,0,1,0])
        motorMove(30,direction,pwmPIN,motor2cwPin,motor2acwPin)
        time.sleep(.2)
        motorMove(0,0,pwmPIN,motor2cwPin,motor2acwPin)
        time.sleep(.2)
        sr.set_reg([0,0,0,0,0,0,0,0])
        direction *= -1

if __name__ == "__main__":
    main()