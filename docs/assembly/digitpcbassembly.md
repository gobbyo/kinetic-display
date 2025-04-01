# Digit PCB Assembly

The display has 4 digits. The digits are numbered from right to left, 0-3, when looking at the front of display. The digit PCBs are digits 0, 2, and 3 whereas the controller PCB is digit 1 and includes the colons. The digit PCBs are the foundation of the display and serve several important functions:

- provides a mechanical backstop to the actuator's segment when retracting into the display
- provides a consistent distance of dispersion for the lighting of the segment, giving each segment a uniform glow rather than spots of light
- provides the traditional role of reducing the wiring, efficiently connects various electronic component minimizing the overall size, reliable, cost-effective, and consistent quality of the circuitry

This section details the assembly of digits 0, 2, and 3. Note the pictures below showing the fully assembled PCBs that will be covered in this section.

Front face fully assembled.
![digit pcb front face](../img/digitpcbassembly/1-digitpcbassembly-frontface.webp)
Back face fully assembled.
![digit pcb back face](../img/digitpcbassembly/1-digitpcbassembly-backface.webp)

## Prerequisites

- [Fabrication of the digit PCBs](../createandorder/pcb.md)
- Table of components and tools

***Table of components***

| Quantity | Component | Image |
| :--: | :------| :-----: |
| 4 | 16 pin IC socket | ![component-1](../img/component/component-1.webp)|
| 4 | L293D stepper motor driver | ![component-2](../img/component/component-2.webp)|
| 2 | 20 pin female header connector | ![component-3](../img/component/component-3.webp)|
| 1 | 20 pin single row breakaway male connector | ![component-4](../img/component/component-4.webp)|
| 2 | 2 Port PCB Mount Screw Terminal Block Connector Straight Pin | ![component-5](../img/component/component-5.webp)|
| 1 | 0.1μ farad ceramic capacitor | ![component-6](../img/component/component-6.webp)|
| 1 | 1μ farad electrolytic capacitor | ![component-7](../img/component/component-7.webp)|
| 28 | 5mm Flat top LED, anode long lead (any color) | ![component-8](../img/component/component-8.webp)|
| 1 | Raspberry Pi Pico with Headers | ![component-9](../img/component/component-9.webp)|
| 3 | Digit PCBs | See [labelling the digit PCBs](#label_the_digit_pcb) |

***Table of tools***

| Required | Tool | Image |
| :---: | :------- | :---: |
| Yes | Soldering station    | ![tool-4](../img/tools/tool-4.webp)|
| Yes | 0.8mm 1.76oz RoHS flux core solder | ![tool-1](../img/tools/tool-1.webp)|
| Yes | Mini flush cutters   | ![tool-6](../img/tools/tool-6.webp)|
| Yes | Isopropyl Alcohol | ![tool-3](../img/tools/tool-3.webp)|
| Yes | Cotton Facial Pads | ![tool-2](../img/tools/tool-2.webp)|
| No  | Label maker | ![tool-5s](../img/tools/tool-5.webp) |

## Label the Digit PCB

1. Using a label maker or piece of tape and pen, create two sets of 3 labels: "0", "2", and "3". Add the (**A**) label to the (**B**) FRONT FACING SIDE of each of the 3 digit PCBs as placed in the picture below. Also note that digit 0 (**C**) in the picture below is a completed digit PCB ready for mounting onto the display.
![digitpcb-2](../img/digitpcbassembly/2-digitpcbassembly.webp)
1. Add the (**A**) label to the (**B**) BACK FACING SIDE of each of the 3 digit PCBs as placed in the picture below.
![digitpcb-3](../img/digitpcbassembly/3-digitpcbassembly.webp)

## Add the 16 pin headers

1. From the front side of the digit PCB, (**A**) insert the 16 pin header into the through holes by aligning the notch with the digit PCB top silk layer outline of the 16 pins. The notch in the 16-pin header is used to ensure correct orientation when connecting the L293D motor driver. Carefully turn over the digit PCB while keeping the 16 pin header in the through holes.
![digitpcb-4](../img/digitpcbassembly/4-digitpcbassembly.webp)
1. (**A**) Solder the 16 pins and repeat the previous step until all 4 of the 16 pin headers are soldered into place.
![digitpcb-5](../img/digitpcbassembly/5-digitpcbassembly.webp)
1. From the back of the digit PCB, (**A**) cut off the soldered pins.
![digitpcb-6](../img/digitpcbassembly/6-digitpcbassembly.webp)
1. Touch up the clipped pins with a small bit of solder to make (**A**) smooth rounded beads instead of sharp points.
![digitpcb-7](../img/digitpcbassembly/7-digitpcbassembly.webp)
1. Clean up the soldered pins by removing the flux using a cotton pad dabbed with isopropyl alcohol. Repeat the previous step if you find your cotton pad is being torn from any protruding pins.
![digitpcb-8](../img/digitpcbassembly/8-digitpcbassembly.webp)

## Add the 28 LEDs

!!! note
    BEFORE SOLDERING LEDS ONTO YOUR DIGIT PCB, be sure to test your LEDs on a breadboard and use a digital camera to spot any variations in color when the LEDs are lit.
Below is a photo showing the color variation of blue 5mm LEDs within the same batch using a breadboards power rail with 2.63v. Note the (**A**) light blue LEDs and the (**B**) purple LEDs within the same blue batch of LEDs.
![blueLEDs](../img/digitpcbassembly/ledcolors.webp)

1. There are seven segments "A" through "G" each with four LEDs. From the front of the digit PCB, start with segment A by inserting the LED's (**A**) long lead (anode) into the "+" through hole. Repeat the process for all segment-A LEDs.
![digitpcbLEDs-1](../img/digitpcbassembly/1-digitpcbassembly-LED.webp)
1. Carefully turn over the digit PCB and rest it with the back facing up. Solder each LED pin onto the digit PCB, then (**A**) snip off the excess. Touch up the clipped pins with a small bit of solder to make smooth rounded beads instead of sharp points.
![digitpcbLEDs-3](../img/digitpcbassembly/3-digitpcbassembly-LED.webp)
1. Clean the flux off with a cotton pad dabbed in isopropyl alcohol.
![digitpcbLEDs-4](../img/digitpcbassembly/4-digitpcbassembly-LED.webp)
1. Repeat the previous steps for segments B through G until all 28 LEDs are soldered onto the PCB. The picture below is the front face of the digit with all 28 LEDs soldered into place.
![digitpcbLEDs-5](../img/digitpcbassembly/5-digitpcbassembly-LED.webp)

## Add the Motor Pins

1. Break out 7 pairs of 2.54mm male breakaway pins using needle nose pliers. 
![digitpcbmotorpins-2](../img/digitpcbassembly/2-digitpcbassembly-motorpins.webp)
1. On the back of the digit PCB, place the short end of the pin-pair into each actuator segment through hole (seg-A through seg-G).
![digitpcbmotorpins-3](../img/digitpcbassembly/3-digitpcbassembly-motorpins.webp)
1. On the front of the digit PCB motor solder pins into place.
![digitpcbmotorpins-4](../img/digitpcbassembly/4-digitpcbassembly-motorpins.webp)
1. Continuing on the front of the digit PCB, cut the pins flush on the pcb, then resolder the snipped pins to create smooth beads.
![digitpcbmotorpins-5](../img/digitpcbassembly/5-digitpcbassembly-motorpins.webp)
1. Clean off the flux residue using a cotton pad dabbed in isopropyl alcohol.
![digitpcbmotorpins-6](../img/digitpcbassembly/6-digitpcbassembly-motorpins.webp)

## Mount the L293D 16-pin IC Stepper Motor Drivers

1. From the front of the digit PCB, orient the motor driver so the notch (or pin 1) is aligned with the 16 pin header.
![digitpcbmotordriver1](../img/digitpcbassembly/1-digitpcbassembly-motordriver.webp)
1. CAREFULLY insert the motor driver into the 16 pin header and ensure none of the pins on the motor driver are bent or protruding from the 16 pin header.
![digitpcbmotordriver2](../img/digitpcbassembly/2-digitpcbassembly-motordriver.webp)
1. Repeat the install for the remaining motor drivers.

## Add the PCB Mount, Two port (2P) Terminal Block Connectors

1. On the front of the digit PCB, insert the PCB two port terminal block connector into the 5v through holes so the face of the connector where the wires are inserted points toward the LEDs on the PCB.
![digitpcbconnector-1](../img/digitpcbassembly/1-digitpcbassembly-connector.webp)
1. Solder the block terminal connector pins on the back of the digit PCB.
![digitpcbconnector-2](../img/digitpcbassembly/2-digitpcbassembly-connector.webp)
1. On the front of the digit PCB position the 2 port terminal block connector facing away from the LEDs. For PCBs labelled "2" & "3", insert the connector pins into the UART Tx-1/Rx-1 through holes. For the digit PCB labelled "0", insert the connector into the Tx-0/Rx-0 through holes.
![digitpcbconnector-3](../img/digitpcbassembly/3-digitpcbassembly-connector.webp)
1. On the back of the digit PCB, solder the remaining connector pins, cut the pins flush, resolder to a smooth bead, then remove the flux wth a cotton dabbed with isopropyl alcohol.
![digitpcbconnector-4](../img/digitpcbassembly/4-digitpcbassembly-connector.webp)

## Add the Electrolytic and Ceramic Capacitors

1. On the front of the digit PCB, align the electrolytic capacitor "-" sign opposite the "+" printed on the PCB for capacitor "c1", see the picture below. Insert the pins into the through holes, then turn the digit PCB over to the back side and solder the capacitor.
![digitpcbcapacitor-1](../img/digitpcbassembly/1-digitpcbassembly-capacitor.webp)
1. On the front of the digit PCB, insert the ceramic capacitor pins into the through holes titled "c2". Turn the digit PCB over to the back and solder the capacitor.
!!! note
    Ceramic capacitors do not have polarity and can be inserted in any direction.
![digitpcbcapacitor-2](../img/digitpcbassembly/3-digitpcbassembly-capacitor.webp)
4. On the back of the digit PCB, cut the pins flush, resolder to a smooth bead, then remove the flux with a cotton dabbed with isopropyl alcohol.
![digitpcbcapacitor-3](../img/digitpcbassembly/4-digitpcbassembly-capacitor.webp)

## Add the 20 pin Headers and Install the Microcontroller

1. On the back side of the PCB, place the two 20 pin headers into the through holes for "RASP1". Carefully turn over the PCB while keeping the 20 pin headers in the through holes.
![digitpcbmicrocontroller-1](../img/digitpcbassembly/1-digitpcbassembly-micro.webp)
1. Level the PCB and adjust the two 20 pin headers so they are perpendicular to the PCB. Solder the pins once in place. Snip all 40 of the pins flush, resolder each to a smooth bead, then remove the flux with a cotton dabbed with isopropyl alcohol.
![digitpcbmicrocontroller-2](../img/digitpcbassembly/2-digitpcbassembly-micro.webp)
1. Orient the Raspberry Pi Pico 2040 microcontroller so the USB port is facing in the same direction as the PCB silk screen, then gently mount the microcontroller onto the header.
![digitpcbmicrocontroller-3](../img/digitpcbassembly/3-digitpcbassembly-micro.webp)

Congratulations for assembling a digit PCB! Be sure to test the digit PCB before assembling the next one.

## Digits 0, 2, & 3 Schematics

![digitschematic-1](../img/digitpcbassembly/digit-schematic-motorcontrollers.png)
![digitschematic-2](../img/digitpcbassembly/digit-schematic-microcontroller.webp)
