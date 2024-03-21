from machine import Pin, PWM
import time

waitTime = 0.2
speed = 75

pwmPIN=10
motor1cwPin=12 
motor1acwPin=13
motor2cwPin=14
motor2acwPin=15
motor3cwPin=16
motor3acwPin=17
motor4cwPin=18
motor4acwPin=19
motor5cwPin=20
motor5acwPin=21
motor6cwPin=22
motor6acwPin=26
motor7cwPin=27
motor7acwPin=11

LED_A = 2
LED_B = 3
LED_C = 4
LED_D = 5
LED_E = 6
LED_F = 7
LED_G = 28

class motoractuator:
    def __init__(self, speedGP, cwGP, acwGP):
        self.speed = PWM(Pin(speedGP))
        self.speed.freq(50)
        self.cw = Pin(cwGP, Pin.OUT)
        self.acw = Pin(acwGP, Pin.OUT)
    
    def extend(self, speed):
        self.speed.duty_u16(int((speed/100)*65536))
        self.cw.on()
        self.acw.off()
        time.sleep(waitTime)
        self.stop()
        print("extend")
    
    def retract(self, speed):
        self.speed.duty_u16(int((speed/100)*65536))
        self.cw.off()
        self.acw.on()
        time.sleep(waitTime)
        self.stop()
        print("retract")
    
    def stop(self):
        self.speed.duty_u16(0)
        self.cw.off()
        self.acw.off()
        print("stop")

def main():
    print("start")

    percentBrightness = .50
    brightness = int(percentBrightness*65536)
    LEDs = [PWM(Pin(LED_A)), PWM(Pin(LED_B)), PWM(Pin(LED_C)), PWM(Pin(LED_D)), PWM(Pin(LED_E)), PWM(Pin(LED_F)), PWM(Pin(LED_G))]
    
    for i in range(0, 7):
        LEDs[i].freq(5000)

    try:
        #actuators = []
        #actuators.append(motoractuator(pwmPIN,motor1cwPin,motor1acwPin))
        actuators = [motoractuator(pwmPIN,motor1cwPin,motor1acwPin), motoractuator(pwmPIN,motor2cwPin,motor2acwPin), motoractuator(pwmPIN,motor3cwPin,motor3acwPin), motoractuator(pwmPIN,motor4cwPin,motor4acwPin), motoractuator(pwmPIN,motor5cwPin,motor5acwPin), motoractuator(pwmPIN,motor6cwPin,motor6acwPin), motoractuator(pwmPIN,motor7cwPin,motor7acwPin)]
        print("actuators initialized")

        while True:
            for i in range(0, 7):
                actuators[i].extend(speed)
                actuators[i].stop()
                LEDs[i].duty_u16(brightness)
                #time.sleep(.1)
            
            time.sleep(1)
            for i in range(0, 7):
                LEDs[i].duty_u16(0)
                actuators[i].retract(speed)
                actuators[i].stop()
                #time.sleep(.1)
            time.sleep(1)

    except Exception as e:
        print("Error: ", e)
    except KeyboardInterrupt:
        print("Keyboard Interrupt")
    finally:
        for i in range(0, 7):
            LEDs[i].duty_u16(0)
            actuators[i].retract(speed)
            time.sleep(.2)
            actuators[i].stop()
            time.sleep(.1)
        print("done")

if __name__ == "__main__":
    main()