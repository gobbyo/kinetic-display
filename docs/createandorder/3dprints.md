# 3D Print the Display Parts

Below are few guidelines to keep in mind when printing and assembling the display:

- Read all the assembly guides in this documentation before printing to ensure you have a clear understanding of the fabrication type and quality, positioning and assembly.
- The 3mf project files are included under the `./fdm/3mf` directory for Bambu Studio or Orca Slicer users. All necessary settings are included at an object level, not on a global level.
- The stl files are included under the `./fdm/stl` directory. You'll need to follow the table below for the settings to use.
- The display face uses over 2/3rds of the 1 KG roll of filament. Therefore, be sure to use the same roll of filament when printing both halves of the display face, segments, and colons. Also, have two 1 KG rolls of white filament from the same batch to avoid inconsistencies in your print color.
- Do not worry if your 3D printer and slicer cannot iron the top surfaces. Ironing the top surfaces is for fit and finish and will not affect the functionality of the display.
- Thoroughly dry your filament before use, especially the nylon and flexible filament types as they will not print properly and cause issue with being stringy and may have inexact gear teeth or hole sizes.
- Be sure you apply an adhesive to the printer plate bed otherwise the edges and corners of the display face may warp. I used all weather Aqua Net, super hold hair spray for my display faces which provided an even coating of adhesive across the entire surface of the bed plate and resulted in clean corners and edges.
- Use painter's tape to keep the pieces organized, see picture below. Note the segments a-g (left to right) are preserved the moment the bed plate is removed from the 3d printer.
![fdmassembly](../img/fdmassembly/segmentparts.webp)

Amount of filament by type

| Type | Weight (g) |
| :--- | ---: |
| Black Nylon  | 77.1g|
| Black PLA  | 272.42g |
| White PLA  | 1535.44 |
| Black TPU  | 115.15 |

All 3D printed parts, see table below for details.

| 3mf | stl | description | stl quantity | per unit (g) | total (g) | Material | Color | Build Plate | Fill Density | Top Surface Ironing | Detect Thin Walls | Top and bottom shell pattern |
| :------ | :------ | :------ | :------: | :------: | :------: | :------ | :------ | :------ | :------ | :------ | :------ | :------ |
| pla-textured-white | colon-seg.stl | Colon, upper and lower | 2 | 1.88 | 3.76 | PLA Matte | white | textured | 100% | No | No | monotonic |
| pla-smooth-black | digit-back-plate.stl | Back plates for digits 0 and 3 for mounting the actuators | 3 | 47.43 | 142.29 | PLA Matte | black | smooth | 50% | Yes | Yes | monotonic |
| tpu-smooth-black | digit-gasket.stl | Gaskets for digits 0 and 3 to cushion the PCB during segment retractions | 3 | 17.86 | 53.58 | TPU | black | smooth | 15% | Yes | No | monotonic |
| pla-smooth-black | digit-gear10.stl | Motor shaft gear for digits and colons with 10 teeth that is mounted onto the heavy duty 103 motors | 30 | 0.5 | 15 | PLA Matte | black | smooth | 100% | No | No | concentric |
| nylon-smooth-black | digit-gear30.stl | Pinion gear for digits and colons with a 30 tooth gear and 6 tooth reduction gear  | 30 | 1.1 | 33 | Nylon | black | smooth | 100% | No | No | concentric |
| pla-smooth-white | digit-motor-mount.stl | Motor mount for digits and colons | 30 | 12.77 | 383.1 | PLA Matte | white | smooth | 100% | No | No | monotonic |
| pla-textured-white | digit0-1-face.stl | Kinetic display face, right side (when facing the front, textured surface side) | 1 | 395 | 395 | PLA Matte | white | textured | 70% | Yes | No | monotonic |
| pla-smooth-black | digit1-back-plate.stl | Conductor and digit 1 back plate for mounting the actuators | 1 | 67.7 | 67.7 | PLA Matte | black | smooth | 50% | Yes | Yes | monotonic |
| tpu-smooth-black | digit1-gasket.stl | Gasket for the conductor and digit 1 to cushion the PCB during segment retractions | 1 | 31.71 | 31.71 | TPU | black | smooth | 15% | No | No | monotonic |
| pla-textured-white | digit2-3-face.stl | Kinetic display face, left side (when facing the front, textured surface side) | 1 | 399 | 399 | PLA Matte | white | textured | 70% | Yes | No | monotonic |
| pla-smooth-black | digit2-back-plate.stl | Back plate for digit 2 for mountig the actuators and powerbank/display stand | 1 | 47.43 | 47.43 | PLA Matte | black | smooth | 50% | Yes | Yes | monotonic |
| tpu-smooth-black | digit2-gasket.stl | Gasket for digits 2 to cushion the PCB during segment retractions | 1 | 17.86 | 17.86 | TPU | black | smooth | 15% | No | No | monotonic |
| pla-smooth-white | powerbank-cover.stl | Cover for buck converters and powerbank PCB | 1 | 65.53 | 65.53 | PLA Matte | white | smooth | 100% | Yes | No | monotonic |
| pla-smooth-white | powerbank.stl | Kinetic display stand, buck converter mounts, and powerbank PCB mount | 1 | 146.75 | 146.75 | PLA Matte | white | smooth | 100% | Yes | No | monotonic |
| nylon-smooth-black | rack-gear.stl | The arm of the actuator that extends and retracts the segment | 30 | 1.47 | 44.1 | Nylon | black | smooth | 25% | No | No | concentric |
| tpu-smooth-black | rackgear-bumper-gasket.stl | Provides some cushion for the rack gear when extended | 30 | 0.4 | 12 | TPU | black | smooth | 100% | No | No | monotonic |
| pla-smooth-white | rackgear-bumper.stl | Stops the segment or colon at the precise distance when extended | 30 | 0.61 | 18.3 | PLA Matte | white | smooth | 100% | No | No | monotonic |
| pla-textured-white | seg-a.stl | Digit 7-segment A | 4 | 4 | 16 | PLA Matte | white | textured | 100% | No | No | monotonic |
| pla-textured-white | seg-b.stl | Digit 7-segment B | 4 | 4 | 16 | PLA Matte | white | textured | 100% | No | No | monotonic |
| pla-textured-white | seg-c.stl | Digit 7-segment C | 4 | 4 | 16 | PLA Matte | white | textured | 100% | No | No | monotonic |
| pla-textured-white | seg-d.stl | Digit 7-segment D | 4 | 4 | 16 | PLA Matte | white | textured | 100% | No | No | monotonic |
| pla-textured-white | seg-e.stl | Digit 7-segment E | 4 | 4 | 16 | PLA Matte | white | textured | 100% | No | No | monotonic |
| pla-textured-white | seg-f.stl | Digit 7-segment F | 4 | 4 | 16 | PLA Matte | white | textured | 100% | No | No | monotonic |
| pla-textured-white | seg-g.stl | Digit 7-segment G | 4 | 4 | 16 | PLA Matte | white | textured | 100% | No | No | monotonic |
| pla-smooth-white | seg-pin.stl | Pin to hold the rack gear onto the segment and colons | 30 | 0.4 | 12 | PLA Matte | white | smooth | 100% | Yes | No | monotonic |

Congratulations for fabricating all your parts!
