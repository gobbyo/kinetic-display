# Buck Module Wiring

Buck converters are essential for converting 12V DC to 5V DC because they efficiently step down the voltage while minimizing energy loss. Unlike linear regulators, which dissipate excess voltage as heat, buck converters use high-frequency switching and inductors to transfer energy more efficiently. This makes them ideal for powering sensitive electronics like micro controllers and LEDs, as they provide stable output voltage, reduce heat generation, and improve overall system reliability.

This guide provides detailed instructions for assembling and wiring DC to DC variable buck converter modules in a Kinetic Display system. It includes a list of required components and tools, step-by-step guidance for wiring and securing the modules, and calibration instructions to ensure proper voltage output.

1. **Correct Wiring**: Proper routing and connection of wires are critical to ensure the display functions correctly. Incorrect wire lengths or connections can lead to assembly issues or electrical faults.
1. **Voltage Calibration**: The buck converters step down the input voltage from 12V to a stable 5.0-5.1V output. Calibration ensures the modules provide the correct voltage to prevent damage to connected components or malfunctions.
1. **Safety Measures**: Follow anti-static precautions and use proper tools to avoid damaging sensitive electronics during assembly.

This guide is essential for ensuring the reliability and safety of the Kinetic Display system.

## Prerequisites

- 3D print the Conductor and Digits TPU gaskets.
- 3D print the Display stand.

***Table of components***

| Quantity | Component | Image |
| :--: | :------ | :-----: |
| 5 | DC to DC variable buck converter module | ![component-31](../img/component/component-31.webp) |
| 1 | 12V 5A Power Supply, AC DC Converter 100-220V to 12 Volt 5 Amp Transformer 5.5x2.1mm Plug | ![component-33](../img/component/component-33.webp) |
| 10M | White 28 AWG Gauge Flexible Silicone Rubber Electric Wire | ![component-28](../img/component/component-28.webp) |
| 10M | Black 28 AWG Gauge Flexible Silicone Rubber Electric Wire | ![component-29](../img/component/component-29.webp) |
| 50cm | (optional) 28 AWG Gauge heat shrink | ![component-30](../img/component/component-30.webp) |
| 10 | M1.7x6mm Cross Round Head with Washer Self Tapping Screw 304 Stainless Steel Screws | ![component-32](../img/component/component-32.webp) |

***Table of tools***

| Required | Tool | Image |
| :---: | :------- | :---: |
| Yes | Multimeter | ![tool-16](../img/tools/tool-16.webp) |
| Yes | Soldering station | ![tool-4](../img/tools/tool-4.webp) |
| Yes | 0.8mm 1.76oz RoHS flux core solder | ![tool-1](../img/tools/tool-1.webp) |
| Yes | Mini flush cutters | ![tool-6](../img/tools/tool-6.webp) |
| Yes | Wire stripper | ![tool-9](../img/tools/tool-9.webp) |
| No | Label maker | ![tool-5](../img/tools/tool-5.webp) |

## PCB and Stand Layout

This section ensures wiring for the PCBs is oriented for the mounting of the buck modules and wiring.

1. Remove the Raspberry Pi Pico and Pico W 2040 from the PCBs. These will be added later when it is safe to do so.
2. Lay the PCBs face up with Digit 0 on the far right and Digit 3 on the far left. Position the stand below the PCBs so the barrel jack is between the Conductor and Digit 1 PCB and Digit 2 PCB.  
   ![buckmodulesandwiring-1](../img/buckmoduleassembly/buckmoduleassembly-1.webp)
3. Place the TPU gaskets on the PCBs. Note that the wiring lays over the gaskets.  
   ![buckmodulesandwiring-2](../img/buckmoduleassembly/buckmoduleassembly-2.webp)

## Wiring the Buck Modules

This section details wiring the buck converter modules to the PCBs. Be sure to follow the instructions to get the wire lengths correct. Incorrect lengths may result in wires being too short or too long, preventing the display face from fitting correctly. Each buck module has an `In +` and `In -` on one side for the 12V input, and an `Out +` and `Out -` on the opposite side for the converted 5V output. This section also covers how to calibrate the variable buck module to provide 5.0V to 5.1V output.

The picture below is the wiring diagram for the buck converter modules:  
![buckmodulesandwiring-wiring](../img/buckmoduleassembly/buckmoduleassembly-wire.webp)

The picture below shows the completed wiring of the buck converter modules. The order of installation is **1, 2, 3** on the right, followed by **4** and **5** on the left:  
![buckmodulesandwiring](../img/buckmoduleassembly/buckmoduleassembly-complete.webp)

!!! warning
    Use anti-static mats, an ESD wristband, and a grounding wire for the remainder of the Kinetic Display electronics assembly.

### Digits and Conductor

1. Following the picture below, place a buck converter module for Digit 0 on the rightmost support on the display stand. Strip 3mm of insulation from the black and white 28 AWG wire while on the roll starting then tin the stripped end with solder. **(A)** Route the two wires from the 5V terminal block connector on the Digit 0 PCB. **(B)** Slide two 3cm sections of heat shrink on the two wires but DO NOT APPLY HEAT, then **(C)** continue routing the wire around the relay, under the power management PCB and through the port on the PCB stand. **(D)** Finish unwinding the wire when you reach the end of the buck module as shown in the picture. Now that the length of wire is known from its route, snip off the wires next to the terminal block connector. **(A)** Strip 3mm of insulation then tin the stripped end with solder. Connect the white wire to the `+` on the `5V` terminal block connector and the black wire onto the `-`.  
   ![buckmodulesandwiring-3](../img/buckmoduleassembly/buckmoduleassembly-3.webp)
1. Following the picture below, turn the Digit 0 buck module over to its backside and solder the white wire onto the `Out +` pad and the black wire onto the `Out -` pad.  
   ![buckmodulesandwiring-4](../img/buckmoduleassembly/buckmoduleassembly-4.webp)
1. Following the picture below, turn the Digit 0 buck module 180 degrees while having its backside facing up. Strip 3mm of insulation from the black and white 28 AWG wire while on the roll starting then tin the stripped end with solder. Solder the white wire onto the buck module's `In +` pad and the black wire onto the `In -` pad.  
   ![buckmodulesandwiring-5](../img/buckmoduleassembly/buckmoduleassembly-5.webp)
1. Turn the Digit 0 buck module over and secure it with M1.7x6mm self tapping screws onto the rightmost module supports on the display stand.  
   ![buckmodulesandwiring-6](../img/buckmoduleassembly/buckmoduleassembly-6.webp)
1. Route the Digit 0 white and black wire to the power management PCB `C-12V-1` terminal block connector, provide about 10mm extra length in the wire before cutting them. Strip 3mm of insulation then tin the stripped end with solder. Connect the white wire to the `+` on the `C-12V-1` and the black wire onto the `-`.  
   ![buckmodulesandwiring-7](../img/buckmoduleassembly/buckmoduleassembly-7.webp)
1. Following the picture below, place a buck converter module for Digit 1 to the left of the Digit 0 module. Strip 3mm of insulation from the black and white 28 AWG wire while on the roll starting then tin the stripped end with solder. Starting with the Digit 1 PCB, **(A)** Route the two wires from the 5V terminal block connector. **(B)** Slide one 3cm section of heat shrink on the two wires but DO NOT APPLY HEAT, then **(C)** continue routing the wire around the relay, under the power management PCB and through the port on the PCB stand. **(D)** Finish unwinding the wire when you reach the end of the second buck module as shown in the picture. Now that the length of wire is known from its route, snip off the wires next to the terminal block connector **(A)**. Strip 3mm of insulation then tin the stripped end with solder. Connect the white wire to the `+` on the `5V` terminal block connector and the black wire onto the `-`.  
   ![buckmodulesandwiring-8](../img/buckmoduleassembly/buckmoduleassembly-8.webp)
1. Following the picture below, turn the Digit 1 buck module over to its backside and solder the white wire onto the `Out +` pad and the black wire onto the `Out -` pad.  
   ![buckmodulesandwiring-9](../img/buckmoduleassembly/buckmoduleassembly-9.webp)
1. Follow the previous steps 3-5 for the Digit 1 buck module then connect the 12V black and white wire into the next available block terminals on `C-12V-1`. See the picture below for the assembled Digit 1 buck module.  
   ![buckmodulesandwiring-10](../img/buckmoduleassembly/buckmoduleassembly-10.webp)
1. Place a buck converter module for the Conductor and Digit 1 to the left of the Digit 1 module. Strip 3mm of insulation from the black and white 28 AWG wire while on the roll starting then tin the stripped end with solder. On the backside of the Conductor and Digit 1 buck module, **(A)** solder the white wire onto the `Out +` pad and the black wire onto the `Out -` pad. Route the wire around the power management relay and **(B)** to the 5V terminal block connector.  
   ![buckmodulesandwiring-11](../img/buckmoduleassembly/buckmoduleassembly-11.webp)
1. Clip the white and black wires, strip 3mm of insulation then tin the stripped end with solder. Connect the white wire to the `+` on the 5V terminal block connector and the black wire onto the `-`.  
   ![buckmodulesandwiring-12](../img/buckmoduleassembly/buckmoduleassembly-12.webp)

## Calibrate the Buck Module Voltage, Part 1

![buckmodulesandwiring-13](../img/buckmoduleassembly/buckmoduleassembly-13.webp)

Follow using the picture above and start with the Digit 0 buck module furthest right. **(A)** Disconnect the black and white wire from the 5V terminal block and connect the probes from the multimeter set to measure DC voltage. **(B)** Plug the 12V power supply into the power management PCB barrel jack. **(C)** Turn the screw on the top of the potentiometer on the Digit 0 buck module counterclockwise until **(D)** the voltage measures between 5.0 and 5.1 volts. Note you'll have to turn the screw on the top of the potentiometer several times counterclockwise before the voltage begins to drop.

Repeat the steps above to calibrate Digit 1 and the Conductor buck modules to 5V.

## Wire Remaining Buck Modules

1. Following the picture below, place a buck converter module for Digit 3 to the far left mounting location. Strip 3mm of insulation from the black and white 28 AWG wire while on the roll starting then tin the stripped end with solder. **(A)** Unroll the two wires starting at the 5V terminal block connector on Digit 3 PCB. **(B)** Slide one 3cm section of heat shrink on the two wires but DO NOT APPLY HEAT, then **(C)** route the wire around the relay, under the power management PCB, and through the port on the PCB stand. **(D)** Finish unwinding the wire when you reach the end of the buck module as shown in the picture. Strip 3mm of insulation then solder the white wire to the buck module `Out +` pad and the black wire to the `Out -` pad. Now that the length of wire is known from its route, snip off the wires next to the terminal block connector **(A)**. Strip 3mm of insulation then tin the stripped end with solder. Connect the white wire to the `+` on the `5V` terminal block connector and the black wire onto the `-`.  
   ![buckmodulesandwiring-14](../img/buckmoduleassembly/buckmoduleassembly-14.webp)
1. Following the diagram below, **(A)** solder the white wire onto the buck module's `In +` pad and the black wire onto the `In -` pad. Secure the module with two M1.7x6mm self tapping screws. **(B)** Route the Digit 0 white and black wire to the power management PCB `C-12V-1` terminal block connector, provide about 10mm extra length in the wire before cutting them. Strip 3mm of insulation then tin the stripped end with solder. Connect the white wire to the `+` on the `C-12V-1` and the black wire onto the `-`.  
   ![buckmodulesandwiring-15](../img/buckmoduleassembly/buckmoduleassembly-15.webp)
1. Following the picture below, place a buck converter module for Digit 2 to the right of Digit 3. Strip 3mm of insulation from the black and white 28 AWG wire while on the roll starting then tin the stripped end with solder. Starting with the Digit 2 PCB, **(A)** unroll the two wires starting at the 5V terminal block connector. **(B)** route the wire around the relay, under the power management PCB, and through the port on the PCB stand. **(C)** Finish unwinding the wire when you reach the end of the buck module as shown in the picture. Strip 3mm of insulation then solder the white wire to the buck module `Out +` pad and the black wire to the `Out -` pad. Now that the length of wire is known from its route, snip off the wires next to the terminal block connector **(A)**. Strip 3mm of insulation then tin the stripped end with solder. Connect the white wire to the `+` on the `5V` terminal block connector and the black wire onto the `-`.  
   ![buckmodulesandwiring-16](../img/buckmoduleassembly/buckmoduleassembly-16.webp)
1. Following the diagram below, **(A)** solder the white wire onto the buck module's `In +` pad and the black wire onto the `In -` pad. Secure the module with two M1.7x6mm self tapping screws. **(B)** Route the Digit 0 white and black wire to the power management PCB `C-12V-1` terminal block connector, provide about 10mm extra length in the wire before cutting them. Strip 3mm of insulation then tin the stripped end with solder. Connect the white wire to the `+` on the `C-12V-1` and the black wire onto the `-`.  
   ![buckmodulesandwiring-17](../img/buckmoduleassembly/buckmoduleassembly-17.webp)
1. Position the heat shrink as per the picture of the completed wiring of the buck converter modules at the beginning of this document. Apply heat from your heat gun to complete the assembly of all the heat shrink.

## Calibrate the Buck Module Voltage, Part 2

Following the picture below with the Digit 3 buck module, **(A)** disconnect the black and white wire from the 5V terminal block, and connect the probes from the multimeter set to measure DC voltage. **(B)** Plug the 12V power supply into the power management PCB barrel jack. **(C)** Turn the screw on the top of the potentiometer on the Digit 3 buck module counterclockwise until **(D)** the voltage measures between 5.0 and 5.1 volts. Note you'll have to turn the screw on the top of the potentiometer several times counterclockwise before the voltage begins to drop.

Repeat the steps above to calibrate Digit 2 buck module to 5V.  
![buckmodulesandwiring-18](../img/buckmoduleassembly/buckmoduleassembly-18.webp)
