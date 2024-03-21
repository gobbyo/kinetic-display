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
motor3cwPin=11
motor3acwPin=12
motor4cwPin=13
motor4acwPin=14
motor5cwPin=15
motor5acwPin=16
motor6cwPin=17
motor6acwPin=18

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
    direction = 1
    print("start")

    while True:  

        if direction == 1:
            print("forward")
            sr.set_reg([0,0,0,0,0,0,0,1])
        else:
            print("reverse")
            sr.set_reg([0,0,0,0,0,0,1,0])

        motorMove(75,direction,pwmPIN,motor1cwPin,motor1acwPin)
        time.sleep(.2)
        motorMove(0,0,pwmPIN,motor1cwPin,motor1acwPin)
        time.sleep(.1)

        motorMove(75,direction,pwmPIN,motor2cwPin,motor2acwPin)
        time.sleep(.2)
        motorMove(0,0,pwmPIN,motor2cwPin,motor2acwPin)
        time.sleep(.1)


        motorMove(75,direction,pwmPIN,motor3cwPin,motor3acwPin)
        time.sleep(.2)
        motorMove(0,0,pwmPIN,motor3cwPin,motor3acwPin)
        time.sleep(.25)

        motorMove(75,direction,pwmPIN,motor4cwPin,motor4acwPin)
        time.sleep(.2)
        motorMove(0,0,pwmPIN,motor4cwPin,motor4acwPin)
        time.sleep(.25)

        motorMove(75,direction,pwmPIN,motor5cwPin,motor5acwPin)
        time.sleep(.2)
        motorMove(0,0,pwmPIN,motor5cwPin,motor5acwPin)
        time.sleep(.25)

        motorMove(75,direction,pwmPIN,motor6cwPin,motor6acwPin)
        time.sleep(.2)
        motorMove(0,0,pwmPIN,motor6cwPin,motor6acwPin)
        time.sleep(.25)

        direction *= -1

if __name__ == "__main__":
    main()