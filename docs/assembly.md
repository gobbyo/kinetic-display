# Assembly

## Fork and clone GitHub

For this task you will create a fork of the kinetic display repository and clone the fork locally onto your workstation. You will need to work with a code fork so that you can modify your local files without changing the original source code. Note the bias of this documentation is to use the Windows operating system with the latest Git tools.

From your windows machine, install the Git tool set:

1. Open a browser session and click the link to [Get started with GitHub documentation - GitHub Docs](https://docs.github.com/en/get-started)
1. Click on the link [Creating an account on GitHub - GitHub Docs](https://docs.github.com/en/get-started/start-your-journey/creating-an-account-on-github) to create your account
1. Then [Set up Git - GitHub Docs](https://docs.github.com/en/get-started/getting-started-with-git/set-up-git) to install the Git tool set.  Use the default values in the setup wizard
1. Login with your GitHub account credentials
1. From your browser open [kinetic-display](https://github.com/gobbyo/kinetic-display)
1. Click on the "Fork" dropdown and create a new fork
1. Open a command prompt and make a new directory/folder by typing ```mkdir repos``` and hit the enter key
1. Change your command prompt to the new directory using command ```cd repos```
1. From your browser, copy the command HTTPS Clone URL and paste it into your command window then hit the enter key. You should see a fork of all the files from the kinetic-display appear in a new folder at ```.\repos\kinetic-display\```.

Congratulations, you have the files to begin your project!

## Fabricate the Printed Circuit Boards (PCBs)

For this task you will order the PCBs to be fabricated. The PCB files are in your fork at kinetic-display\pcb. See the instructions below to place a separate order for each of the 3 files that begin with the following names:

- Gerber_KineticDisplay-Controller
- Gerber_KineticDisplay-PowerSystem
- Gerber_KineticDisplay-SingleDigit

You will need to order more PCBs than required for this project because the minimum order is five for most PCB fabrication facilities. Be sure to order the remaining components and materials from the bill of materials (BOM).

1. From your browser open [https://jlcpcb.com/](https://jlcpcb.com/) and create an account if you do not have one, then click the “Order now” button. See the figure below.
![Click the 'order now' button](img/pcborder-1.png)
1. Open the Gerber file by clicking the “Add Gerber file” button. Repeat this step through step 4 for each of the three Gerber files found under the ```kinetic-display\pcb directory```. See the figure below.
![Click the 'Add Gerber file' button](img/pcborder-2.png)
1. Use all the default settings except change the PCB color to white to give the LEDs more luminosity.
![Use the default settings except set the PCB color to white](img/pcborder-3.png)
1. Click the “SAVE TO CART” and finish the order by completing the shipping and payment part of the wizard.
![Use the default settings except set the PCB color to white](img/pcborder-4.png)

## 3D Print the Display Parts

Below are few guidelines to keep in mind when printing and assembling the display:

- Print all the parts by color and filament type. First print all the white pieces, then black.
- The display face uses over 2/3rds of the 1 KG roll of filament. Therefore, be sure to use the same roll of filament when printing both halves of the display face, segments, and colons. Also, have two 1 KG rolls of white filament from the same batch to avoid inconsistencies in your print color.
- Do not use any glue as it is not necessary and may make a mess.
- Do not worry if your 3D printer and slicer cannot iron the top surfaces. Ironing the top surfaces is for fit and finish and will not affect the functionality of the display.
- Be sure you apply an adhesive to the printer plate bed otherwise the edges and corners of the display face may warp. I used all weather Aqua Net, super hold hair spray for my display faces which provided an even coating of adhesive across the entire surface of the bed plate and resulted in clean corners and edges.

All 3D printed parts
![All 3D printed parts](img/allparts.png)

## Actuator assembly

There are 30 actuators in the display, 7 per digit and 2 for the colons (4 digits x 7 segments + 2 colons = 30 total actuators). The diagrams below identify the various parts and composition of the actuator.

Fully assembled actuator with segment and back stopper.
![All 3D printed parts](img/motor-actuator-titles.png)

Actuator rack and pinion gear assembly.
![All 3D printed parts](img/motor-gears-title.png)