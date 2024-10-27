import digit
from uart_protocol import uartProtocol, uartChannel, UARTChecksumError, UARTInvalidDigit, UARTInvalidAction, uartActions, uartCommand, commandHelper
import time

def main():
    display = digit.Digit(digit.led_pins, digit.LEDbrightness, digit.motor_pins)
    uartCh = uartChannel.uart0
    if display._digit > 1:
        uartCh = uartChannel.uart1
    
    display.syncTime(0,0,0)
    
    print("Digit {0} using UART channel {1}".format(display._digit, uartCh))

    try:
        uart = uartProtocol(uartCh, commandHelper.baudRate[3])
        time.sleep(.5)

        while True:
            time.sleep(.1)
            try:
                cmd = uart.receiveCommand()
                if cmd is not None:
                    print("digit received cmd: digit={0} action={1} value={2}".format(cmd.digit, cmd.action, cmd.value))
                    actuatorMoves = 0
                    if display._digit == cmd.digit:              
                        if cmd.action == int(uartActions.setdigit):
                            a = int(cmd.value)
                            if 1 == display.testdigit:
                                digitArray = display.getDigitArray(uartCommand.digitAlien[a])
                            else:
                                digitArray = display.getDigitArray(uartCommand.digitValue[a])
                            actuatorMoves = display.set_digit(digitArray)
                            print("digit {0} set to number {1}, actuator moves = {2}".format(cmd.digit, cmd.value, actuatorMoves))
                        elif cmd.action == int(uartActions.brightness):
                            # 0-9, 0 = off, 9 being 90% luminosity
                            print("digit {0} set brightness to {1}".format(cmd.digit, cmd.value/10))
                            display.brightness = cmd.value/10
                            actuatorMoves = 1
                        elif cmd.action == int(uartActions.setmotorspeed):
                            # 0-100, 100 being 100% speed
                            display.motorspeed = int(cmd.value)
                            print("digit {0} motorspeed set to {1}".format(cmd.digit, display.motorspeed))
                            actuatorMoves = 1
                        elif cmd.action == int(uartActions.setwaittime):
                            # hundreths of a second, e.g. 15 = 0.15 seconds
                            display.waitTime = float(cmd.value/100)
                            print("digit {0} waittime set to {1}".format(cmd.digit, display.waitTime))   
                            actuatorMoves = 1                         
                        elif cmd.action == int(uartActions.dance):
                            print("digit {0} dancing".format(cmd.digit))
                            actuatorMoves = display.dance()
                        elif cmd.action == int(uartActions.extendSegment):
                            if cmd.value > 6:
                                cmd.value = 6
                            print("digit {0} extending segment {1}".format(cmd.digit, cmd.value))
                            actuatorMoves = display.extend_segment(int(cmd.value))
                        elif cmd.action == int(uartActions.retractSegment):
                            if cmd.value > 6:
                                cmd.value = 6
                            print("digit {0} retracting segment {1}".format(cmd.digit, cmd.value))
                            actuatorMoves = display.retract_segment(int(cmd.value))
                        else:
                            pass
                        #prevents the display from executing the next command until the actuator has completed its move
                        time.sleep(actuatorMoves * display.waitTime)
                    else:
                        print("command ignored as target digit {0} is not digit {1}".format(cmd.digit, display._digit))
            except UARTChecksumError as e:
                print("Checksum error: {0}".format(e))
            except UARTInvalidDigit as e:
                print("Invalid digit: {0}".format(e))
            except UARTInvalidAction as e:
                print("Invalid action: {0}".format(e))
            except Exception as e:
                print("receiveCommand error: {0}".format(e))
            finally:
                pass
    except Exception as e:
        print("Exception in main: {0}".format(e))
        return

if __name__ == '__main__':
    main()