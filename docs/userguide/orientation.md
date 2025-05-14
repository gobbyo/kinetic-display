# User Guide - Orientation

## Front of Display

Following the diagram below.

- **A** is Digit 0
- **B** is Digit 1
- **C** is Upper and lower colons
- **D** is Digit 2
- **E** is Digit 3

Each digit has seven segments A-G that extend or retract depending on the action.

When a segment extends, LEDs behind the segment provide lighting to give it a uniform glow. A Light Dependent Resistor (LDR) above Digit 1 in the back, senses the ambient light in the room causing the LEDs to dim or brighten. All extended segments with lit LEDs adjust to the given light level. The LEDs turn off when the segment retracts.

![orientation-1](../img/user-guide-orientation/orientation-1.webp)

The display has several actions allowing you to customize a scheduler which determines when and which item among the following is displayed:

1. **Local time** in 12 or 12 hour, both colons extended
    ![orientation-1b](../img/user-guide-orientation/orientation-1b.webp)
2. **Date** in month and day, both colons retracted
    ![orientation-2](../img/user-guide-orientation/orientation-2.webp)
3. **Internal temperature** in Celsius or Fahrenheit, upper colon extended, lower colon retracted
    ![orientation-3](../img/user-guide-orientation/orientation-3.webp)
4. **Internal humidity** in percent, upper colon extended, lower colon retracted
    ![orientation-4](../img/user-guide-orientation/orientation-4.webp)
5. **External temperature** in Celsius or Fahrenheit, lower colon extended, upper colon retracted
    ![orientation-5](../img/user-guide-orientation/orientation-5.webp)
6. **External humidity** in percent, lower colon extended, upper colon retracted
    ![orientation-6](../img/user-guide-orientation/orientation-6.webp)

7. **Digit Type** is a setting allowing you to show the digits as human or alien, see the [translation table for alien digits](../userguide/digittype.md). Below is a picture of the alien digit type.

    ![orientation-9](../img/user-guide-orientation/orientation-9.webp)

## Top of Display

The top profile of the display with the short-form stand. Optionally, you can install a long-form stand with a protective guard to protect curious cats from disrupting the power management system.
![orientation-8](../img/user-guide-orientation/orientation-8.webp)

## Back of Display

Following the picture below:

**A** = **Light Dependent Resistor (LDR)**. Senses the ambient light in the room causing the LEDs to dim or brighten. All extended segments with lit LEDs adjust to the given light level.

**B** = **On/Off switch**. The On/Off switch has different modes depending on the state of being plugged in or not. See the On/Off switch guide for details.

**C** = **Digital Humidity Temperature (DHT-22) sensor**. Allows for the display of the internal room temperature and humidity.

**D** = **Segment Actuator**. There are 30 total segment actuators including the colons.

**E** = **Digit Raspberry Pi Pico 2040 Micro Controller**. There are 4 **Picos**, one for each digit, numbered 0-3. The **Pico** acts as the central processing unit for the digit supporting the following functions:

- Sends control signals to the motor drivers for segment movement.
- Controls the LEDs for segment illumination.
- Communicates with the main conductor PCB via UART.

**F** = **Conductor and Colon Raspberry Pi Pico 2040 W Micro Controller**. The **Pico W** 2040 (conductor) operates the colons and serves as the central command and control for the display, performing the following functions:

- Sends commands to digits as to what to display (e.g., 0-9, A-F).
- Sends commands for the brightness of the digits.
- When in Admin mode, transmits its own Wi-Fi service to wirelessly change the display settings from a cell phone or computer.
- Manages the scheduler, which is the mechanism for displaying time, date, external temperature and humidity, and interior temperature and humidity.
- When connected to a Wi-Fi network, obtains its public-facing IP address, looks up the time zone it is located in, and sets the display to the local time.
- When connected to a Wi-Fi network, obtains the closest weather station and, depending on the scheduler, may display the external temperature and humidity.
- Manages the low power consumption mode by turning off the power to digits 0-3. When awakened, it turns on the power to digits 0-3.

**G** = **Barrel Jack for 12v Power Supply**. The stand containing the barrel jack also serves as the power management system for the display. There are different modes for the **On/Off** switch depending on the wall plug being plugged in when the switch is in its **On** position or its **Off** position. See the On/Off switch guide for details.

!!!note
    Plug the 12v power supply into the barrel jack BEFORE plugging the power supply into the wall plug.

![orientation-7](../img/user-guide-orientation/orientation-7.webp)
