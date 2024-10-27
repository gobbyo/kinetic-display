from uart_protocol import uartProtocol, uartChannel, uartCommand, commandHelper, uartActions
from dht11 import DHT11, InvalidChecksum, InvalidPulseCount
from syncRTC import syncRTC
from machine import Pin, RTC, ADC
import time

dhtPowerpin = 16
hybernateswitchPin = 18
powerRelayPin = 19
photoresistorPin = 28 # Light Dependent Resistor Part GL5516
dhtPin = 27

# This class manages the hardware components of the system, including:
# - UART communication (uart0 and uart1)
# - Photoresistor for ambient light sensing
# - DHT11 sensor for temperature and humidity measurements
# - RTC (Real-Time Clock) for timekeeping
# - Hybernate switch for power management
# - Power relay for controlling power to components
# - LED colon display
# It provides methods to initialize the hardware, read sensor data,
# and control various components of the system.
class HardwareManager:
    def __init__(self):
        self.uart0 = None
        self.uart1 = None
        self.photoresistor = None
        self.dht11 = None
        self.rtc = None
        self.hybernate_switch = None
        self.power_relay = None
        self.light = 0

    def initialize_hardware(self): # Initialize the hardware
        self.dht11 = DHT11(Pin(dhtPin))
        self.hybernate_switch = Pin(hybernateswitchPin, Pin.IN, Pin.PULL_DOWN)
        self.powerRelay = Pin(powerRelayPin, Pin.OUT)
        self.rtc = RTC()
        self.uart0 = uartProtocol(uartChannel.uart0, commandHelper.baudRate[3])
        time.sleep(.75)
        self.uart1 = uartProtocol(uartChannel.uart1, commandHelper.baudRate[3])
        time.sleep(.75)
        self.photoresistor = ADC(Pin(photoresistorPin))
        self.powerpin = Pin(dhtPowerpin, Pin.OUT)

    def read_light_level(self):
        high = 65535 #max value for 16 bit ADC
        range = high/2 #half of max value
        k = high - self.photoresistor.read_u16() #calculate the difference between max and actual value
        percent = (k/range)*10 #calculate the range as 0 to 10
        self.light = 10-int(round(percent,0)) #calculate the light level
        if self.light >= 10:
            self.light = 9
        elif self.light <= 0:
            self.light = 1
        return self.light

    def read_indoor_temp_humidity(self):
        self.powerpin.on()
        time.sleep(1)
        self.dht11.measure()
        self.powerpin.off()
        return self.dht11.temperature, self.dht11.humidity

    def get_current_time(self): # Get the current time from the RTC after it has been set by the syncRTC function
        dt = self.rtc.datetime()
        return dt
    
    def power_relay_on(self): # Turn on the power relay
        self.powerRelay.on()

    def power_relay_off(self): # Turn off the power relay
        self.powerRelay.off()
    
    def hybernate_switch(self): # Read the state of the hybernate switch
        return self.hybernate_switch.value()

#    This function serves as a basic test and demonstration of the HardwareManager's capabilities,
#    continuously monitoring light levels and indoor climate conditions
def main():
    hw = HardwareManager()
    hw.initialize_hardware()
    while True:
        print("light level: {0}".format(hw.read_light_level()))
        try:
            time.sleep(1)
            tempHumid = hw.read_indoor_temp_humidity()
            print(tempHumid)
            c = int(tempHumid[0])
            humidity = int(tempHumid[1])
            f = '{0:02}'.format(int((9/5)*tempHumid[0]+32))
            print("{0}C, {1}F, {2}%".format(c, f, humidity))
        except InvalidChecksum:
            print("Invalid checksum")
        except InvalidPulseCount:
            print("Invalid pulse count")
        finally:
            time.sleep(2)

if __name__ == "__main__":
    main()