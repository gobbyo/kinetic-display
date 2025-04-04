# Controller PCB Test

Run the tests in this section after assembling the controller PCB to ensure all the components on the PCB are soldered and functional. Any defective electronic component on the controller PCB will need to be replaced before completing the project.

## Prerequisites

- [Completed Controller and Digit 1 PCB ready for actuators](controllerpcbassembly.md).
- Computer and microcontroller with the [prerequisite software](../prerequisitesoftware.md).
- [Deployed the Controller Project to the Controller PCB](deploycontrollerproject.md)
- [Completed the digit PCB test](digitpcbtest.md) for digit 1 on the controller PCB.

## Controller PCB Test Application

1. From Visual Studio Code, **(A)** select the File->Open Folder menu, **(B)** select the conductor folder, then **(C)** click the **Select Folder** button.
![testpcbactuator-prerequisite](../img/controllerpcbtest/controllerpcbtest-1.webp)
1. On the Controller and Digit 1 PCB, **(A)** plug the USB cable from your computer into the USB port on the Raspberry Pi Pico W 2040. **(B)** Connect a motor actuator to the `COLON-TOP` with the white wire dupont connector plugged into `CW` pin and the black wire plugged into the `CCW` pin.
![controllerpcbtest-2](../img/controllerpcbtest/controllerpcbtest-2.webp)
1. From Visual Studio Code, **(A)** select the `digit_colon.py` file, then **(B)** select **MicroPico vREPL** from the terminal pane menu.
![controllerpcbtest-3](../img/controllerpcbtest/controllerpcbtest-3.webp)
1. From the Visual Studio Code status bar, **(A)** verify the Raspberry Pi Pico W is connected. **(B)** Click the `Run` button to start the controller PCB test application.
![controllerpcbtest-4](../img/controllerpcbtest/controllerpcbtest-4.webp)