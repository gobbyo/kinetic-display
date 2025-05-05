from machine import Pin, PWM, RTC
from common.uart_protocol import commandHelper, uartCommand
import time
from common.config import Config

# Constants
LED_BRIGHTNESS_DEFAULT = 0.4
LED_MAX_BRIGHTNESS = 10922  # 1/6th of 65535
MOTOR_SPEED_PIN = 11
PWM_FREQUENCY = 50
LED_PWM_FREQUENCY = 1000
MOTOR_SPEED_MAX = 65535
MOTOR_SPEED_MAX_PERCENT = 100
WAIT_TIME_DEFAULT = 0.02
RTC_YEAR = 2000
RTC_MONTH = 1
RTC_DAY = 1
RTC_WEEKDAY = 0
RTC_SUBSECONDS = 0
DANCE_DELAY = 0.01
MAX_ATTEMPTS = 100
SEGMENT_COUNT = 2
BRIGHTNESS_SCALE = 10

# Motor tuples (extend pin, retract pin)
motor1 = (12, 13)
motor2 = (14, 15)
motor_pins = [motor1, motor2]

# LED pins
led_pins = [2, 3]

class MotorActuator:  
    """
    Controls the motor actuator for extending and retracting segments.

    This class provides methods to control the speed and direction of a motor
    actuator using PWM signals. It includes methods to extend, retract, and stop
    the motor, as well as to handle exceptions during motor operations.

    Attributes:
        speed (PWM): The PWM object to control motor speed.
        cw (Pin): The Pin object to control clockwise rotation.
        ccw (Pin): The Pin object to control counterclockwise rotation.
    """
    def __init__(self, speedPin, cwPin, acwPin):
        self.speed = PWM(Pin(speedPin))
        self.speed.freq(PWM_FREQUENCY)
        self.cw = Pin(cwPin, Pin.OUT)
        self.ccw = Pin(acwPin, Pin.OUT)
        self.stop()

    def _move(self, motorSpeed, wait, direction_pin):
        """
        Internal method to handle motor movement in a specific direction.
        
        Args:
            motorSpeed (int): Speed of the motor.
            wait (float): Time to wait during movement.
            direction_pin (Pin): Pin object for the movement direction.
        """
        try:
            self.speed.duty_u16(int((motorSpeed / MOTOR_SPEED_MAX_PERCENT) * MOTOR_SPEED_MAX))
            direction_pin.on()
            time.sleep(wait)
        except ValueError as e:
            print(f"Motor movement error - invalid parameter value: {e}")
        except OSError as e:
            print(f"Motor movement hardware error: {e}")
        except Exception as e:
            print(f"Unexpected motor movement error: {e}")
        finally:
            self.stop()

    def extend(self, motorSpeed, wait):  
        """Extend the actuator at specified speed and wait time."""
        self._move(motorSpeed, wait, self.cw)

    def retract(self, motorSpeed, wait):  
        """Retract the actuator at specified speed and wait time."""
        self._move(motorSpeed, wait, self.ccw)

    def stop(self):
        """Stop all motor movement."""
        self.speed.duty_u16(0)
        self.cw.off()
        self.ccw.off()

class DigitColons:
    """
    Manages the digit colons display and motor actuators.

    This class provides methods to control the LED brightness, motor actuators for extending
    and retracting segments, and synchronizing the time display. It reads configuration settings
    from a JSON file and allows for dynamic adjustments of brightness, motor speed, and wait time.
    The class also includes methods for setting individual segments, performing a dance sequence,
    and updating the display based on the current time.

    Attributes:
        leds (list): List of PWM objects for controlling LED brightness.
        config (Config): Configuration object for reading and writing settings.
        previousDigitArray (list): List representing the current state of each segment.
        actuators (list): List of MotorActuator objects for controlling segment movement.
        rtc (RTC): Real-time clock object for time synchronization.
        brightness (int): Current brightness level of the LEDs.
        motorSpeed (int): Current speed of the motor actuators.
        waitTime (float): Wait time between motor movements.
        digit (int): Current digit being displayed.
        testDigit (int): Test digit for display purposes.
    """
    def __init__(self, ledPins, percentLedBrightness, motorPins):  
        self.leds = []
        self.config = None
        self.previousDigitArray = [0] * SEGMENT_COUNT
        self.actuators = []
        self.rtc = None

        try:
            # Initialize PWM for LED pins
            for pin in ledPins:
                led = PWM(Pin(pin))
                led.freq(LED_PWM_FREQUENCY)
                led.duty_u16(0)
                self.leds.append(led)

            # Initialize configuration and RTC
            self.config = Config("digit.json")
            self.rtc = RTC()
            
            # Load configuration values with defaults
            self.previousDigitArray = self.config.read("previous")
            percentLedBrightness = float(self.config.read("brightness"))
            self._brightness = int(percentLedBrightness * LED_MAX_BRIGHTNESS)
            self.motorSpeed = int(self.config.read("speed"))
            self.waitTime = float(self.config.read("wait"))
            self.digit = int(self.config.read("digit"))
            self.testDigit = int(self.config.read("alien"))

            # Initialize motor actuators
            for motor in motorPins:
                self.actuators.append(MotorActuator(MOTOR_SPEED_PIN, motor[0], motor[1]))

            # Wait for initialization to complete and set initial state
            time.sleep(0.5)
            print("previousDigitArray:", self.previousDigitArray)
            self.setDigit(self.previousDigitArray)

        except ValueError as e:
            print(f"Initialization error - invalid parameter value: {e}")
            self._releaseResources()
            raise
        except OSError as e:
            print(f"Initialization hardware error: {e}")
            self._releaseResources()
            raise
        except Exception as e:
            print(f"Unexpected error during initialization: {e}")
            self._releaseResources()
            raise

    def _releaseResources(self):  
        """Release resources initialized during the constructor."""
        try:
            for led in self.leds:
                led.duty_u16(0)
            self.leds = []

            if self.config:
                self.config.__del__()
                self.config = None

            self.actuators = []
            self.rtc = None
        except OSError as e:
            print(f"Hardware error during resource release: {e}")
        except AttributeError as e:
            print(f"Attribute error during resource release: {e}")
        except Exception as e:
            print(f"Unexpected error during resource release: {e}")

    def __del__(self):
        try:
            for led in self.leds:
                led.duty_u16(0)
            self.config.__del__()
        except AttributeError as e:
            print(f"Attribute error during cleanup: {e}")
        except OSError as e:
            print(f"Hardware error during cleanup: {e}")
        except Exception as e:
            print(f"Unexpected error during cleanup: {e}")

    @property
    def testdigit(self):
        return self.testDigit
    
    @testdigit.setter
    def testdigit(self, test):
        self.testDigit = test
        self.config.write("alien", test)
    
    @property
    def speed(self):
        return self.motorSpeed

    @speed.setter
    def speed(self, speed):
        self.motorSpeed = speed
        self.config.write("speed", int(speed))
    
    @property
    def wait(self):
        return self.waitTime
    
    @wait.setter
    def wait(self, wt):
        self.waitTime = wt
        self.config.write("wait", wt)
    
    @property
    def brightness(self):
        return self._brightness
    
    @brightness.setter
    def brightness(self, b):
        self._brightness = int(b * LED_MAX_BRIGHTNESS)
        self.config.write("brightness", b)
        for i in range(SEGMENT_COUNT):
            if self.previousDigitArray[i] == 1:
                self.leds[i].duty_u16(self._brightness)

    def getDigitArray(self, val):
        a = [0] * SEGMENT_COUNT
        for i in range(len(a)):
            a[i] = (val & (0x01 << i)) >> i
        return a
    
    def extendSegment(self, seg):  
        """
        Extend a specific segment of the display.
        
        Args:
            seg (int): The segment index to extend.
            
        Returns:
            int: 1 if segment was successfully extended,
                 0 if there was an error or invalid segment,
                -1 if segment was already extended (no action taken)
        """
        if not 0 <= seg < SEGMENT_COUNT:
            print(f"Error: Invalid segment index {seg}")
            return 0

        try:
            if self.previousDigitArray[seg] == 0:
                self.actuators[seg].extend(self.motorSpeed, self.waitTime)
                self.leds[seg].duty_u16(self._brightness)
            self.previousDigitArray[seg] = 1
            self.setPreviousDigitArray(self.previousDigitArray)
            return 1  # Success
        except OSError as e:
            print(f"Hardware error extending segment {seg}: {e}")
            return 0  # Failed
        except IndexError as e:
            print(f"Index error extending segment {seg}: {e}")
            return 0  # Failed
        except Exception as e:
            print(f"Unexpected error extending segment {seg}: {e}")
            return 0  # Failed
        return -1  # Already extended, no action taken

    def retractSegment(self, seg):  
        """
        Retract a specific segment of the display.
        
        Args:
            seg (int): The segment index to retract.
            
        Returns:
            int: 1 if segment was successfully retracted,
                 0 if there was an error or invalid segment,
                -1 if segment was already retracted (no action taken)
        """
        if not 0 <= seg < SEGMENT_COUNT:
            print(f"Error: Invalid segment index {seg}")
            return 0

        try:
            if self.previousDigitArray[seg] == 1:
                self.actuators[seg].retract(self.motorSpeed, self.waitTime)
                self.leds[seg].duty_u16(0)
            self.previousDigitArray[seg] = 0
            self.setPreviousDigitArray(self.previousDigitArray)
            return 1  # Success
        except OSError as e:
            print(f"Hardware error retracting segment {seg}: {e}")
            return 0  # Failed
        except IndexError as e:
            print(f"Index error retracting segment {seg}: {e}")
            return 0  # Failed
        except Exception as e:
            print(f"Unexpected error retracting segment {seg}: {e}")
            return 0  # Failed
        return -1  # Already retracted, no action taken

    def setDigit(self, digitArray):  
        """
        Set the segments according to the provided digit array.
        
        Args:
            digitArray (list): A list of 0s and 1s representing which segments should be
                               retracted (0) or extended (1).
            
        Returns:
            int: The number of actuator movements performed, or 0 if an error occurred.
        """
        if len(digitArray) != SEGMENT_COUNT:
            print(f"Error: digitArray must have {SEGMENT_COUNT} elements.")
            return 0
            
        try:
            actuatorMoves = 0
            for i in range(SEGMENT_COUNT):
                if (digitArray[i] == 1 and self.previousDigitArray[i] == 0):
                    self.actuators[i].extend(self.motorSpeed, self.waitTime)
                    self.leds[i].duty_u16(self._brightness)
                    actuatorMoves += 1
                elif (digitArray[i] == 1 and self.previousDigitArray[i] == 1):
                    self.leds[i].duty_u16(self._brightness)
                elif (digitArray[i] == 0 and self.previousDigitArray[i] == 1):
                    self.actuators[i].retract(self.motorSpeed, self.waitTime)
                    self.leds[i].duty_u16(0)
                    actuatorMoves += 1
                    
            self.setPreviousDigitArray(digitArray)
            return actuatorMoves
        except IndexError as e:
            print(f"Index error setting digit: {e}")
            return 0
        except OSError as e:
            print(f"Hardware error setting digit: {e}")
            return 0
        except ValueError as e:
            print(f"Value error setting digit: {e}")
            return 0
        except Exception as e:
            print(f"Unexpected error setting digit: {e}")
            return 0

    def setPreviousDigitArray(self, digitArray):  
        self.config.write('previous', digitArray)
        self.previousDigitArray = digitArray

    def dance(self):
        actuatorMoves = 0
        for seg in range(SEGMENT_COUNT):
            self.extendSegment(seg)
            time.sleep(DANCE_DELAY)
            actuatorMoves += 1
        for seg in range(SEGMENT_COUNT):
            self.retractSegment(seg)
            time.sleep(DANCE_DELAY)
            actuatorMoves += 1
        return actuatorMoves

    def syncTime(self, h, m, s):  
        self.rtc.datetime((RTC_YEAR, RTC_MONTH, RTC_DAY, RTC_WEEKDAY, h, m, s, RTC_SUBSECONDS))
    
    def setTimeDisplay(self, twelveHour):  
        """
        Set the display to show the current time.
        
        Args:
            twelveHour (bool): Whether to use 12-hour format.
        """
        attempts = 0
        while attempts < MAX_ATTEMPTS:
            t = self.rtc.datetime()
            if t[6] % 10 == self.digit:
                break
            time.sleep(0.1)
            attempts += 1

        if attempts == MAX_ATTEMPTS:
            print("Warning: setTimeDisplay reached maximum attempts without success.")
            return

        # Select the appropriate digit from hours or minutes
        if self.digit < 2:
            d = '{0:02}'.format(t[4])[self.digit]  # Hour digit
        else:
            d = '{0:02}'.format(t[5])[self.digit - 2]  # Minute digit

        # Handle 12-hour format for first digit of hour
        if twelveHour and d == '0' and self.digit == 0:
            d = 'F'

        # Set the digit using the digit value mapping from uartCommand
        cmd = uartCommand("default")
        self.setDigit(self.getDigitArray(cmd.digitValue[int(d)]))

# Example usage:
def main():
    """
    Main function to interact with the DigitColons class.

    This function provides a command-line interface to control the DigitColons
    object. Users can input commands to set the digit, brightness, extend or
    retract segments, set motor speed, wait time, or quit the program.

    Commands:
        (d)igit (d0-2): Set the digit.
        (b)rightness (b0-9): Set the brightness (0-9).
        (e)xtend segment (e0-e1): Extend a specific segment.
        (t)ime: Set the time.
        (r)etract segment (r0-r1): Retract a specific segment.
        (m)otor speed (m0-100): Set the motor speed (0-100).
        (w)ait time (w1-99): Set the wait time (1-99).
        (a): Run dance sequence.
        (q)uit: Quit the program.
    """
    d = None
    try:
        d = DigitColons(led_pins, 0.4, motor_pins)
        
        while True:
            try:
                print("\nDigitColons Control Interface")
                print("-" * 30)
                print("Current settings:")
                print(f"  Brightness: {d.brightness/LED_MAX_BRIGHTNESS:.1f}")
                print(f"  Motor speed: {d.speed}")
                print(f"  Wait time: {d.wait:.2f}")
                print("-" * 30)
                
                seg = input("Enter command:\n"
                            "\t(d)igit (d0-2): Set digit\n"
                            "\t(b)rightness (b0-9): Set brightness\n"
                            "\t(e)xtend segment (e0-e1): Extend segment\n"
                            "\t(t)ime: Set time\n"
                            "\t(r)etract segment (r0-r1): Retract segment\n"
                            "\t(m)otor speed (m0-100): Set motor speed\n"
                            "\t(w)ait time (w1-99): Set wait time\n"
                            "\t(a): Run dance sequence\n"
                            "\t(q)uit: Exit program\n"
                            "\t>: ")
                
                # Basic validation for empty input
                if not seg:
                    print("Error: Empty input. Please enter a valid command.")
                    continue
                
                # Process the command based on the first character
                command = seg[0].lower()
                
                # Quit
                if command == 'q':
                    print("Exiting program...")
                    break
                    
                # Dance sequence
                elif command == 'a':
                    print("Running dance sequence...")
                    actuatorMoves = d.dance()
                    print(f"Dance completed with {actuatorMoves} movements.")
                    
                # Brightness adjustment
                elif command == 'b':
                    if len(seg) < 2 or not seg[1].isdigit():
                        print("Error: Brightness command requires a digit from 0-9.")
                        continue
                    
                    brightnessValue = int(seg[1])
                    if not 0 <= brightnessValue <= 9:
                        print("Error: Brightness must be between 0 and 9.")
                        continue
                        
                    print(f"Setting brightness to {brightnessValue}/10")
                    d.brightness = brightnessValue/10  # Scale to 0-0.9
                    
                # Set digit display
                elif command == 'd':
                    if len(seg) < 2:
                        print("Error: Digit command requires a value.")
                        continue
                    
                    try:
                        a = commandHelper().decodeHex(value=seg[1])
                        digitArray = d.getDigitArray(a)
                        print(f"Setting digit {a}, array={digitArray}")
                        actuatorMoves = d.setDigit(digitArray)
                        time.sleep(actuatorMoves * d.wait)
                    except ValueError as e:
                        print(f"Value error setting digit: {e}")
                    except TypeError as e:
                        print(f"Type error setting digit: {e}")
                    except Exception as e:
                        print(f"Unexpected error setting digit: {e}")
                    
                # Extend segment
                elif command == 'e':
                    if len(seg) < 2 or not seg[1].isdigit():
                        print("Error: Extend command requires a segment number (0-1).")
                        continue
                    
                    segmentIndex = int(seg[1])
                    if not 0 <= segmentIndex < SEGMENT_COUNT:
                        print(f"Error: Invalid segment index. Must be between 0 and {SEGMENT_COUNT-1}.")
                        continue
                        
                    print(f"Extending segment {segmentIndex}...")
                    actuatorMoves = d.extendSegment(segmentIndex)
                    time.sleep(actuatorMoves * d.wait)
                    
                # Set motor speed
                elif command == 'm':
                    try:
                        if len(seg) < 2:
                            print("Error: Motor speed command requires a value (0-100).")
                            continue
                            
                        speedValue = int(seg[1:])
                        if not 0 <= speedValue <= 100:
                            print("Error: Motor speed must be between 0 and 100.")
                            continue
                            
                        print(f"Setting motor speed to {speedValue}")
                        d.speed = speedValue
                    except ValueError as e:
                        print(f"Value error setting motor speed: {e}")
                    
                # Set wait time
                elif command == 'w':
                    try:
                        if len(seg) < 2:
                            print("Error: Wait time command requires a value (1-99).")
                            continue
                            
                        waitValue = int(seg[1:])
                        if not 1 <= waitValue <= 99:
                            print("Error: Wait time must be between 1 and 99.")
                            continue
                            
                        waitTime = waitValue/100
                        print(f"Setting wait time to {waitTime:.2f} seconds")
                        d.wait = waitTime
                    except ValueError as e:
                        print(f"Value error setting wait time: {e}")
                    
                # Retract segment
                elif command == 'r':
                    if len(seg) < 2 or not seg[1].isdigit():
                        print("Error: Retract command requires a segment number (0-1).")
                        continue
                    
                    segmentIndex = int(seg[1])
                    if not 0 <= segmentIndex < SEGMENT_COUNT:
                        print(f"Error: Invalid segment index. Must be between 0 and {SEGMENT_COUNT-1}.")
                        continue
                        
                    print(f"Retracting segment {segmentIndex}...")
                    actuatorMoves = d.retractSegment(segmentIndex)
                    time.sleep(actuatorMoves * d.wait)
                
                # Time setting (placeholder - actual implementation needed)
                elif command == 't':
                    print("Time setting not implemented yet.")
                    # Here you would add code to set the time
                    
                # Invalid command
                else:
                    print(f"Error: Invalid command '{command}'. Please try again.")
                
            except OSError as e:
                print(f"Hardware error processing command: {e}")
            except ValueError as e:
                print(f"Value error processing command: {e}")
            except KeyboardInterrupt:
                print("\nOperation interrupted by user.")
                break
            except Exception as e:
                print(f"Unexpected error processing command: {e}")
                
    except OSError as e:
        print(f"Hardware error initializing DigitColons: {e}")
    except ValueError as e:
        print(f"Value error initializing DigitColons: {e}")
    except KeyboardInterrupt:
        print("\nOperation interrupted by user.")
    except Exception as e:
        print(f"Unexpected error initializing DigitColons: {e}")
    finally:
        # Ensure proper cleanup
        if d is not None:
            print("Cleaning up resources...")
            d.__del__()
            
if __name__ == "__main__":
    main()