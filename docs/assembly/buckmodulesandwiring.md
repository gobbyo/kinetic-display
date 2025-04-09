# Buck Modules and Wiring

## Prerequisites

- 3D print the Digit and controller TPU gaskets

## PCB and Stand Layout

This section ensures wiring for the PCBs are oriented for the mounting of the buck modules and wiring.

1. Remove the Raspberry Pi Pico and Pico W 2040 from the PCBs. We'll add these later when it is safe to do so.
1. Lay the PCBs face up with Digit 0 on the far right and Digit 3 on the far left. Position the stand below the PCBs so the barrel jack is between the controller/Digit 1 PCB and Digit 2 PCB.
![buckmodulesandwiring-1](../img/buckmoduleassembly/buckmoduleassembly-1.webp)
1. Place the TPU gaskets on the PCBs. Note the TPU gasket for Digit 2 differs slightly from Digit 0 and 3 gaskets.
![buckmodulesandwiring-2](../img/buckmoduleassembly/buckmoduleassembly-2.webp)

## Wiring the Buck Modules

This section details wiring the buck converter to the PCBs. The buck converter module has an `In +` and `In -` on one side for the 12v input, and an `Out +` and `Out -` on the opposite side for the converted 5v output. This section will also cover how to calibrate the variable buck module to provide 5.0v to 5.1v output.

![buckmodulesandwiring-wiring](../img/buckmoduleassembly/buckmoduleassembly-wire.webp)

The picture below is the completed wiring of the buck converter modules. The order of install is **1, 2, 3** on the right, followed by **4** and **5** on the left.

![buckmodulesandwiring](../img/buckmoduleassembly/buckmoduleassembly-complete.webp)

!!! warning
    Use anti static mats and ESD wristband and grounding wire for the remainder of the Kinetic Display electronics assembly.

### Digits 0-1, and Controller

1. Following the picture below, place a buck converter module for Digit 0 on the rightmost support on the display stand. Strip 3mm of insulation from the black and white 28 AWG wire while on the roll starting then tin the stripped end with solder. Starting with the Digit 0 PCB, **(A)** Route the two wires from the 5v terminal block connector. **(B)** Slide two 3cm sections of heat shrink on the two wires but DO NOT APPLY HEAT, then **(C)** continue routing the wire around the relay, under the power management PCB and through the port on the PCB stand. **(D)** Finish unwinding the wire when you reach the end of buck module as shown in the picture. Now that the length of wire is known from its route, snip off the wires next to the terminal block connector **(A)**. Strip 3mm of insulation then tin the stripped end with solder. Connect the white wire to the `+` on the `5v` terminal block connector and the black wire onto the `-`.
![buckmodulesandwiring-3](../img/buckmoduleassembly/buckmoduleassembly-3.webp)
1. Following the picture below, turn the Digit 0 buck module over to its backside and solder the white wire onto the `Out +` pad and the black wire onto the `Out -` pad.
![buckmodulesandwiring-4](../img/buckmoduleassembly/buckmoduleassembly-4.webp)
1. Following the picture below, turn the Digit 0 buck module 180 degrees while having its backside facing up. Strip 3mm of insulation from the black and white 28 AWG wire while on the roll starting then tin the stripped end with solder. Solder the white wire onto the buck module's `In +` pad and the black wire onto the `In -` pad.
![buckmodulesandwiring-5](../img/buckmoduleassembly/buckmoduleassembly-5.webp)
1. Turn the Digit 0 buck module over and secure it with 1.7 x 6mm self tapping screws onto the rightmost module supports on the display stand.
![buckmodulesandwiring-6](../img/buckmoduleassembly/buckmoduleassembly-6.webp)
1. Route the Digit 0 white and black wire to the power management PCB `C-12v-1` terminal block connector, provide about 10mm extra length in the wire before cutting them. Strip 3mm of insulation then tin the stripped end with solder. Connect the white wire to the `+` on the `C-12v-1` and the black wire onto the `-`.
![buckmodulesandwiring-7](../img/buckmoduleassembly/buckmoduleassembly-7.webp)
1. Following the picture below, place a buck converter module for Digit 1 to the left of the Digit 0 module. Strip 3mm of insulation from the black and white 28 AWG wire while on the roll starting then tin the stripped end with solder. Starting with the Digit 1 PCB, **(A)** Route the two wires from the 5v terminal block connector. **(B)** Slide one 3cm section of heat shrink on the two wires but DO NOT APPLY HEAT, then **(C)** continue routing the wire around the relay, under the power management PCB and through the port on the PCB stand. **(D)** Finish unwinding the wire when you reach the end of second buck module as shown in the picture. Now that the length of wire is known from its route, snip off the wires next to the terminal block connector **(A)**. Strip 3mm of insulation then tin the stripped end with solder. Connect the white wire to the `+` on the `5v` terminal block connector and the black wire onto the `-`.
![buckmodulesandwiring-8](../img/buckmoduleassembly/buckmoduleassembly-8.webp)
1. Following the picture below, turn the Digit 1 buck module over to its backside and solder the white wire onto the `Out +` pad and the black wire onto the `Out -` pad.
![buckmodulesandwiring-9](../img/buckmoduleassembly/buckmoduleassembly-9.webp)
1. Follow the previous steps 3-5 for the Digit 1 buck module then connect the 12v black and white wire into the next available block terminals on `C-12v-1`. See the picture below for the assembled Digit 1 buck module.
![buckmodulesandwiring-10](../img/buckmoduleassembly/buckmoduleassembly-10.webp)
1. Place a buck converter module for the Colon/controller to the left of the Digit 1 module. Strip 3mm of insulation from the black and white 28 AWG wire while on the roll starting then tin the stripped end with solder. On the backside of the Colon/controller buck module, **(A)** solder the white wire onto the `Out +` pad and the black wire onto the `Out -` pad. Route the wire around the power management relay and **(B)** to the 5v terminal block connector.
![buckmodulesandwiring-11](../img/buckmoduleassembly/buckmoduleassembly-11.webp)
1. Clip the white and black wires, strip 3mm of insulation then tin the stripped end with solder. Connect the white wire to the `+` on the 5v terminal block connector and the black wire onto the `-`.
![buckmodulesandwiring-12](../img/buckmoduleassembly/buckmoduleassembly-12.webp)

### Calibrate the Buck Module Voltage

![buckmodulesandwiring-13](../img/buckmoduleassembly/buckmoduleassembly-13.webp)

Following the picture above and starting with the Digit 0 buck module and working our way left. **(A)** disconnect the black and white wire from the 5v terminal block and connect the probes from the multimeter and turn on the multimeter. **(B)** Plug the 12v power supply into the power management PCB barrel jack. **(C)** Turn the screw on the top of the potentiometer on the Digit 0 buck module counterclockwise until **(D)** the voltage measures between 5.0 and 5.1 volts. Note you'll have to turn the screw on the top of the potentiometer several times before the voltage begins to drop.

Repeat the steps above to calibrate Digit 1 and the Conductor buck modules to 5v.

## Continue Wiring the Remaining Buck Modules

1. Following the picture below, place a buck converter module for Digit 3 to the far left mounting location. Strip 3mm of insulation from the black and white 28 AWG wire while on the roll starting then tin the stripped end with solder. Starting with the Digit 3 PCB, **(A)** unroll the two wires starting at the 5v terminal block connector. **(B)** Slide one 3cm section of heat shrink on the two wires but DO NOT APPLY HEAT, then **(C)** route the wire around the relay, under the power management PCB, and through the port on the PCB stand. **(D)** Finish unwinding the wire when you reach the end of the buck module as shown in the picture. Strip 3mm of insulation then solder the white wire to the buck module `Out +` pad and the black wire to the `Out -` pad. Now that the length of wire is known from its route, snip off the wires next to the terminal block connector **(A)**. Strip 3mm of insulation then tin the stripped end with solder. Connect the white wire to the `+` on the `5v` terminal block connector and the black wire onto the `-`.
![buckmodulesandwiring-14](../img/buckmoduleassembly/buckmoduleassembly-14.webp)
1. Following the diagram below, **(A)** solder the white wire onto the buck module's `In +` pad and the black wire onto the `In -` pad. Secure the module with two M1.7x6mm self tapping screws. **(B)** Route the Digit 0 white and black wire to the power management PCB `C-12v-1` terminal block connector, provide about 10mm extra length in the wire before cutting them. Strip 3mm of insulation then tin the stripped end with solder. Connect the white wire to the `+` on the `C-12v-1` and the black wire onto the `-`.
![buckmodulesandwiring-15](../img/buckmoduleassembly/buckmoduleassembly-15.webp)

![buckmodulesandwiring-16](../img/buckmoduleassembly/buckmoduleassembly-16.webp)

![buckmodulesandwiring-17](../img/buckmoduleassembly/buckmoduleassembly-17.webp)

![buckmodulesandwiring-18](../img/buckmoduleassembly/buckmoduleassembly-18.webp)
