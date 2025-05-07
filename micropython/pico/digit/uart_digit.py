import digit
from common.uart_protocol import uartProtocol, uartChannel, UARTChecksumError, UARTInvalidDigit, UARTInvalidAction, uartActions, uartCommand, commandHelper
import time
import gc

# Pre-calculate and store these constants instead of computing in each loop
ACTION_SETDIGIT = int(uartActions.setdigit)
ACTION_BRIGHTNESS = int(uartActions.brightness)
ACTION_SETMOTORSPEED = int(uartActions.setmotorspeed)
ACTION_SETWAITTIME = int(uartActions.setwaittime)
ACTION_DANCE = int(uartActions.dance)
ACTION_EXTENDSEGMENT = int(uartActions.extendSegment)
ACTION_RETRACTSEGMENT = int(uartActions.retractSegment)
ACTION_DIGITTYPE = int(uartActions.digittype)

# Add a debug flag to reduce print statements in production
DEBUG = False

def handle_command(display, cmd):
    """Handle commands for digit display with MicroPython compatibility."""
    # Early validation
    if display._digit != cmd.digit:
        print("command ignored as target digit", cmd.digit, "is not digit", display._digit)
        return
    
    action = int(cmd.action)
    value = int(cmd.value)
    actuator_moves = 0
    
    # Implement dispatch table for actions
    cmd_handlers = {
        ACTION_SETDIGIT: _handle_setdigit,
        ACTION_BRIGHTNESS: _handle_brightness,
        ACTION_SETMOTORSPEED: _handle_motorspeed,
        ACTION_SETWAITTIME: _handle_waittime,
        ACTION_DANCE: _handle_dance,
        ACTION_EXTENDSEGMENT: _handle_extend,
        ACTION_RETRACTSEGMENT: _handle_retract,
        ACTION_DIGITTYPE: _handle_digitType,
    }
    
    handler = cmd_handlers.get(action)
    if handler:
        actuator_moves = handler(display, cmd.digit, value)
    
    # Only sleep if needed
    if actuator_moves > 0:
        time.sleep(actuator_moves * display.waitTime)

# Helper functions (defined outside handle_command)
def _handle_setdigit(display, digit, value):
    is_alien = getattr(display, 'testdigit', 0) == 1
    pattern = uartCommand.digitTest[value] if is_alien else uartCommand.digitValue[value]
    digit_array = display.getDigitArray(pattern)
    actuator_moves = display.set_digit(digit_array)
    print("digit", digit, "set to number", value, "actuator moves =", actuator_moves)
    return actuator_moves

def _handle_brightness(display, digit, value):
    display.brightness = value / 10
    print("digit", digit, "set brightness to", display.brightness)
    return 1

def _handle_motorspeed(display, digit, value):
    display.motorspeed = value
    print("digit", digit, "motorspeed set to", display.motorspeed)
    return 1

def _handle_waittime(display, digit, value):
    display.waitTime = float(value / 100)
    print("digit", digit, "waittime set to", display.waitTime)
    return 1

def _handle_dance(display, digit, value):
    actuator_moves = display.dance()
    print("digit", digit, "dancing")
    return actuator_moves

def _handle_extend(display, digit, value):
    segment = min(value, 6)
    actuator_moves = display.extend_segment(segment)
    print("digit", digit, "extending segment", segment)
    return actuator_moves

def _handle_retract(display, digit, value):
    segment = min(value, 6)
    actuator_moves = display.retract_segment(segment)
    print("digit", digit, "retracting segment", segment)
    return actuator_moves

def _handle_digitType(display, digit, value):
    digitType = min(value, 2)
    display.testdigit = digitType
    print("digit", digit, "set to ", digitType)
    return 1

def main():
    # Initialize with error handling
    try:
        display = digit.Digit(digit.led_pins, digit.LEDbrightness, digit.motor_pins)
    except Exception as e:
        print("Error initializing display:", e)
        return
        
    uartCh = uartChannel.uart0 if display._digit <= 1 else uartChannel.uart1
    
    try:
        display.syncTime(0, 0, 0)
    except Exception as e:
        print("Error syncing time:", e)
    
    print("Digit", display._digit, "using UART channel", uartCh)

    # UART initialization with retry
    uart = None
    for attempt in range(3):
        try:
            uart = uartProtocol(uartCh, commandHelper.baudRate[3])
            break
        except Exception as e:
            print("UART init attempt", attempt, "failed:", e)
            time.sleep(1)
    
    if not uart:
        print("Failed to initialize UART")
        return
        
    time.sleep(0.5)

    # Add to the beginning of main():
    try:
        import machine
        wdt = machine.WDT(timeout=8388)  # 8388ms timeout allowed by micropython
        has_watchdog = True
    except (ImportError, AttributeError):
        has_watchdog = False
        print("Watchdog not available")

    # Main loop with watchdog considerations
    gc_counter = 0
    while True:
        gc_counter += 1
        if gc_counter > 100:  # Every ~10 seconds (with 0.1s sleep)
            gc.collect()
            gc_counter = 0

        if has_watchdog:
            try:
                wdt.feed()
            except Exception:
                pass  # Silent failure if watchdog has issues

        try:
            cmd = uart.receiveCommand()
            if cmd is not None:
                if DEBUG:
                    print("digit received cmd: digit=", cmd.digit, "action=", cmd.action, "value=", cmd.value)
                handle_command(display, cmd)
        except (UARTChecksumError, UARTInvalidDigit, UARTInvalidAction) as e:
            print(type(e).__name__ + ":", e)
        except Exception as e:
            print("receiveCommand error:", e)
        
        time.sleep(0.1)  # Reduced polling frequency to save power

if __name__ == '__main__':
    main()
