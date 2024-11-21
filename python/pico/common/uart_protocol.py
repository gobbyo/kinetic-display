from machine import UART, Pin
import time
import uasyncio as asyncio  # Import uasyncio for async operations
# This file contains the UART commands

class UARTChecksumError(Exception):
    pass

class UARTInvalidDigit(Exception):
    pass

class UARTInvalidAction(Exception):
    pass

# Two UART channels are available on the Raspberry Pi Pico.
# UART0 channel is used for the hour tens and ones digits.
# UART1 channel is used for the minute tens and ones digits.
class uartChannel():
    uart0 = 0
    uart1 = 1

# UART pins:
class uartPins():
    uartTx0Pin = 0
    uartRx0Pin = 1
    uartTx1Pin = 4
    uartRx1Pin = 5

# Each digit is assigned a number, 0-3, with 0 being the leftmost digit 
# and 3 being the rightmost digit when facing the display.
# The colon controller is the conductor for all digits
class hourMinutesDigit():
    hour_tens_digit = 0
    hour_ones_digit = 1
    minute_tens_digit = 2
    minute_ones_digit = 3
    conductor = 4
    
class uartActions():
    setdigit = 0
    retractSegment = 1
    extendSegment = 2
    dance = 3
    ack = 4
    setmotorspeed = 5
    setwaittime = 6
    brightness = 7
    hybernate = 8

# The UART protocol is a 3 character string
# The valid character set is 0-15 for the digit display
    # 0 = 	0011 1111   0x3F
    # 1 =	0000 0110   0x06
    # 2 =	0101 1011   0x5B
    # 3 =	0100 1111   0x4F
    # 4 =	0110 0110   0x66
    # 5 =	0110 1101   0x6D
    # 6 =	0111 1101   0x7D
    # 7 =	0000 0111   0x07
    # 8 =   0111 1111   0x7F
    # 9 =   0110 0111   0x67
    # 10 =   0110 0011   0x63  #degrees
    # 11 =   0101 1100   0x5C  #percent
    # 12 =   0011 1001   0x39  #celcius
    # 13 =   0111 0001   0x71  #farhenheit
    # 14 =   0100 0000   0x40  #minus
    # 15 =   0000 0000   0x00  #clear

# Test digits are defined as follows:
    # 0 = 	0010 0001   0x21
    # 1 =	0000 0011   0x03
    # 2 =	0011 0000   0x60
    # 3 =	0100 0010   0x42
    # 4 =	0100 0001   0x41
    # 5 =	0010 0010   0x22
    # 6 =	0111 0000   0x70
    # 7 =	0100 0011   0x43
    # 8 =   0110 0001   0x61
    # 9 =   0110 0010   0x62
    # 10 =   0010 0101   0x25
    # 11 =   0000 1101   0x0D
    # 12 =   0100 1001   0x49
    # 13 =   0100 0110   0x46
    # 14 =   0100 0101   0x45
    # 15 =   0000 0000   0x00  #clear

class uartCommand():
    cmdStr = '0000'
    len = len(cmdStr)
    digitValue = [0x3F,0x06,0x5B,0x4F,0x66,0x6D,0x7D,0x07,0x7F,0x67,0x63,0x5C,0x39,0x71,0x40,0x00]
    digitTest = [0x21,0x03,0x60,0x42,0x41,0x22,0x70,0x43,0x61,0x62,0x25,0x0D,0x49,0x46,0x45,0x00]
    def __init__(self, uartCmdString):
        self.cmdStr = uartCmdString
        self.set(uartCmdString)
    def encode(self):
        return bytearray('{0}{1}{2:02}'.format(self.digit, self.action, self.value), 'utf-8')
    def set(self,uartCmdString):
        self.digit = int(uartCmdString[0])
        self.action = int(uartCmdString[1])
        self.value = int(uartCmdString[2:])

class uartProtocol():
    def __init__(self, uartCh, baudRate):
        self.uartCh = uartCh
        self.baudRate = baudRate
        
        if uartCh == uartChannel.uart0:
            self.uart = UART(0)
            self.uart.init(uartCh, baudRate, rx=Pin(uartPins.uartRx0Pin), tx=Pin(uartPins.uartTx0Pin), txbuf=4, rxbuf=4)
        else:
            self.uart = UART(1)
            self.uart.init(uartCh, baudRate, rx=Pin(uartPins.uartRx1Pin), tx=Pin(uartPins.uartTx1Pin), txbuf=4, rxbuf=4)

    async def clearQueue(self):
        if self.uart.any() > 0:
            a = self.uart.readline()
            print("clearQueue: {0}".format(a))

    async def sendCommand(self, uartCmd):
        b = uartCmd.encode()
        print("sendCommand: {0}".format(b))
        self.uart.write(b)
        await asyncio.sleep(0)  # Yield control to the event loop

    async def receiveCommand(self):
        for i in range(20):
            await asyncio.sleep(0.1)  # Non-blocking sleep
            if self.uart.any() > 0:
                b = bytearray(uartCommand.cmdStr, 'utf-8')
                self.uart.readinto(b)
                if b == bytearray(b'\x00000'):
                    return None
                try:
                    s = b.decode('utf-8')
                    print("receiveCommand: {0}".format(s))
                    uartCmd = uartCommand(s)
                    if commandHelper.validate(uartCmd):
                        return uartCmd
                except ValueError:
                    print("receiveCommand: ValueError")
                    return None
                except Exception as e:
                    print("receiveCommand error: {0}".format(e))
                    return None
        return None

class commandHelper():
    baudRate = [9600, 19200, 38400, 57600, 115200]
    # uart command tool to decode hex values
    def decodeHex(value):
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

    # uart command tool to encode hex values
    def encodeHex(value):
        v = int(value)
        if v < 10:
            return '{0}'.format(value)
        if v > 15:
            return 'E'
        return str(hex(v)).upper()[2:]
    # uart command validation
    def validate(uartCmd):
        if len(uartCmd.cmdStr) != uartCommand.len:
            raise UARTChecksumError("Invalid uartCommand length = {0}".format(len(uartCmd.cmdStr)))
            #return False
        if (uartCmd.digit < 0) or (uartCmd.digit > hourMinutesDigit.conductor):
            raise UARTInvalidDigit("Invalid uartCommand digit = {0}".format(uartCmd.digit))
            #return False
        #if (uartCmd.action < 0) or (uartCmd.action > 8):
        #    raise UARTInvalidAction("Invalid uartCommand action = {0}".format(uartCmd.action))
            #return False
        return True

async def main():
    ch = 0
    uartch = input("Enter UART channel (0 or 1): ")
    if uartch == '1':
        ch = 1
    uart = uartProtocol(ch, commandHelper.baudRate[3])

    while True:
        cmdStr = input("Send command string [Digit(0-3) Action(0-9) Value(0-99)]: ")
        cmd = uartCommand(cmdStr)
        await uart.sendCommand(cmd)
        await asyncio.sleep(0.05)
        cmd = await uart.receiveCommand()
        if cmd is not None:
            print("uart{0} command received: {1}".format(ch, cmd.cmdStr))

if __name__ == "__main__":
    asyncio.run(main())