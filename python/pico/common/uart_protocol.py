from machine import UART, Pin
import time
# This file contains the UART commands


class UARTChecksumError(Exception):
    pass

class UARTInvalidDigit(Exception):
    pass

class UARTInvalidAction(Exception):
    pass


class uartChannel():
    """
    A class to represent UART channels.
    Two UART channels are available on the Raspberry Pi Pico.
    UART0 channel is used for the hour tens and ones digits.
    UART1 channel is used for the minute tens and ones digits.

    Attributes
    ----------
    uart0 : int
        Represents UART channel 0.
    uart1 : int
        Represents UART channel 1.
    """
    uart0 = 0
    uart1 = 1

# UART pins:
class uartPins():
    uartTx0Pin = 0
    uartRx0Pin = 1
    uartTx1Pin = 4
    uartRx1Pin = 5


class hourMinutesDigit():
    """
    A class used to represent the digits of hours and minutes in a time format.
    Each digit is assigned a number, 0-3, with 0 being the right most digit 
    and 3 being the left most digit when facing the display.
    The colon controller is the conductor for all digits

    Attributes
    ----------
    hour_tens_digit : int
        The tens digit of the hour (default is 0)
    hour_ones_digit : int
        The ones digit of the hour (default is 1)
    minute_tens_digit : int
        The tens digit of the minute (default is 2)
    minute_ones_digit : int
        The ones digit of the minute (default is 3)
    conductor : int
        An additional attribute, purpose unspecified (default is 4)
    """
    hour_tens_digit = 0
    hour_ones_digit = 1
    minute_tens_digit = 2
    minute_ones_digit = 3
    conductor = 4
    
class uartActions():
    """
    uartActions class defines a set of constants representing different UART (Universal Asynchronous Receiver-Transmitter) actions.

    Attributes:
        setdigit (int): Command to set a digit.
        retractSegment (int): Command to retract a segment.
        extendSegment (int): Command to extend a segment.
        dance (int): Command to perform a dance action.
        ack (int): Command to acknowledge.
        setmotorspeed (int): Command to set the motor speed.
        setwaittime (int): Command to set the wait time.
        brightness (int): Command to set the brightness.
        hybernate (int): Command to put the device into hibernate mode.
    """
    setdigit = 0
    retractSegment = 1
    extendSegment = 2
    dance = 3
    ack = 4
    setmotorspeed = 5
    setwaittime = 6
    brightness = 7
    hybernate = 8

class uartCommand():
    """
    A class to represent a UART command.
    The UART protocol is a 3 character string
    The valid character set is 0-15 for the digit display
        0 = 	0011 1111   0x3F
        1 =	0000 0110   0x06
        2 =	0101 1011   0x5B
        3 =	0100 1111   0x4F
        4 =	0110 0110   0x66
        5 =	0110 1101   0x6D
        6 =	0111 1101   0x7D
        7 =	0000 0111   0x07
        8 =   0111 1111   0x7F
        9 =   0110 0111   0x67
        10 =   0110 0011   0x63  #degrees
        11 =   0101 1100   0x5C  #percent
        12 =   0011 1001   0x39  #celcius
        13 =   0111 0001   0x71  #farhenheit
        14 =   0100 0000   0x40  #minus
        15 =   0000 0000   0x00  #clear
    Test digits are defined as follows:
        0 = 	0010 0001   0x21
        1 =	0000 0011   0x03
        2 =	0011 0000   0x60
        3 =	0100 0010   0x42
        4 =	0100 0001   0x41
        5 =	0010 0010   0x22
        6 =	0111 0000   0x70
        7 =	0100 0011   0x43
        8 =   0110 0001   0x61
        9 =   0110 0010   0x62
        10 =   0010 0101   0x25
        11 =   0000 1101   0x0D
        12 =   0100 1001   0x49
        13 =   0100 0110   0x46
        14 =   0100 0101   0x45
        15 =   0000 0000   0x00  #clear
    This class provides methods to encode and set UART command strings, as well as properties to access
    digit values and test values.

    Attributes:
    -----------
    cmdStr : str
        The command string for the UART command.
    digitValue : list
        A list of hexadecimal values representing digit values.
    digitTest : list
        A list of hexadecimal values representing test digit values.
    digit : int
        The digit part of the UART command string.
    action : int
        The action part of the UART command string.
    value : int
        The value part of the UART command string.
    
    Methods:
    --------
    commandlen():
        Class method that returns the length of the command string.
    encode():
        Encodes the UART command string into a bytearray.
    set(uartCmdString):
        Sets the digit, action, and value attributes based on the UART command string.
    """
    @classmethod
    def commandlen(cls):
        return 5  # Define the length of the command string
    
    @property
    def cmdStr(self):
        return str(self._cmdStr)

    @cmdStr.setter
    def cmdStr(self, value: str):
        self._cmdStr = value
    
    @property
    def digitValue(self):
        return [0x3F,0x06,0x5B,0x4F,0x66,0x6D,0x7D,0x07,0x7F,0x67,0x63,0x5C,0x39,0x71,0x40,0x00]

    @property
    def digitTest(self):
        return [0x21,0x03,0x60,0x42,0x41,0x22,0x70,0x43,0x61,0x62,0x25,0x0D,0x49,0x46,0x45,0x00]

    def __init__(self, uartCmdString: str):
        self.cmdStr = uartCmdString
        self.set(uartCmdString)

    def encode(self):
        return bytearray('{0}{1}{2:02}'.format(self.digit, self.action, self.value), 'utf-8')
    
    def set(self,uartCmdString):
        self.digit = int(uartCmdString[0])
        self.action = int(uartCmdString[1])
        self.value = int(uartCmdString[2:])

class uartProtocol():
    """
    A class to handle UART communication protocol.

    Attributes:
    -----------
    uartCh : int
        The UART channel to use (e.g., uartChannel.uart0 or uartChannel.uart1).
    baudRate : int
        The baud rate for the UART communication.
    uart : UART
        The UART instance initialized with the specified channel and baud rate.
    
    Methods:
    --------
    __init__(uartCh, baudRate):
        Initializes the uartProtocol instance with the specified UART channel and baud rate.
    clearQueue():
        Clears the UART receive buffer if there is any data available.
    sendCommand(uartCmd):
        Sends a command over UART after encoding it to bytes.
    receiveCommand():
        Receives a command from UART, validates it, and returns a uartCommand instance if valid.
    """
    def __init__(self, uartCh, baudRate):
        self.uartCh = uartCh
        self.baudRate = baudRate
        
        if uartCh == uartChannel.uart0:
            self.uart = UART(0)
            self.uart.init(uartCh, baudRate, rx=Pin(uartPins.uartRx0Pin), tx=Pin(uartPins.uartTx0Pin), txbuf=4, rxbuf=4)
        else:
            self.uart = UART(1)
            self.uart.init(uartCh, baudRate, rx=Pin(uartPins.uartRx1Pin), tx=Pin(uartPins.uartTx1Pin), txbuf=4, rxbuf=4)

    def clearQueue(self):
        if self.uart.any() > 0:
            a = self.uart.readline()
            print("clearQueue: {0}".format(a))

    def sendCommand(self, uartCmd):
        b = uartCmd.encode()
        print("sendCommand: {0}".format(b))
        self.uart.write(b)

    def receiveCommand(self):
        for i in range(20):
            if self.uart.any() > 0:
                uart_cmd_instance = uartCommand("00000")  # Create an instance with a default command string
                b = bytearray(uart_cmd_instance.cmdStr, 'utf-8')  # Ensure correct length
                self.uart.readinto(b)
                if b == bytearray(b'\x00000'):
                    return None
                try:
                    s = b.decode('utf-8')
                    print("receiveCommand: {0}".format(s))
                    uartCmd = uartCommand(s)  # Ensure uartCommand is initialized with a string
                    helper = commandHelper()
                    if helper.validate(uartCmd):
                        return uartCmd
                except ValueError:
                    print("receiveCommand: ValueError")
                except Exception as e:
                    print("receiveCommand error: {0}".format(e))
                return None
        return None

class commandHelper():
    """
    A helper class for UART command operations including encoding, decoding, and validation.
    Attributes:
    ----------
    baudRate : list
        A list of standard baud rates for UART communication.
    Methods:
    -------
    decodeHex(value):
        Decodes a single hexadecimal character (0-9, A-F) to its integer value.
    encodeHex(value):
        Encodes an integer value (0-15) to its hexadecimal character representation.
    validate(uartCmd):
        Validates the structure and values of a UART command object.
    """
    baudRate = [9600, 19200, 38400, 57600, 115200]
    
    def decodeHex(self, value):
        returnVal = value
        if value == "A":
            returnVal = 10
        elif value == "B":
            returnVal = 11
        elif value == "C":
            returnVal = 12
        elif value == "D":
            returnVal = 13
        elif value == "E":
            returnVal = 14
        elif value == "F":
            returnVal = 15
        return int(returnVal)

    def encodeHex(self, value):
        v = int(value)
        if v < 10:
            return '{0}'.format(value)
        if v > 15:
            return 'E'
        return str(hex(v)).upper()[2:]
    
    def validate(self, uartCmd):
        if len(uartCmd.cmdStr) != uartCommand.commandlen():
            raise UARTChecksumError("Invalid uartCommand length = {0}".format(len(uartCmd.cmdStr)))
        if (uartCmd.digit < 0) or (uartCmd.digit > hourMinutesDigit.conductor):
            raise UARTInvalidDigit("Invalid uartCommand digit = {0}".format(uartCmd.digit))
        return True

def main():
    ch = 0
    uartch = input("Enter UART channel (0 or 1): ")
    if uartch == '1':
        ch = 1
    uart = uartProtocol(ch, commandHelper.baudRate[3])

    while True:
        cmdStr = input("Send command string [Digit(0-3) Action(0-9) Value(0-99)]: ")
        cmd = uartCommand(cmdStr)
        uart.sendCommand(cmd)
        time.sleep(0.05)
        cmd = uart.receiveCommand()
        if cmd is not None:
            print("uart{0} command received: {1}".format(ch, cmd.cmdStr))

if __name__ == "__main__":
    main()