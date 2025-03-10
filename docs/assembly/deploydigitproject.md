# Deploy the Digit Project to the Digit PCB

In this section you will upload code to your Raspberry Pi Pico and PicoW from your computer.

## Prerequisites

- Completed the assembly and soldering of the [Digit PCB](digitpcbassembly.md)
- Created a fork of the Kinetic-Display GitHub repository, see [Software and Microcontroller Preparation](../prerequisitesoftware.md)
- Deployed the digit directory, also see [Software and Microcontroller Preparation](../prerequisitesoftware.md)

## Configure and Deploy the Digit Project

1. Connect your Computer to the digit PCB Pico per the instructions on [Verify Micropython on your Raspberry Pi Pico](../prerequisitesoftware.md)
2. From VS Code, select **File->Open Folder...** and open the **deploy/digit** folder you deployed during step 4 in the section [Fork and Clone the Repository](../prerequisitesoftware.md)
3. Following the screen capture below, select the Explorer icon (**A**) in the left [Activity bar](https://code.visualstudio.com/docs/getstarted/userinterface#_basic-layout). Click the digit.json file (**B**) in the Explorer pane. Change the **"digit":** value (**C**) to match the PCB labelled number 0-3.
!!! warning
    It is very important to have the digit value in the digit.json file match the PCB's labelled value.
![testdigitpcb-1](../img/testdigitpcb/testdigitpcb-1.webp)
1. Following the screen capture below, click **All Commands** (**A**) on the [status bar](https://code.visualstudio.com/api/ux-guidelines/status-bar). In the Command text field (**B**), type "**Upload**" after "**> MicroPico:** ", then select the dropdown **MicroPico: Upload project to Pico**.
![testdigitpcb-2](../img/testdigitpcb/testdigitpcb-2.webp)
1. Verify the project was uploaded into the Pico.
![testdigitpcb-3](../img/testdigitpcb/testdigitpcb-3.webp)
