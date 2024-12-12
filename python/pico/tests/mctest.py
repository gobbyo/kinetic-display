from machine import Pin, UART
import time

# Test the UART protocol
def testGPIO():
    for i in range(0,29,1):
        if i <= 22 or i >= 26:
            p = Pin(i, Pin.OUT)
            p.on()
            time.sleep(.25)
            p.off()
            time.sleep(.125)

def testUART(channel, txpin, rxpin, payload="Hello from the Pico!"):
    uart = UART(channel, 9600, rx=Pin(rxpin), tx=Pin(txpin))
    #uart.init(channel, 9600, rx=Pin(rxpin), tx=Pin(txpin))
    uart.write(payload.encode('utf-8'))
    time.sleep(.2)
    if uart.any() > 0:
        b = bytearray(payload, 'utf-8')
        size = uart.readinto(b)
        if b != None:
            s = b.decode('utf-8')
            print("UART{0}: {1}(size={2})".format(channel, s, size))
    uart.deinit()

def main():
    try:
        print("Testing GPIO and UART")
        print("This is a test of the UART protocol")
        testUART(0,0,1)
        testUART(1,4,5)
        testGPIO()
    except KeyboardInterrupt:
        print("KeyboardInterrupt")
    except Exception as e:
        print("Exception: {0}".format(e))
    finally:
        pass

if __name__ == "__main__":
    main()