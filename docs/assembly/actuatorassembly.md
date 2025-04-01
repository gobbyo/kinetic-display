# Actuator Assembly

There are 30 actuators in the display, 7 per digit and 2 for the colons (4 digits x 7 segments + 2 colons = 30 total actuators). The diagrams below identify the various parts and composition of the actuator.

Fully assembled actuator with segment and back stopper.
![All 3D printed parts](../img/motor-actuator-titles.png)

Actuator rack and pinion gear assembly.
![All 3D printed parts](../img/motor-gears-title.png)

The actuator assembly includes installing the shaft gear onto the DC brushed motor, preparing and adding the wires to the motor, assembling the motor mount, pinion gear and shaft, then adding the DC brushed motor to the assembled motor mount.

## Prerequisites

***Table of components***

| Quantity | Component | Image |
| :--: | :------| :-----: |
| 30 | 130 Strong Magnetic Toy Motor | ![component-10](../img/component/component-10.webp) |
| 150 cm | 28 AWG Stranded Wire (white) | ![component-11](../img/component/component-11.webp) |
| 150 cm | 28 AWG Stranded Wire (black) | ![component-12](../img/component/component-12.webp) |
| 60 | DuPont 2.54mm Pitch Female Connector Pin | ![component-13](../img/component/component-13.webp) |
| 30 | DuPont 2.54mm Pitch Terminal Connector Single Row Housing 2 Pin | ![component-14](../img/component/component-14.webp) |
| 10 | Jumbo Metal Paperclip (smooth) | ![component-15](../img/component/component-15.webp) |

***Table of tools***

| Required | Tool | Image |
| :---: | :------- | :---: |
| Yes | Soldering station    | ![tool-4](../img/tools/tool-4.webp)|
| Yes | 0.8mm 1.76oz RoHS flux core solder | ![tool-1](../img/tools/tool-1.webp)|
| Yes | Large regular tipped screwdriver | ![tool-7](../img/tools/tool-7.webp) |
| Yes | Super glue | ![tool-8](../img/tools/tool-8.webp) |
| Yes | 22-34 AWG Wire Stripper and Cutter | ![tool-9](../img/tools/tool-9.webp) |
| Yes | Pin Crimp Tool for 2.54mm Dupont Connectors | ![tool-10](../img/tools/tool-10.webp) |
| Yes | Heavy Duty Wire Cutter Pliers | ![tool-11](../img/tools/tool-11.webp) |
| Yes | Heavy Duty Cross Locking or Clamping Tweezers | ![tool-12](../img/tools/tool-12.webp) |
| Yes | 10cm zinc strip | ![tool-14](../img/tools/tool-14.webp) |
| No | Label Maker | ![tool-5](../img/tools/tool-5.webp) |

## Shaft Gear

In this section you'll glue the shaft gear onto the shaft to avoid slippage. The shaft gear must be made from rigid filament like PLA or ABS.

### Shaft Gear Installation Steps

The tools and parts needed to install the shaft gear include: a regular tipped screwdriver, super glue, motor shaft 10-toothed gear, and DC brushed toy motor.

1. Add a drop of super glue to attach the shaft gear. Note the shaft gear is 10mm high and the hole is 5mm.
![shaftstep1](../img/motor-shaft-gear/2-motor-shaft-gear.webp)
1. Position the DC toy motor vertically so the bottom of the DC motor shaft sits on a hard surface. Use the regular tipped screwdriver to press the 10-toothed gear onto the shaft. Be sure to push the 10-toothed gear 5mm down into the shaft.
![shaftstep2](../img/motor-shaft-gear/3-motor-shaft-gear.webp)
1. Repeat the steps in this section for the remaining 29 motors.
![shaftstep4](../img/motor-shaft-gear/4-motor-shaft-gear.webp)

## Wires

After the actuator is assembled, it will be connected to the digit PCB. The white 28 AWG wire provides the clockwise (CW) motion that extends the segment, the black wire provides the counter clockwise (CCW) motion that retracts the segment.

### Wire Cutting and Soldering Steps

In this section you'll create 21 unlabelled motors with 4 centimeter wires with Dupont connectors, 4 motors labelled "C", 4 motors labelled "D", and one labelled "UC" (upper colon), totalling 9 motors having 6 centimeter wires with dupont connectors. The tools and parts needed to prepare and add the wires to the DC motor includes: black and white 28 AWG stranded wire, wire strippers for 28 AWG wire, and a soldering station with 0.8mm 1.76g flux core solder.

1. Cut 9 white and 9 black wires of 6 centimeter lengths for segment actuators C and D and the upper colon. Cut 21 white and 21 black wires of 4 centimeter lengths for the remaining actuators.
![step1](../img/motor-wire/1-motor-wire.webp)
1. Strip about 3mm off one end of each black and white wire.
![step2](../img/motor-wire/2-motor-wire.webp)
1. Position the DC motor so the shaft is pointed away and the terminals are facing up. Set your soldering iron to 350°C then add solder to each motor terminal.
![step3](../img/motor-wire/3-motor-wire.webp)
1. With the DC motor shaft pointing up and the terminals are facing up, solder the white wire onto the left motor terminal and the black wire onto the right motor terminal.
![step4](../img/motor-wire/4-motor-wire.webp)

!!! note
     There are 9 motors with 6 centimeter wire lengths: four motors labelled C, four D, and one UC (upper colon). Place a label on the black-wire side of the motor.

### Dupont Connections

The tools and parts needed to add the 2.54mm Dupont connectors to each wire include: the DC motor with shaft gear and wires (as prepared in the previous steps), a Dupont connector crimping tool, 60 female Dupont pin connectors and 30 1x2p Dupont connector housings.

1. Strip 3mm off the end of the DC motor wire.
![step1](../img/dupont-connections/1-motor-dupont-connection.webp)
1. Crimp the female connectors onto each wire.
![step2](../img/dupont-connections/2-motor-dupont-connection.webp)
1. Slide the Dupont connector housing onto the wires so the pins lock into the housing.
![step3](../img/dupont-connections/3-motor-dupont-connection.webp)
1. Repeat the previous steps for all remaining motors. Be sure to place your label on the black-wire side of the motor for the 6 centimeter wire length actuators with C (4), D (4) and one UC (upper colon). No need to label the 21 other actuators with 4 centimeter lengths
![step4](../img/dupont-connections/4-motor-dupont-connection.webp)

## Motor Mount

In this section you'll assemble the motor mounts. Properly installed parts on the motor mount are essential to making the actuators work without issues such as having a segment stick or jam in an extended or retracted position. The figure below summarizes the assembly for the motor mount. There are three parts: the **(A) motor mount**, the **(B) pinion reduction gear**, and **(C) pinion gear shaft**. Discard the red support section.
![actuatorfigure](../img/actuator/motor-mount-figure.webp)
The tools and parts needed to assemble the motor mount include: 3d printed motor mount in PLA and Nylon pinion reduction gear, a 20mm metal shaft made from a jumbo paper clip, a soldering station capable of a heat setting of 250° C, clamping tweezers with a thin piece of metal.

1. Cut the off the straight sections from the Jumbo paper clip.
![actuatorstep1](../img/actuator/1-actuator.webp)
1. Measure 2 cm from each Jumbo paper clip straight section.
![actuatorstep2](../img/actuator/2-actuator.webp)
1. Use a large wire cutter to cut the shaft.
![actuatorstep3](../img/actuator/3-actuator.webp)
1. Insert the 2 cm shaft through the motor mount until is protrudes about 1mm into the pinion gear space.
![actuatorstep4](../img/actuator/4-actuator.webp)
1. Add the pinion gear to the motor mount as shown in the diagram. Insert the shaft by aligning the pinion gear shaft hole with the metal shaft, then slide the metal shaft all the way into the motor mount.
![actuatorstep5](../img/actuator/5-actuator.webp)
1. Heat your soldering iron to 250°C and prepare your clamping tweezer and zinc strip as shown in the picture.
![actuatorstep6](../img/actuator/6-actuator.webp)
1. Hold the zinc strip over the shaft collar and press down on the zinc strip with your soldering iron. Melt the collar and flatten it onto the motor mount.
![actuatorstep7](../img/actuator/7-actuator.webp)
1. When finished, the melted collar will only protrude about a half millimeter out from the motor mount.
![actuatorstep8](../img/actuator/8-actuator.webp)
!!! note
    Verify the shaft can slide through the pinion gear before assembling the motor. If you cannot rotate the pinion gear on the shaft, then you'll need to reprint the pinion gear to ensure the hole is wide enough. Avoid an overly sized shaft hole as it allows the gear to shift side to side on the motor shaft and will cause the actuator to jam or stick. ![actuatorstep9](../img/actuator/9-actuator.webp)
1. Hold the main body of the motor mount so the pinion gear faces left. Avoid touching or putting any pressure onto the motor mounting tabs used the screw the motor onto the display. With your other hand, hold the prepared motor with the shaft pointed left and the terminals downward, insert the prepared motor into the motor mount.
![actuatorstep10](../img/actuator/10-actuator.webp)
1. Repeat the process for the remaining 29 motors.
![actuatorstep11](../img/actuator/11-actuator.webp)
