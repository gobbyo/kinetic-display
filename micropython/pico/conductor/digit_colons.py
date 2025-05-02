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
MOTOR_SPEED_MAX = 100
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
            self.speed.duty_u16(int((motorSpeed / MOTOR_SPEED_MAX) * LED_MAX_BRIGHTNESS))
            direction_pin.on()
            time.sleep(wait)
        except Exception as e:
            print(f"Motor movement error: {e}")
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
        previous_digit_array (list): List representing the current state of each segment.
        actuators (list): List of MotorActuator objects for controlling segment movement.
        rtc (RTC): Real-time clock object for time synchronization.
        _brightness (int): Current brightness level of the LEDs.
        motor_speed (int): Current speed of the motor actuators.
        wait_time (float): Wait time between motor movements.
        digit (int): Current digit being displayed.
        test_digit (int): Test digit for display purposes.
    """
    def __init__(self, ledPins, percentLedBrightness, motorPins):  
        self.leds = []
        self.config = None
        self.previous_digit_array = [0] * SEGMENT_COUNT
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
            self.previous_digit_array = self.config.read("previous", default=[0] * SEGMENT_COUNT)
            percent_led_brightness = float(self.config.read("brightness", default=LED_BRIGHTNESS_DEFAULT))
            self._brightness = int(percent_led_brightness * LED_MAX_BRIGHTNESS)
            self.motor_speed = int(self.config.read("speed", default=MOTOR_SPEED_MAX))
            self.wait_time = float(self.config.read("wait", default=WAIT_TIME_DEFAULT))
            self.digit = int(self.config.read("digit", default=0))
            self.test_digit = int(self.config.read("alien", default=0))

            # Initialize motor actuators
            for motor in motorPins:
                self.actuators.append(MotorActuator(MOTOR_SPEED_PIN, motor[0], motor[1]))

            # Wait for initialization to complete and set initial state
            time.sleep(0.5)
            self.setDigit(self.previous_digit_array)
        except Exception as e:
            print(f"Error during initialization: {e}")
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
        except Exception as e:
            print(f"Error during resource release: {e}")

    def __del__(self):
        try:
            for led in self.leds:
                led.duty_u16(0)
            self.config.__del__()
        except Exception as e:
            print(f"Error during cleanup: {e}")

    @property
    def testdigit(self):
        return self.test_digit
    
    @testdigit.setter
    def testdigit(self, test):
        self.test_digit = test
        self.config.write("alien", test)
    
    @property
    def speed(self):
        return self.motor_speed

    @speed.setter
    def speed(self, speed):
        self.motor_speed = speed
        self.config.write("speed", int(speed))
    
    @property
    def wait(self):
        return self.wait_time
    
    @wait.setter
    def wait(self, wt):
        self.wait_time = wt
        self.config.write("wait", wt)
    
    @property
    def brightness(self):
        return self._brightness
    
    @brightness.setter
    def brightness(self, b):
        self._brightness = int(b * LED_MAX_BRIGHTNESS)
        self.config.write("brightness", b)
        for i in range(SEGMENT_COUNT):
            if self.previous_digit_array[i] == 1:
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

        if self.previous_digit_array[seg] == 0:
            try:
                self.actuators[seg].extend(self.motor_speed, self.wait_time)
                self.leds[seg].duty_u16(self._brightness)
                self.previous_digit_array[seg] = 1
                self.setPreviousDigitArray(self.previous_digit_array)
                return 1  # Success
            except Exception as e:
                print(f"Error extending segment {seg}: {e}")
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

        if self.previous_digit_array[seg] == 1:
            try:
                self.actuators[seg].retract(self.motor_speed, self.wait_time)
                self.leds[seg].duty_u16(0)
                self.previous_digit_array[seg] = 0
                self.setPreviousDigitArray(self.previous_digit_array)
                return 1  # Success
            except Exception as e:
                print(f"Error retracting segment {seg}: {e}")
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
                if (digitArray[i] == 1 and self.previous_digit_array[i] == 0):
                    self.actuators[i].extend(self.motor_speed, self.wait_time)
                    self.leds[i].duty_u16(self._brightness)
                    actuatorMoves += 1
                elif (digitArray[i] == 0 and self.previous_digit_array[i] == 1):
                    self.actuators[i].retract(self.motor_speed, self.wait_time)
                    self.leds[i].duty_u16(0)
                    actuatorMoves += 1
                    
            self.setPreviousDigitArray(digitArray)
            return actuatorMoves
        except Exception as e:
            print(f"Error setting digit: {e}")
            return 0

    def setPreviousDigitArray(self, digitArray):  
        self.config.write('previous', digitArray)
        self.previous_digit_array = digitArray

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
                    actuator_moves = d.dance()
                    print(f"Dance completed with {actuator_moves} movements.")
                    
                # Brightness adjustment
                elif command == 'b':
                    if len(seg) < 2 or not seg[1].isdigit():
                        print("Error: Brightness command requires a digit from 0-9.")
                        continue
                    
                    brightness_value = int(seg[1])
                    if not 0 <= brightness_value <= 9:
                        print("Error: Brightness must be between 0 and 9.")
                        continue
                        
                    print(f"Setting brightness to {brightness_value}/10")
                    d.brightness = brightness_value/10  # Scale to 0-0.9
                    
                # Set digit display
                elif command == 'd':
                    if len(seg) < 2:
                        print("Error: Digit command requires a value.")
                        continue
                    
                    try:
                        a = commandHelper().decodeHex(value=seg[1])
                        digit_array = d.getDigitArray(a)
                        print(f"Setting digit {a}, array={digit_array}")
                        actuator_moves = d.setDigit(digit_array)
                        time.sleep(actuator_moves * d.wait_time)
                    except Exception as e:
                        print(f"Error setting digit: {e}")
                    
                # Extend segment
                elif command == 'e':
                    if len(seg) < 2 or not seg[1].isdigit():
                        print("Error: Extend command requires a segment number (0-1).")
                        continue
                    
                    segment_index = int(seg[1])
                    if not 0 <= segment_index < SEGMENT_COUNT:
                        print(f"Error: Invalid segment index. Must be between 0 and {SEGMENT_COUNT-1}.")
                        continue
                        
                    print(f"Extending segment {segment_index}...")
                    actuator_moves = d.extendSegment(segment_index)
                    time.sleep(actuator_moves * d.wait_time)
                    
                # Set motor speed
                elif command == 'm':
                    try:
                        if len(seg) < 2:
                            print("Error: Motor speed command requires a value (0-100).")
                            continue
                            
                        speed_value = int(seg[1:])
                        if not 0 <= speed_value <= 100:
                            print("Error: Motor speed must be between 0 and 100.")
                            continue
                            
                        print(f"Setting motor speed to {speed_value}")
                        d.speed = speed_value
                    except ValueError:
                        print("Error: Motor speed must be a number between 0 and 100.")
                    
                # Set wait time
                elif command == 'w':
                    try:
                        if len(seg) < 2:
                            print("Error: Wait time command requires a value (1-99).")
                            continue
                            
                        wait_value = int(seg[1:])
                        if not 1 <= wait_value <= 99:
                            print("Error: Wait time must be between 1 and 99.")
                            continue
                            
                        wait_time = wait_value/100
                        print(f"Setting wait time to {wait_time:.2f} seconds")
                        d.wait = wait_time
                    except ValueError:
                        print("Error: Wait time must be a number between 1 and 99.")
                    
                # Retract segment
                elif command == 'r':
                    if len(seg) < 2 or not seg[1].isdigit():
                        print("Error: Retract command requires a segment number (0-1).")
                        continue
                    
                    segment_index = int(seg[1])
                    if not 0 <= segment_index < SEGMENT_COUNT:
                        print(f"Error: Invalid segment index. Must be between 0 and {SEGMENT_COUNT-1}.")
                        continue
                        
                    print(f"Retracting segment {segment_index}...")
                    actuator_moves = d.retractSegment(segment_index)
                    time.sleep(actuator_moves * d.wait_time)
                
                # Time setting (placeholder - actual implementation needed)
                elif command == 't':
                    print("Time setting not implemented yet.")
                    # Here you would add code to set the time
                    
                # Invalid command
                else:
                    print(f"Error: Invalid command '{command}'. Please try again.")
                
            except Exception as e:
                print(f"Error processing command: {e}")
                
    except Exception as e:
        print(f"Failed to initialize DigitColons: {e}")
    finally:
        # Ensure proper cleanup
        if 'd' in locals() and d is not None:
            print("Cleaning up resources...")
            d.__del__()
            
if __name__ == "__main__":
    main()