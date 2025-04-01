# Controller and Digit 1 PCB Assembly

Digit 1 and the colons are on a single PCB. Digit 1 is identical to digits 0, 2, and 3 except it is contained on a single PCB with the colons. The controller operates the colons and is the central command and control for the display performing the following functions:

- Sends commands to digits as to what to display (i.e. 0-9, A-F)
- Sends commands for the brightness of the digits
- When in the Admin mode, it will transmit its own wifi service that provides a way to change the display settings
- Manages the scheduler, which is the mechanism for displaying time, date, external temperature and humidity, and interior temperature and humidity.
- When connected to a wifi network, it will obtain its public facing IP address, look up the time zone it is located in, and set the display to the local time
- When connected to a wifi network, it will obtain the closest weather station and, depending on the scheduler, may display the external temperature and humidity.
- Manages the low power consumption mode by turning off the power to digits 0-3.  When awakened, it will turn back on the power to digits 0-3.

Below is the fully assembled, front face of the controller PCB.
![front-face-controller-pcb](../img/controllerpcb/fullyassembled-frontface.webp)
Below is the fully assembled, back side of the controller PCB.
![back-face-controller-pcb](../img/controllerpcb/fullyassembled-backface.webp)

## Prerequisites

- [Fabrication of the digit PCBs](../createandorder/pcb.md)
- Table of components and tools

***Table of components***

| Quantity | Component | Image |
| :--: | :------| :-----: |
| 5 | 16 pin IC socket | ![component-1](../img/component/component-1.webp)|
| 5 | L293D stepper motor driver | ![component-2](../img/component/component-2.webp)|
| 4 | 20 pin female header connector | ![component-3](../img/component/component-3.webp)|
| 1 | 20 pin single row breakaway male connector | ![component-4](../img/component/component-4.webp)|
| 6 | 2 Port PCB Mount Screw Terminal Block Connector Straight Pin | ![component-5](../img/component/component-5.webp)|
| 2 | 0.1μ farad ceramic capacitor | ![component-6](../img/component/component-6.webp)|
| 2 | 1μ farad electrolytic capacitor | ![component-7](../img/component/component-7.webp)|
| 28 | 5mm Flat top LED, anode long lead (any color) | ![component-8](../img/component/component-8.webp)|
| 2 | 3mm Flat top LED, anode long lead (any color) | ![component-17](../img/component/component-17.webp)|
| 1 | Raspberry Pi Pico 2040 with Headers | ![component-9](../img/component/component-9.webp)|
| 1 | Raspberry Pi Pico W 2040 with Headers | ![component-9](../img/component/component-16.webp)|
| 1 | Controller PCB | See next section |

***Table of tools***

| Required | Tool | Image |
| :---: | :------- | :---: |
| Yes | Soldering station    | ![tool-4](../img/tools/tool-4.webp)|
| Yes | 0.8mm 1.76oz RoHS flux core solder | ![tool-1](../img/tools/tool-1.webp)|
| Yes | Mini flush cutters   | ![tool-6](../img/tools/tool-6.webp)|
| Yes | Isopropyl Alcohol | ![tool-3](../img/tools/tool-3.webp)|
| Yes | Cotton Facial Pads | ![tool-2](../img/tools/tool-2.webp)|

## Assemble Digit One

On the controller PCB, follow the instructions from the digit PCB assembly to assemble digit one.

1. On the front face of the controller PCB, [add the 16 pin headers](digitpcbassembly.md#add_the_16_pin_headers) as previously completed for the digit PCBs. Note the highlighted sections in the picture below that you'll add an additional (5th) 16 pin header to the controller PCB.
![1-controllerpcb](../img/controllerpcb/1-controllerpcb.webp)
1. On the front face of the controller PCB, [add the 28 5mm LEDs](digitpcbassembly.md#add_the_28_leds) as previously completed for the digit PCBs. Do not solder the 5mm LED into the **Top-LED1** or **LWR-LED1** location on the controller PCB. Instructions later in this section will detail how to install the 3mm LEDs into the "Top-LED1" and "LWR-LED1" locations.
![2-controllerpcb](../img/controllerpcb/2-controllerpcb.webp)
1. On the back face of the controller PCB, [add the motor pins](digitpcbassembly.md#add_the_motor_pins). Note the highlighted sections in the picture below that there are two additional motor pins (pairs) you'll need to add, and an additional 3-pin connector for the Digital Humidity Temperature (DHT) sensor.
![3-controllerpcb](../img/controllerpcb/3-controllerpcb.webp)

## Add the 3mm Flat Top LEDs for the Colon Segments

In addition to the soldering equipment you needed when previously mounting the 5mm flat top LEDs, you'll need the two 3D printed colon segments, label **A** in the diagram below, as fabricated in the [3D print the display parts](../createandorder/3dprints.md) document.
![6-controllerpcb](../img/controllerpcb/6-controllerpcb.webp)

1. Following label **B** in the diagram above, insert the 3mm flat top LEDs into **Top-LED1** and **LWR-LED1** on the front face of the controller PCB. Follow the same 5mm LED install process and be sure to insert the long lead anode of the LED into the **+** through hole.
2. Following the diagram below, slide the colon segments over the 3mm LED. Note the lower base of the LED lense may need to be lightly sanded with 300 grid sandpaper if it does not easily slide into the colon segment.
![7-controllerpcb](../img/controllerpcb/7-controllerpcb.webp)
3. On the back side of the controller PCB, align the colon segment so its square base is positioned into the square hole of the PCB.
![8-controllerpcb](../img/controllerpcb/8-controllerpcb.webp)
4. Solder the 3mm LEDs into place.
![9-controllerpcb](../img/controllerpcb/9-controllerpcb.webp)
5. Optionally you can use a metric ruler to verify the LEDs protrude perpendicular from the PCB and are 14mm from the PCB to the top of the lens of the LED. This optional step insures the proper length of the 3mm LEDs.
![10-controllerpcb](../img/controllerpcb/10-controllerpcb.webp)

## Solder the PNP and NPN transistors

1. Following the diagram below, solder the s8550D PNP transistor into the through hole (mis-) labelled 2N8550 on the front face of the controller PCB.
![4-controllerpcb](../img/controllerpcb/4-controllerpcb.webp)
1. Following the diagram below, solder the 2N2222A PNP transistor into the though hole labelled 2N2222 on the front face of the controller PCB.
![5-controllerpcb](../img/controllerpcb/5-controllerpcb.webp)

## Mount the L293D 16-pin IC Motor Drivers

1. On the front face of the controller PCB, [mount the L293D 16-pin IC Stepper Motor Drivers](digitpcbassembly/#mount_the_l293d_16_pin_ic_stepper_motor_drivers) as previously completed for the digit PCBs.
![5-controllerpcb-motordriverIC](../img/digitpcbassembly/1-digitpcbassembly-motordriver.webp)

## Add the 20-pin Headers for the Pico and PicoW

1. On the back side of the PCB, place the four 20 pin headers into the through holes for **RASP1** and **RASP2**. Carefully turn over the PCB while keeping the 20 pin headers in the through holes. Level the PCB and adjust the two 20 pin headers so they are perpendicular to the PCB. Solder the pins once in place. Snip all 40 of the pins flush, resolder each to a smooth bead, then remove the flux with a cotton dabbed with isopropyl alcohol.
![11-controllerpcb](../img/controllerpcb/11-controllerpcb.webp)

## Solder the surface mount resistors

1. On the back side of the PCB, solder the two 10kΩ resistors onto the pads marked **R2 10k** and **R3 10k** located between the top and bottom rows of teh 20-pin headers.
![12-controllerpcb](../img/controllerpcb/12-controllerpcb.webp)

## Install Six, two port (2P) Terminal Block Connectors

There are five 2P terminal block connectors on the front face of the PCB, and one on the back side.
The diagram below shows a completed install of the terminal block connectors on the front face of the controller PCB. Note the arrows pointing in the direction of the terminal block connector where the wires are inserted into the ports. When following the steps below you'll position the front face of the controller PCB up and work your way from the bottom left corner to the bottom right corner.
![13-controllerpcb](../img/controllerpcb/13-controllerpcb.webp)

1. Follow the diagram below and insert the 2P terminal block connector into the **5v-D1** through holes with the connector facing LEFT, then solder it into place.
![14-controllerpcb](../img/controllerpcb/14-controllerpcb.webp)
1. Follow the diagram below and insert the 2P terminal block connector into the **U7, Tx-1 Rx-1** through holes with the connector facing LEFT, then solder it into place.
![15-controllerpcb](../img/controllerpcb/15-controllerpcb.webp)
1. Follow the diagram below and insert the 2P terminal block connector into the **U7, GPIO19 Tx-0** through holes with the connector facing LEFT, then solder it into place.
![16-controllerpcb](../img/controllerpcb/16-controllerpcb.webp)
1. Follow the diagram below and insert the 2P terminal block connector into the **UART1, Tx-0 Rx-0** through holes with the connector facing RIGHT, then solder it into place.
![17-controllerpcb](../img/controllerpcb/17-controllerpcb.webp)
Follow the diagram below, insert the 2P terminal block connector into the **5v-D0** through holes with the connector facing LEFT, then solder it into place.
![18-controllerpcb](../img/controllerpcb/18-controllerpcb.webp)
1. Position the back face of the PCB up and insert the 2P terminal block connector into the **5v-OUT** through holes with the connector facing RIGHT, then solder it into place.
![19-controllerpcb](../img/controllerpcb/19-controllerpcb.webp)

## Add the Electrolytic and Ceramic Capacitors

1. On the front of the digit PCB, align the electrolytic capacitor "-" sign opposite the "+" printed on the PCB for capacitor "c1", see the picture below. Insert the pins into the through holes, then turn the digit PCB over to the back side and solder the capacitor.
![digitpcbcapacitor-1](../img/digitpcbassembly/1-digitpcbassembly-capacitor.webp)
1. On the front of the digit PCB, insert the ceramic capacitor pins into the through holes titled "c2". Turn the digit PCB over to the back and solder the capacitor.
!!! note
    Ceramic capacitors do not have polarity and can be inserted in any direction.
![digitpcbcapacitor-2](../img/digitpcbassembly/3-digitpcbassembly-capacitor.webp)
4. On the back of the digit PCB, cut the pins flush, resolder to a smooth bead, then remove the flux with a cotton dabbed with isopropyl alcohol.
![digitpcbcapacitor-3](../img/digitpcbassembly/4-digitpcbassembly-capacitor.webp)



Congratulations for assembling a digit PCB! Be sure to test the digit PCB before assembling the next one.

## Controller and Digit 1 Schematics

![digitschematic-1](../img/digitpcbassembly/digit-schematic-motorcontrollers.png)
![digitschematic-2](../img/digitpcbassembly/digit-schematic-microcontroller.webp)
