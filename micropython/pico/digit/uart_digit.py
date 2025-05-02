import digit
from common.uart_protocol import uartProtocol, uartChannel, UARTChecksumError, UARTInvalidDigit, UARTInvalidAction, uartActions, uartCommand, commandHelper
import time
import functools

# Define magic numbers as constants with descriptive names
MAX_SEGMENT_VALUE = 6
BRIGHTNESS_DIVISOR = 10
WAIT_TIME_DIVISOR = 100
DEFAULT_BAUD_RATE_INDEX = 3
UART_RECEIVE_DELAY_SECONDS = 0.1
INITIAL_HOURS = 0
INITIAL_MINUTES = 0
INITIAL_SECONDS = 0
ACTUATOR_MOVE_DELAY_SECONDS = 0.5

def handle_errors(default_return=0):
    """
    A decorator to handle common errors in command handler functions.

    Args:
        default_return: The value to return in case of an error.

    Returns:
        A wrapped function with error handling.
    """
    def decorator(func):
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            try:
                return func(*args, **kwargs)
            except ValueError:
                print(f"ValueError in {func.__name__}: Invalid value format.")
                return default_return
            except Exception as e:
                print(f"Error in {func.__name__}: {e}")
                return default_return
        return wrapper
    return decorator

def handleCommand(display, cmd):  # Changed to CamelCase
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
    @handle_errors()
    def set_digit():
        digit_value = int(cmd.value)
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

    @handle_errors()
    def set_brightness():
        brightness_value = float(cmd.value) / BRIGHTNESS_DIVISOR
        display.brightness = brightness_value
        print(f"digit {cmd.digit} set brightness to {display.brightness}")
        return 1

    @handle_errors()
    def set_motor_speed():
        motor_speed = int(cmd.value)
        display.motor_speed = motor_speed
        print(f"digit {cmd.digit} motorspeed set to {display.motor_speed}")
        return 1

    @handle_errors()
    def set_wait_time():
        wait_time = float(cmd.value) / WAIT_TIME_DIVISOR
        display.wait_time = wait_time
        print(f"digit {cmd.digit} waittime set to {display.wait_time}")
        return 1

    @handle_errors()
    def dance():
        moves = display.dance()
        print(f"digit {cmd.digit} dancing")
        return moves

    @handle_errors()
    def extend_segment():
        segment_value = max(0, min(int(cmd.value), MAX_SEGMENT_VALUE))  # Ensure segment_value is between 0 and MAX_SEGMENT_VALUE
        moves = display.extend_segment(segment_value)
        print(f"digit {cmd.digit} extending segment {segment_value}")
        return moves

    @handle_errors()
    def retract_segment():
        segment_value = max(0, min(int(cmd.value), MAX_SEGMENT_VALUE))  # Ensure segment_value is between 0 and MAX_SEGMENT_VALUE
        
        # Validate segment index before accessing previous_digit_array
        if segment_value >= len(display.previous_digit_array):
            print(f"Invalid segment index: {segment_value}")
            return 0
        
        moves = display.retract_segment(segment_value)
        print(f"digit {cmd.digit} retracting segment {segment_value}")
        return moves

    actions = {
        uartActions.setdigit: set_digit,
        uartActions.brightness: set_brightness,
        uartActions.setmotorspeed: set_motor_speed,
        uartActions.setwaittime: set_wait_time,
        uartActions.dance: dance,
        uartActions.extendSegment: extend_segment,
        uartActions.retractSegment: retract_segment,
    }

    if display.digit == cmd.digit:
        action = actions.get(cmd.action)
        if action:
            actuator_moves = action()
            time.sleep(actuator_moves * display.wait_time)
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
    5. Enters an event-driven loop to receive and handle commands:
        - Receives a command via UART.
        - If a command is received, it prints the command details and calls handle_command to execute the command.
        - Handles various exceptions such as UARTChecksumError and UARTInvalidDigit, printing error details.

    This function is intended to be the entry point of the script when executed.
    """
    display = digit.Digit(digit.led_pins, digit.Digit.brightness, digit.motor_pins)
    uart_channel = uartChannel.uart0 if display.digit <= 1 else uartChannel.uart1
    
    display.sync_time(INITIAL_HOURS, INITIAL_MINUTES, INITIAL_SECONDS)
    print(f"Digit {display.digit} using UART channel {uart_channel}")

    try:
        uart = uartProtocol(uart_channel, commandHelper.baudRate[DEFAULT_BAUD_RATE_INDEX])
        time.sleep(ACTUATOR_MOVE_DELAY_SECONDS)

        while True:
            try:
                # Use a non-blocking approach to check for commands
                cmd = uart.receiveCommand(non_blocking=True)
                if cmd is not None:
                    print(f"digit received cmd: digit={cmd.digit} action={cmd.action} value={cmd.value}")
                    actuator_moves = handleCommand(display, cmd)
                    
                    # Instead of sleeping, use a non-blocking delay mechanism
                    if actuator_moves > 0:
                        start_time = time.ticks_ms()
                        while time.ticks_diff(time.ticks_ms(), start_time) < actuator_moves * display.wait_time * 1000:
                            # Check for new commands during the delay
                            try:
                                cmd = uart.receiveCommand(non_blocking=True)
                                if cmd is not None:
                                    print(f"digit received cmd during delay: digit={cmd.digit} action={cmd.action} value={cmd.value}")
                                    handleCommand(display, cmd)
                            except Exception as e:
                                print(f"Error during command handling in delay: {type(e).__name__}: {e}")
                                import traceback
                                traceback.print_exc()
                                raise  # Re-raise the exception for consistent error handling
            except (UARTChecksumError, UARTInvalidDigit, UARTInvalidAction) as e:
                print(f"{type(e).__name__}: {e}")
                raise  # Re-raise the exception for consistent error handling
            finally:
                # Ensure any resources like Pin objects are properly cleaned up
                if hasattr(uart, 'cleanup'):
                    uart.cleanup()
    except ValueError as e:
        print(f"ValueError: Invalid value encountered. Details: {e}")
        raise  # Re-raise the exception for consistent error handling
    except Exception as e:
        print(f"Critical error in main: {type(e).__name__}: {e}")
        import traceback
        traceback.print_exc()
        raise  # Re-raise the exception for consistent error handling
    finally:
        # Ensure any resources like Pin objects are properly cleaned up
        if hasattr(uart, 'cleanup'):
            uart.cleanup()


if __name__ == '__main__':
    main()
