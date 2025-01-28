# Actuator Assembly

There are 30 actuators in the display, 7 per digit and 2 for the colons (4 digits x 7 segments + 2 colons = 30 total actuators). The diagrams below identify the various parts and composition of the actuator.

Fully assembled actuator with segment and back stopper.
![All 3D printed parts](../img/motor-actuator-titles.png)

Actuator rack and pinion gear assembly.
![All 3D printed parts](../img/motor-gears-title.png)

The actuator assembly includes installing the shaft gear onto the DC brushed motor, preparing and adding the wires to the motor, assembling the motor mount, pinion gear and shaft, then adding the DC brushed motor to the assembled motor mount.

## Shaft Gear

In this section you'll glue the shaft gear onto the shaft to avoid slippage. The shaft gear must be made from rigid filament like PLA or ABS.

### Shaft Gear Installation Steps

1. The tools and parts needed to install the shaft gear include: a regular tipped screwdriver, super glue, motor shaft 10-toothed gear, and DC brushed toy motor.
![shaftprereq](../img/motor-shaft-gear/1-motor-shaft-gear.webp)
1. Add a drop of super glue to attach the shaft gear. Note the shaft gear is 10mm high and the hole is 5mm.
![shaftstep1](../img/motor-shaft-gear/2-motor-shaft-gear.webp)
1. Position the DC toy motor vertically so the bottom of the DC motor shaft sits on a hard surface. Use the regular tipped screwdriver to press the 10-toothed gear onto the shaft. Be sure to push the 10-toothed gear 5mm down into the shaft.
![shaftstep2](../img/motor-shaft-gear/3-motor-shaft-gear.webp)
1. Repeat the steps in this section for the remaining 29 motors.
![shaftstep4](../img/motor-shaft-gear/4-motor-shaft-gear.webp)

## Wires

After the actuator is assembled, it will be connected to the digit PCB. The white 28 AWG wire provides the clockwise (CW) motion that extends the segment, the black wire provides the counter clockwise (CCW) motion that retracts the segment.

### Wire Cutting and Soldering Steps

In this section you'll create 21 unlabelled motors with 4cm wires with Dupont connectors, 4 motors labelled "C", 4 motors labelled "D", and one labelled "UC" (upper colon), totalling 9 motors having 6cm wires with dupont connectors.

1. The tools and parts needed to prepare and add the wires to the DC motor includes: black and white 28 AWG stranded wire, wire strippers for 28 AWG wire, and a soldering station with 0.8mm 1.76g flux core solder.
![step1](../img/motor-wire/1-motor-wire-assembly.webp)
2. Cut 9 white and 9 black wires of 6cm lengths for segment actuators C and D and the upper colon. Cut 21 white and 21 black wires of 4cm lengths for the remaining actuators.
![step1](../img/motor-wire/2-motor-wire-assembly.webp)
1. Strip about 3mm off one end of each black and white wire.
![step2](../img/motor-wire/3-motor-wire-assembly.webp)
1. Position the DC motor so the shaft is facing upward and the terminals are on the top. Set your soldering iron to 350°C then add solder to each motor terminal.
![step3](../img/motor-wire/4-motor-wire-assembly.webp)
1. Solder the white wire onto the left motor lead and the black wire onto the right motor lead. Be sure to label the motors with 6cm wire as C, D, and the upper colon.
![step4](../img/motor-wire/5-motor-wire-assembly.webp)

### Dupont Connections

1. The tools and parts needed to add the 2.54mm Dupont connectors to each wire include: the DC motor with shaft gear and wires (as prepared in the previous steps), a Dupont connector crimping tool, 60 female Dupont pin connectors and 30 1x2p Dupont connector housings.
![step1](../img//dupont-connections/1-motor-wire-dupont-connection.webp)
1. Strip 3mm off the DC motor wire and crimp each female Dupont pin connector to each wire.
![step2](../img/dupont-connections/2-motor-wire-dupont-connection.webp)
1. Crimp the female connectors onto each wire.
![step3](../img/dupont-connections/3-motor-wire-dupont-connection.webp)
1. Crimp the female connectors onto each wire.
![step4](../img/dupont-connections/4-motor-wire-dupont-connection.webp)
1. Repeat the previous steps for all remaining motors. Be sure to place your label on the black side of the motor for the nine, 6cm wire length actuators with C, D or UC (upper colon). No need to label the 21 other actuators with 4cm lengths
![step5](../img/dupont-connections/5-motor-wire-dupont-connection.webp)

## Motor Mount

1. The tools and parts needed to assemble the motor mount include: 3d printed motor mount in PLA and Nylon pinion reduction gear, a 20mm metal shaft made from a jumbo paper clip. a soldering station capable of a heat setting of 250° C, clamping tweezers with a thin piece of metal. Verify the shaft can easily slide through the pinion gear before assembling the motor. If you cannot easily rotate the pinion gear on the shaft, then you'll need a 1/16" drill bit and drill to widen the pinion gear shaft hole.
![actuatorstep1](../img/actuator/1-actuator-assembly.jpg)
1. Partially insert the 20mm shaft into the motor mount as shown in the picture below.
![actuatorstep2](../img/actuator/2-actuator-assembly.jpg)
1. Align the pinion reduction gear and shaft so the shaft can easily slide through the pinion gear. Make sure the large 30-tooth side of the pinion gear is facing out per the diagram below.
![actuatorstep3](../img/actuator/3-actuator-assembly.jpg)
1. Clamp down the motor mount with the open end of the shaft facing up per the picture below.
![actuatorstep4](../img/actuator/4-actuator-assembly.jpg)
1. Melt the shaft into place using the thin metal (zinc) strip and clamping tweezers. Melt the motor mount shaft entry down to half its size--the small melted plasic nub should extend about 1mm out from the motor mount. See the picture below.
![actuatorstep5](../img/actuator/5-actuator-assembly.jpg)
![actuatorstep6](../img/actuator/6-actuator-assembly.jpg)
![actuatorstep7](../img/actuator/7-actuator-assembly.jpg)
