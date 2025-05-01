from machine import Pin, PWM, RTC
from common.uart_protocol import commandHelper, uartCommand
import time
from common.config import Config

# Constants
LED_BRIGHTNESS_DEFAULT = 0.4
MOTOR_SPEED_PIN = 11
PWM_FREQUENCY = 50
LED_PWM_FREQUENCY = 1000
MOTOR_SPEED_MAX = 100
WAIT_TIME_DEFAULT = 0.02
BRIGHTNESS_MAX = 65536
DIGIT_ARRAY_SIZE = 7
RTC_YEAR = 2000
RTC_MONTH = 1
RTC_DAY = 1
RTC_WEEKDAY = 0
RTC_SUBSECONDS = 0

# Motor tuples (extend pin, retract pin)
motor1 = (12, 13)
motor2 = (14, 15)
motor3 = (16, 17)
motor4 = (18, 19)
motor5 = (20, 21)
motor6 = (22, 26)
motor7 = (27, 10)
motor_pins = [motor1, motor2, motor3, motor4, motor5, motor6, motor7]

# LED pins
led_pins = [2, 3, 6, 7, 8, 9, 28]

class Motoractuator:
    def __init__(self, speedPin, cwPin, ccwPin):
        self.speed = PWM(Pin(speedPin))
        self.speed.freq(PWM_FREQUENCY)
        self.cw = Pin(cwPin, Pin.OUT)
        self.ccw = Pin(ccwPin, Pin.OUT)
        self.stop()
    
    def extend(self, motor_speed, waitTime):
        try:
            self.speed.duty_u16(int((motor_speed / MOTOR_SPEED_MAX) * BRIGHTNESS_MAX))
            self.cw.on()
            time.sleep(waitTime)
        except Exception as e:
            print(f"extend error: {e}")
        finally:
            self.stop()
            #print("extend")
    
    def retract(self, motor_speed, waitTime):
        try:
            self.speed.duty_u16(int((motor_speed / MOTOR_SPEED_MAX) * BRIGHTNESS_MAX))
            self.ccw.on()
            time.sleep(waitTime)
        except Exception as e:
            print(f"retract error: {e}")
        finally:
            self.stop()
            #print("retract")
    
    def stop(self):
        self.speed.duty_u16(0)
        self.cw.off()
        self.ccw.off()
        #print("stop")

class Digit:
    """
    The Digit class represents a digital display controlled by LEDs and motor actuators.

    This class provides methods to initialize the display, load configuration settings,
    control the brightness of LEDs, extend and retract segments, and display digits.
    It also includes functionality to synchronize and display time, and perform a "dance"
    sequence by sequentially extending and retracting segments.

    The code is written to be synchronous, not asynchronous. 
    The design of the power system cannot safely handle more than one motor active at any given time.

    Attributes:
        leds (list): A list of PWM objects controlling the LEDs.
        start_led (Pin): A Pin object for the start LED.
        config (Config): A Config object for loading and saving configuration settings.
        actuators (list): A list of Motoractuator objects controlling the segments.
        rtc (RTC): An RTC object for real-time clock functionality.
        previous_digit_array (list): A list representing the previous state of the digit segments.
        brightness (int): The brightness level of the LEDs.
        motor_speed (int): The speed of the motor actuators.
        wait_time (float): The wait time for motor movements.
        digit (int): The current digit being displayed.
        test_digit (int): A test digit value.
    """
    def __init__(self, led_pins, percent_led_brightness, motor_pins):
        """
        Initialize the Digit class.

        This constructor initializes the Digit class by setting up the LEDs, loading the configuration,
        initializing the actuators, and setting up the RTC. It also handles exceptions that may occur
        during initialization and releases resources if an error is encountered.

        Args:
            led_pins (list): A list of GPIO pins connected to the LEDs.
            percent_led_brightness (float): The default brightness level for the LEDs, as a percentage.
            motor_pins (list): A list of tuples, where each tuple contains the extend and retract pins for a motor.
        """
        self.leds = []
        self.start_led = None
        self.config = None
        self.actuators = []
        self.rtc = None

        try:
            self.start_led = Pin(25, Pin.OUT)

            # Initialize LEDs
            for pin in led_pins:
                led = PWM(Pin(pin))
                led.freq(LED_PWM_FREQUENCY)
                led.duty_u16(0)
                self.leds.append(led)

            # Load configuration
            self.config = Config("digit.json")
            self.previous_digit_array = [0] * 7
            self.brightness = 0
            self.motor_speed = 0
            self.wait_time = 0
            self.digit = 0
            self.test_digit = 0

            self.rtc = RTC()
            self._load_config()

            # Initialize actuators
            self.actuators = [
                Motoractuator(MOTOR_SPEED_PIN, motor[0], motor[1]) for motor in motor_pins
            ]
            for actuator in self.actuators:
                actuator.stop()

        except OSError as fnfe:
            print(f"Configuration file not found: {fnfe}")
            self._release_resources()
            raise
        except ValueError as ve:
            print(f"Invalid configuration value: {ve}")
            self._release_resources()
            raise
        except Exception as e:
            print(f"Unexpected error during initialization: {e}")
            self._release_resources()
            raise

    def _release_resources(self):
        """Release resources initialized during the constructor."""
        if self.leds:
            for led in self.leds:
                led.duty_u16(0)
        if self.start_led:
            self.start_led.off()
        if self.config:
            self.config.__del__()
        self.leds = []
        self.actuators = []
        self.start_led = None
        self.config = None
        self.rtc = None

    def _load_config(self):
        """Load configuration values from the config file."""
        try:
            self.previous_digit_array = self.config.read("previous") or [0] * 7
        except KeyError:
            self.previous_digit_array = [0] * 7

        try:
            self.brightness = int(float(self.config.read("brightness")) * 65536)
        except (KeyError, TypeError, ValueError):
            self.brightness = int(0.5 * 65536)

        try:
            self.motor_speed = int(self.config.read("motorspeed"))
        except (KeyError, TypeError, ValueError):
            self.motor_speed = 50

        try:
            self.wait_time = float(self.config.read("waitTime"))
        except (KeyError, TypeError, ValueError):
            self.wait_time = 0.02

        try:
            self.digit = int(self.config.read("digit"))
        except (KeyError, TypeError, ValueError):
            self.digit = 0

        try:
            self.test_digit = int(self.config.read("alien"))
        except (KeyError, TypeError, ValueError):
            self.test_digit = 0

    def __del__(self):
        """Clean up resources when the object is garbage collected."""
        try:
            if hasattr(self, 'leds'):
                for led in self.leds:
                    led.duty_u16(0)
            if hasattr(self, 'start_led'):
                self.start_led.off()
            if hasattr(self, 'config'):
                print("need to add close method to config")
                #self.config.close()  # Assuming there's a close method
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
    def motorspeed(self):
        return self.motor_speed

    @motorspeed.setter
    def motorspeed(self, speed):
        self.motor_speed = speed
        self.config.write("motorspeed", speed)
    
    @property
    def waitTime(self):
        return self.wait_time
    
    @waitTime.setter
    def waitTime(self, wt):
        self.wait_time = wt
        self.config.write("waitTime", wt)
    
    @property
    def brightness(self):
        return self._brightness
    
    @brightness.setter
    def brightness(self, b):
        self._brightness = int(b*65536)
        self.config.write("brightness", b)
        for i in range(0,7):
            if 1 == self.previous_digit_array[i]:
                self.leds[i].duty_u16(self._brightness)
                print(f"----------\nbrightness {self._brightness} seg={i}")

    def getDigitArray(self, val):
        """
        Convert an integer value to a digit array.

        This method takes an integer value and converts it into a list of binary digits,
        representing the segments of a digit display. Each element in the list corresponds
        to a segment, where 1 indicates the segment should be on and 0 indicates it should be off.

        Args:
            val (int): The integer value to be converted.

        Returns:
            list: A list of integers (0 or 1) representing the segments of the digit display.
        """
        a = [0,0,0,0,0,0,0]
        for i in range(len(a)):
            a[i] = (val & (0x01 << i)) >> i
        return a
    
    def extend_segment(self, seg):
        """
        Extend a specific segment of the digit display.

        This method extends the specified segment by activating the corresponding actuator
        and setting the LED brightness. It also updates the internal state to reflect the
        extended segment.

        Args:
            seg (int): The index of the segment to extend.

        Returns:
            int: 1 if the segment was successfully extended, 0 if the segment index is invalid.
        """
        if not 0 <= seg < len(self.previous_digit_array):
            print(f"Error: Invalid segment index {seg}")
            return 0

        if self.previous_digit_array[seg] == 0:
            try:
                self.actuators[seg].extend(self.motor_speed, self.wait_time)
                self.leds[seg].duty_u16(self._brightness)
                self.previous_digit_array[seg] = 1
                self.set_previous_digit_array(self.previous_digit_array)
            except IndexError as e:
                print(f"Error accessing actuator/LED for segment {seg}: {e}")
            except Exception as e:
                print(f"Error extending segment {seg}: {e}")
        return 1


    def retract_segment(self, seg):
        """
        Retract a specific segment of the digit display.

        This method retracts the specified segment by deactivating the corresponding actuator
        and turning off the LED. It also updates the internal state to reflect the retracted segment.

        Args:
            seg (int): The index of the segment to retract.

        Returns:
            int: 1 if the segment was successfully retracted, 0 if the segment index is invalid.
        """
        if self.previous_digit_array[seg] == 1:
            try:
                self.actuators[seg].retract(self.motor_speed, self.wait_time)
                self.leds[seg].duty_u16(0)
                self.previous_digit_array[seg] = 0
                self.setPreviousDigitArray(self.previous_digit_array)
            except Exception as e:
                print(f"Error retracting segment {seg}: {e}")
        return 1

    def set_digit(self, digitArray):
        """
        Set the digit display to the specified digit array.

        This method updates the digit display by extending or retracting the segments
        based on the provided digit array. It also updates the LED brightness for each
        segment and keeps track of the number of actuator moves performed.

        Args:
            digitArray (list): A list of integers representing the segments to be displayed.
                               Each element should be 0 or 1, where 1 indicates the segment
                               should be extended and 0 indicates it should be retracted.

        Returns:
            int: The total number of actuator moves performed.
        """
        self.start_led.on()
        actuatorMoves = 0
        print(f"set_digit: {digitArray}")
        for i in range(0,7):
            skipped = True
            if (1 == digitArray[i]) and (0 == self.previous_digit_array[i]):
                self.actuators[i].extend(self.motor_speed,self.wait_time)
                print(f"\t[1] seg {chr(i+97)} extended")
                self.leds[i].duty_u16(self._brightness)
                actuatorMoves += 1
                skipped = False

            if (1 == digitArray[i]) and (1 == self.previous_digit_array[i]):
                self.leds[i].duty_u16(self._brightness)
                print(f"\t[1] seg {chr(i+97)} skipped")
                skipped = False

            if (0 == digitArray[i]) and (1 == self.previous_digit_array[i]):
                print(f"\t[0] seg {chr(i+97)} retracted")
                self.leds[i].duty_u16(0)
                self.actuators[i].retract(self.motor_speed,self.wait_time)
                actuatorMoves += 1
                skipped = False

            if skipped:
                print(f"\t[{self.previous_digit_array[i]}] seg {chr(i+97)} skipped")

        self.setPreviousDigitArray(digitArray)
        self.start_led.off()
        return actuatorMoves

    def setPreviousDigitArray(self, digitArray):
        """
        Update the previous digit array and save it to the configuration.

        This method writes the provided digit array to the configuration file
        and updates the internal state to reflect the new digit array.

        Args:
            digitArray (list): A list of integers representing the new digit array.
        """
        self.config.write('previous',digitArray)
        for i in range(7):
            self.previous_digit_array[i] = digitArray[i]

    def dance(self):
        """
        Perform a sequence of extending and retracting all segments in a predefined order.

        This method sequentially extends and retracts each segment of the digit display,
        creating a "dance" effect. The method turns on the start LED at the beginning and
        turns it off at the end. It also keeps track of the number of actuator moves performed.

        Returns:
            int: The total number of actuator moves performed during the dance sequence.
        """
        self.start_led.on()
        actuatorMoves = 0
        for seg in [2,3,4,5,0,1,6]:
            self.extend_segment(seg)
            time.sleep(.01)
            actuatorMoves += 1
        for seg in [5,0,1,2,3,4,6]:
            self.retract_segment(seg)
            time.sleep(.01)
            actuator_moves += 1
        self.start_led.off()
        return actuator_moves

    def sync_time(self, h, m, s):
        """
        Synchronize the RTC with the provided time.

        Args:
            h (int): Hours (0-23).
            m (int): Minutes (0-59).
            s (int): Seconds (0-59).
        """
        # time tuple = [year, month, day, weekday, hours, minutes, seconds, subseconds]
        self.rtc.datetime((RTC_YEAR, RTC_MONTH, RTC_DAY, RTC_WEEKDAY, h, m, s, RTC_SUBSECONDS))
    
    def set_time_display(self, twelve_hour):
        """
        Display the current time on the digit display in either 12-hour or 24-hour format.

        Args:
            twelve_hour (bool): If True, display time in 12-hour format. Otherwise, use 24-hour format.
        """
        max_attempts = 100  # Prevent infinite loop by limiting attempts
        attempts = 0

        while attempts < max_attempts:
            t = self.rtc.datetime()
            if t[6] % 10 == self.digit:
                break
            time.sleep(0.1)
            attempts += 1

        if attempts == max_attempts:
            print("Warning: set_time_display reached maximum attempts without success.")
            return

        if self.digit < 2:  # Hours
            d = '{0:02}'.format(t[4])[self.digit]
            if twelve_hour and d == '0' and self.digit == 0:
                d = 'F'
        else:  # Minutes
            d = '{0:02}'.format(t[5])[self.digit - 2]

        self.set_digit(self.get_digit_array(uartCommand.digitValue[int(d)]))

def instructions():
    """
    Display the command menu and validate user input.

    Returns:
        tuple: A tuple containing the action (str) and value (str) entered by the user.
    """
    actions = ['c', 'd', 'e', 'l', 'r', 's', 't', 'w', 'q']

    while True:
        print("Enter a command:")
        print("\t(c)ycle through digits")
        print("\t(d)igit (d0-d9,dA-dF)")
        print("\t(e)xtend segment (e0-e6)")
        print("\t(l)uminosity (0-9)")
        print("\t(r)etract segment (r0-r6)")
        print("\t(s)peed (50-100)% of segment movement")
        print("\t(t)est digit")
        print("\t(w)ait time (15-30 milliseconds) of segment movement")
        print("\t(q)uit")
        cmd = input("command: ").strip()

        if not cmd:
            print("Invalid input. Please enter a command.")
            continue

        action = cmd[0].lower()
        if action not in actions:
            print(f"Invalid action '{action}'. Please enter a valid command.")
            continue

        value = cmd[1:].strip()
        if action in ['e', 'r', 'l', 's', 'w']:
            if not value.isdigit():
                print(f"Invalid value '{value}' for action '{action}'. Please enter a numeric value.")
                continue

        if action == 'd' and not (0 <= int(value, 16) <= 15):
            print(f"Invalid digit value '{value}'. Please enter a value between 0 and F.")
            continue

        if action in ['e', 'r'] and not (0 <= int(value) <= 6):
            print(f"Invalid segment value '{value}'. Please enter a value between 0 and 6.")
            continue

        if action == 'l' and not (0 <= int(value) <= 9):
            print(f"Invalid luminosity value '{value}'. Please enter a value between 0 and 9.")
            continue

        if action == 's' and not (10 <= int(value) <= 100):
            print(f"Invalid speed value '{value}'. Please enter a value between 10 and 100.")
            continue

        if action == 'w' and not (15 <= int(value) <= 30):
            print(f"Invalid wait time value '{value}'. Please enter a value between 15 and 30 milliseconds.")
            continue

        if action in ['c', 't']:
            value = '0'

        return action, value

def main():
    d = Digit(led_pins, LED_BRIGHTNESS_DEFAULT, motor_pins)
    helper = commandHelper()
    finished = False
    
    while not finished:
        seg, value = instructions()

        if seg == 'c':
            print("cycle through digits:")
            for i in range(0, 16):
                try:
                    a = helper.decodeHex(value=i)
                    print(f"digit=(0x{a:02x})")
                    digitArray = d.getDigitArray(uartCommand.digitValue[int(a)])
                    d.set_digit(digitArray)
                    time.sleep(1)
                except ValueError as ve:
                    print(f"ValueError during digit cycling: {ve}")
                except Exception as e:
                    print(f"Unexpected error during digit cycling: {e}")
        elif seg == 'd':
            print(f"digit=({value})")
            try:
                a = helper.decodeHex(value)
                digitArray = d.getDigitArray(uartCommand.digitValue[a])
                actuatorMoves = d.set_digit(digitArray)
                print(f"Digit set successfully. Actuator moves: {actuatorMoves}")
            except KeyError as ke:
                print(f"KeyError while setting digit: {ke}. Ensure the digit value is valid.")
            except ValueError as ve:
                print(f"ValueError while decoding digit: {ve}. Ensure the input is in the correct format.")
            except Exception as e:
                print(f"Unexpected error while setting digit: {e}")
        elif seg == 'e':
            try:
                i = int(value)
                print(f"extend segment=({i})")
                actuatorMoves = d.extend_segment(i)
            except ValueError as ve:
                print(f"ValueError while extending segment: {ve}")
            except Exception as e:
                print(f"Unexpected error while extending segment: {e}")
        elif seg == 'l':
            try:
                print(f"luminosity=({value})")
                d.brightness = float(value) / 10
            except ValueError as ve:
                print(f"ValueError while setting luminosity: {ve}")
            except Exception as e:
                print(f"Unexpected error while setting luminosity: {e}")
        elif seg == 'r':
            try:
                i = int(value)
                print(f"retract segment=({i})")
                actuatorMoves = d.retract_segment(i)
            except ValueError as ve:
                print(f"ValueError while retracting segment: {ve}")
            except Exception as e:
                print(f"Unexpected error while retracting segment: {e}")
        elif seg == 's':
            try:
                i = int(value)
                print(f"set_motor_speed({i})")
                d.motorspeed = i
            except ValueError as ve:
                print(f"ValueError while setting motor speed: {ve}")
            except Exception as e:
                print(f"Unexpected error while setting motor speed: {e}")
        elif seg == 't':
            try:
                actuatorMoves = d.dance()
                print(f"test actuator moves={actuatorMoves}")
            except Exception as e:
                print(f"Unexpected error during test dance: {e}")
        elif seg == 'w':
            try:
                i = int(value)
                print(f"set_wait_time({i})")
                d.waitTime = i / 100
            except ValueError as ve:
                print(f"ValueError while setting wait time: {ve}")
            except Exception as e:
                print(f"Unexpected error while setting wait time: {e}")
        else:
            finished = True
            print("quitting...")

if __name__ == "__main__":
    main()