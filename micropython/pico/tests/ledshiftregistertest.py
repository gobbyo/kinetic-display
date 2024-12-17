from machine import Pin
import uasyncio as asyncio

async def blink_led(pin, on_time, off_time, iterations):
    for _ in range(iterations):
        print("on")
        pin.on()
        await asyncio.sleep(on_time)
        pin.off()
        await asyncio.sleep(off_time)

async def main():
    try:
        print("start")
        p0 = Pin(18, Pin.OUT)
        p1 = Pin(19, Pin.OUT)

        await blink_led(p0, on_time1, off_time, iterations1)
        await blink_led(p1, on_time2, off_time, iterations2)

    except Exception as e:
        print("Error: ", e)
    
    except KeyboardInterrupt:
        print("Keyboard Interrupt")
    
    finally:
        print("done")

asyncio.run(main())