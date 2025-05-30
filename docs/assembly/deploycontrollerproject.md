# Deploy the Conductor Project to the Conductor PCB

In this guide you will upload code from the **conductor** folder on your computer to your Raspberry Pi Pico W 2040.

## Prerequisites

- Completed the assembly and soldering of the [conductor PCB](controllerpcbassembly.md).
- Created a fork of the Kinetic-Display GitHub repository. See [Software and Microcontroller Preparation](../prerequisitesoftware.md).
- Deployed the digit and controller directories. Also, see [Software and Microcontroller Preparation](../prerequisitesoftware.md).

## Configure and Deploy the Conductor Project

1. Connect your computer to the conductor PCB Pico W 2040 as described in [Verify Micropython on your Raspberry Pi Pico](../prerequisitesoftware.md).
1. Open VS Code and follow the steps below:
      - **(A)** Select **File -> Open Folder...**.
      - **(B)** Navigate to the **deploy/conductor** folder you deployed during step 4 in the section [Fork and Clone the Repository](../prerequisitesoftware.md).
      - **(C)** Click the "Select Folder" button.  
   ![deploycontrollercode-1.webp](../img/deploycontrollercode/deploycontrollercode-1.webp)
1. Open the `main.py` file and make the following changes:
      - **(A)** Comment out the call to the `loop()` function.
      - **(B)** Uncomment the `manual()` function.
      - **(C)** Rename the `main.py` file to `_main.py`.  
   Don't forget to save the file after making these changes.  
   ![deploycontrollercode-2](../img/deploycontrollercode/deploycontrollercode-2.webp)
1. Create a new terminal in VS Code:
      - **(A)** Click the ellipsis (`...`) in the terminal pane.
      - **(B)** Select **Terminal -> New Terminal** from the submenu.  
   ![deploycontrollercode-3](../img/deploycontrollercode/deploycontrollercode-3.webp)
1. Connect your computer's USB port to the Raspberry Pi Pico W 2040 as shown below:  
   ![deploycontrollercode-4](../img/deploycontrollercode/deploycontrollercode-4.webp)
1. In the terminal pane:
      - **(A)** Select the drop-down menu.
      - **(B)** Click the **MicroPico vREPL** submenu item.  
   ![deploycontrollercode-5](../img/deploycontrollercode/deploycontrollercode-5.webp)
1. Upload the project to the Pico:
      - **(A)** Click **All Commands** on the [status bar](https://code.visualstudio.com/api/ux-guidelines/status-bar).
      - **(B)** In the Command text field, type "**Upload**" after "**> MicroPico:** ".
      - **(C)** Select the dropdown **MicroPico: Upload project to Pico**.  
   ![deploycontrollercode-6](../img/deploycontrollercode/deploycontrollercode-6.webp)

## Configuration Options

The Kinetic Display can be configured through the web interface after connection to Wi-Fi. The following settings are available:

- **Time Format**: 12-hour or 24-hour time format (setting: `time`)
- **Motor Speed**: Controls the speed of segment movements (setting: `speed`)
- **Wait Time**: Delay between segment movements in milliseconds (setting: `wait`)
- **Temperature Unit**: Celsius or Fahrenheit (setting: `tempCF`)
- **Schedule**: The event schedule file to use (setting: `schedule`)
- **Digit Test at Startup**: Enable or disable the digit test animation when the display starts up (setting: `enable_test_digits`)
  - Set to `true` to enable the digit test (default)
  - Set to `false` to disable the digit test

Disabling the digit test at startup can be useful in environments where the mechanical noise of the segment movements might be disruptive, or when you want the display to start showing the time immediately.

Congratulations on successfully uploading the code to the conductor's Raspberry Pi Pico W!