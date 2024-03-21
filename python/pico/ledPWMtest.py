from machine import Pin, PWM
import time


def main():
    percentBrightness = .50
    brightness = int(percentBrightness*65536)

    try:
        LEDs = [PWM(Pin(7)), PWM(Pin(8)), PWM(Pin(9)), PWM(Pin(10)), PWM(Pin(11)), PWM(Pin(12)), PWM(Pin(13))]

        for LED in LEDs:
            LED.freq(5000)

        while True:
            for LED in LEDs:
                LED.duty_u16(brightness)
                time.sleep(0.5)
                LED.duty_u16(0)
    
    except Exception as e:
        print("Error: ", e)
    
    except KeyboardInterrupt:
        print("Keyboard Interrupt")
    
    finally:
        for LED in LEDs:
            LED.duty_u16(0)
            LED.deinit()
        print("done")

if __name__ == "__main__":
    main()