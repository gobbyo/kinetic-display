import digit
from common.uart_protocol import uartProtocol, uartChannel, UARTChecksumError, UARTInvalidDigit, UARTInvalidAction, uartActions, uartCommand, commandHelper
import time
#import asyncio
# Define magic numbers as constants
MAX_SEGMENT_VALUE = 6
BRIGHTNESS_DIVISOR = 10
WAIT_TIME_DIVISOR = 100
DEFAULT_BAUD_RATE_INDEX = 3
UART_RECEIVE_DELAY = 0.1
INITIAL_SYNC_TIME = (0, 0, 0)
ACTUATOR_MOVE_DELAY = 0.5
def handle_command(display, cmd):
    """
    Handle a command received via UART and perform the corresponding action on the display.

    Args:
        display: The display object that the command will be executed on.
        cmd: The command object containing the action to be performed and its parameters.

    The function supports the following actions:
        - Set digit value
        - Set brightness
        - Set motor speed
        - Set wait time
        - Perform a dance sequence
        - Extend a segment
        - Retract a segment

    The function will print the action taken and any relevant details to the console.
    """
    def set_digit():
        try:
            digit_value = int(cmd.value)
            
            # Check if digit_value is in valid range
            if digit_value not in uartCommand.digitValue:
                print(f"Invalid digit value: {digit_value}")
                return 0
                
            digit_array = display.getDigitArray(
                uartCommand.digitAlien[digit_value] if display.testdigit == 1 
                else uartCommand.digitValue[digit_value]
            )
            
            moves = display.set_digit(digit_array)
            print(f"digit {cmd.digit} set to number {digit_value}, actuator moves = {moves}")
            return moves
            
        except ValueError:
            print(f"Invalid digit value format: {cmd.value}")
            return 0
        except Exception as e:
            print(f"Error setting digit: {e}")
            return 0


    def set_brightness():
        display.brightness = cmd.value / 10
        print(f"digit {cmd.digit} set brightness to {display.brightness}")
        return 1

    def set_motor_speed():
        display.motorspeed = int(cmd.value)
        print(f"digit {cmd.digit} motorspeed set to {display.motorspeed}")
        return 1

    def set_wait_time():
        display.waitTime = float(cmd.value / 100)
        print(f"digit {cmd.digit} waittime set to {display.waitTime}")
        return 1

    def dance():
        moves = display.dance()
        print(f"digit {cmd.digit} dancing")
        return moves

    def extend_segment():
        cmd.value = min(cmd.value, 6)
        moves = display.extend_segment(int(cmd.value))
        print(f"digit {cmd.digit} extending segment {cmd.value}")
        return moves

    def retract_segment():
        cmd.value = min(cmd.value, 6)
        moves = display.retract_segment(int(cmd.value))
        print(f"digit {cmd.digit} retracting segment {cmd.value}")
        return moves

    actions = {
        int(uartActions.setdigit): set_digit,
        int(uartActions.brightness): set_brightness,
        int(uartActions.setmotorspeed): set_motor_speed,
        int(uartActions.setwaittime): set_wait_time,
        int(uartActions.dance): dance,
        int(uartActions.extendSegment): extend_segment,
        int(uartActions.retractSegment): retract_segment,
    }

    if display.digit == cmd.digit:
        action = actions.get(cmd.action)
        if action:
            actuatorMoves = action()
            time.sleep(actuatorMoves * display.waitTime)
        else:
            print(f"Unknown action {cmd.action} for digit {cmd.digit}")
    else:
        print(f"command ignored as target digit {cmd.digit} is not digit {display.digit}")

def main():
    """
    The main function initializes the display and UART communication, then enters a loop to handle incoming commands.

    The function performs the following steps:
    1. Initializes the display object with the appropriate pins and settings.
    2. Selects the UART channel based on the display digit.
    3. Synchronizes the display time.
    4. Initializes the UART protocol with the selected channel and baud rate.
    5. Enters an infinite loop to receive and handle commands:
        - Receives a command via UART.
        - If a command is received, it prints the command details and calls handle_command to execute the command.
        - Handles various exceptions such as UARTChecksumError and UARTInvalidDigit, printing error details.

    This function is intended to be the entry point of the script when executed.
    """
    display = digit.Digit(digit.led_pins, digit.Digit.brightness, digit.motor_pins)
    uartCh = uartChannel.uart0 if display.digit <= 1 else uartChannel.uart1
    
    display.sync_time(0, 0, 0)
    print(f"Digit {display.digit} using UART channel {uartCh}")

    try:
        uart = uartProtocol(uartCh, commandHelper.baudRate[3])
        time.sleep(.5)

        while True:
            time.sleep(.1)
            try:
                cmd = uart.receiveCommand()
                if cmd is not None:
                    print(f"digit received cmd: digit={cmd.digit} action={cmd.action} value={cmd.value}")
                    handle_command(display, cmd)
            except UARTChecksumError as e:
                print(f"UARTChecksumError: Invalid checksum detected. Details: {e}")
            except UARTInvalidDigit as e:
                print(f"UARTInvalidDigit: Received an invalid digit. Details: {e}")
    except Exception as e:
        print(f"Critical error in main: {type(e).__name__}: {e}")
        # Optionally log the stack trace for debugging
        import traceback
        traceback.print_exc()
    except ValueError as e:
        print(f"ValueError: Invalid value encountered. Details: {e}")
    except Exception as e:
        print(f"Unexpected error in receiveCommand: {type(e).__name__}: {e}")
        # Optionally log the stack trace for debugging
        import traceback
        traceback.print_exc()
    except Exception as e:
        print(f"Exception in main: {e}")

if __name__ == '__main__':
    main()
    #asyncio.run(main())