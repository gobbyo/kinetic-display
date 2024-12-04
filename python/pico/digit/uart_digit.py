import digit
from common.uart_protocol import uartProtocol, uartChannel, UARTChecksumError, UARTInvalidDigit, UARTInvalidAction, uartActions, uartCommand, commandHelper
import asyncio

async def handle_command(display, cmd):
    actuatorMoves = 0
    if display._digit == cmd.digit:
        if cmd.action == int(uartActions.setdigit):
            a = int(cmd.value)
            digitArray = display.getDigitArray(uartCommand.digitAlien[a] if display.testdigit == 1 else uartCommand.digitValue[a])
            actuatorMoves = display.set_digit(digitArray)
            print(f"digit {cmd.digit} set to number {cmd.value}, actuator moves = {actuatorMoves}")
        elif cmd.action == int(uartActions.brightness):
            display.brightness = cmd.value / 10
            actuatorMoves = 1
            print(f"digit {cmd.digit} set brightness to {display.brightness}")
        elif cmd.action == int(uartActions.setmotorspeed):
            display.motorspeed = int(cmd.value)
            actuatorMoves = 1
            print(f"digit {cmd.digit} motorspeed set to {display.motorspeed}")
        elif cmd.action == int(uartActions.setwaittime):
            display.waitTime = float(cmd.value / 100)
            actuatorMoves = 1
            print(f"digit {cmd.digit} waittime set to {display.waitTime}")
        elif cmd.action == int(uartActions.dance):
            actuatorMoves = display.dance()
            print(f"digit {cmd.digit} dancing")
        elif cmd.action == int(uartActions.extendSegment):
            cmd.value = min(cmd.value, 6)
            actuatorMoves = display.extend_segment(int(cmd.value))
            print(f"digit {cmd.digit} extending segment {cmd.value}")
        elif cmd.action == int(uartActions.retractSegment):
            cmd.value = min(cmd.value, 6)
            actuatorMoves = display.retract_segment(int(cmd.value))
            print(f"digit {cmd.digit} retracting segment {cmd.value}")
        else:
            pass
        await asyncio.sleep(actuatorMoves * display.waitTime)
    else:
        print(f"command ignored as target digit {cmd.digit} is not digit {display._digit}")

async def main():
    display = digit.Digit(digit.led_pins, digit.LEDbrightness, digit.motor_pins)
    uartCh = uartChannel.uart0 if display._digit <= 1 else uartChannel.uart1
    
    display.syncTime(0, 0, 0)
    print(f"Digit {display._digit} using UART channel {uartCh}")

    try:
        uart = uartProtocol(uartCh, commandHelper.baudRate[3])
        await asyncio.sleep(.5)

        while True:
            await asyncio.sleep(.1)
            try:
                cmd = await uart.receiveCommand()
                if cmd is not None:
                    print(f"digit received cmd: digit={cmd.digit} action={cmd.action} value={cmd.value}")
                    await handle_command(display, cmd)
            except (UARTChecksumError, UARTInvalidDigit, UARTInvalidAction) as e:
                print(f"{type(e).__name__}: {e}")
            except Exception as e:
                print(f"receiveCommand error: {e}")
    except Exception as e:
        print(f"Exception in main: {e}")

if __name__ == '__main__':
    asyncio.run(main())