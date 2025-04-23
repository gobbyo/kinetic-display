# Display Face and PCBs Assembly with Integration Testing

This guide details assembling the PCBs onto the display face and includes integration testing of the electronic components that make the Kinetic Display function.

## Prerequisites

- Completed assembly of all PCBs, including the conductor, digit, and power management PCBs.
- Wired and calibrated buck modules.
- Installed UART and relay wiring.

***Table of components***

| Quantity | Component | Image |
| :--: | :------ | :-----: |
| 30 | M1.7x8mm Cross Round Head with Washer Self Tapping Screw 304 Stainless Steel Screws | ![component-32](../img/component/component-32.webp) |

***Table of tools***

| Required | Tool | Image |
| :---: | :------- | :---: |
| Yes | Fine-tipped Philips head screwdriver | ![tool-17](../img/tools/tool-17.webp) |

## Display Face and PCBs Assembly

1. Connect the two 3D-printed sides of the display face with the front facing down onto your workbench. The cove on the backside of the display face should be on the top, furthest from you. See the picture in the next step with the conductor PCB tilted upward to unveil the position of the cove.
1. Position the stand and PCBs atop the display face as shown in the picture below. Ensure the wiring fits in the cove and the gaskets of the PCBs are flush against the display face without any wires protruding.  
   ![displayfacepcb-1](../img/displayfacepcbs/displayfacepcbs-1.webp)
1. Using a small Philips head screwdriver, secure the PCBs with M1.7x8mm self-tapping screws in the locations highlighted below.  
   ![displayfacepcb-2](../img/displayfacepcbs/displayfacepcbs-2.webp)
1. Following the picture below:
      - **(A)** Connect the DHT22 sensor to the conductor PCB.
      - **(B)** Plug in the 12V power supply into the power management PCB's barrel jack. Note: The DHT22 sensor connection is temporary and will be permanently installed later.
      - **(C)** Connect your computer's USB cable to the conductor PCB Raspberry Pi Pico W 2040.  
   ![displayfacepcb-3](../img/displayfacepcbs/displayfacepcbs-3.webp)

!!! warning
    ONLY connect your computer's USB cable to the conductor PCB Raspberry Pi Pico W 2040 AFTER plugging in the 12V power supply. Plugging in your computer's USB cable BEFORE your 12V power supply is plugged in will burn out the sensitive circuitry within the Pico W.

## Integration Test

1. From Visual Studio Code on your computer:
      - **(A)** Click the `_main.py` file in the explorer pane.
      - **(B)** Run the program. Ensure you have a connection via your computer's USB cable to the conductor PCB Raspberry Pi Pico W 2040.  
   ![displayfacepcbtest-1](../img/displayfacepcbs/displayfacepcbtest-1.webp)
1. From Visual Studio Code on your computer, type the `(a)ll digits test` command in the terminal to check the UART connections across the digits. See the video below to verify the segments animate from digit 3 to digit 0.  
   ![displayfacepcbtest-2](../img/displayfacepcbs/displayfacepcbtest-2.webp)  
   ![alldigitstest](../img/displayfacepcbs/alldigitstest.webp)
1. From the command terminal pane, use the `(r)elay (0=off,1=on)` command by typing `r0` (off) then `r1` (on) to check the relay functionality. See the video below with the LEDs on the buck converters turning on and off.  
   ![displayfacepcbtest-3](../img/displayfacepcbs/displayfacepcbtest-3.webp)  
   ![relaytest](../img/displayfacepcbs/relaytest.webp)
1. From the command terminal pane, use the `(t)emp(0=C,1=F)` command by typing `t0` or `t1` to display the temperature (respectively) in Celsius or Fahrenheit. You'll need to tip the display up on one side to view the front of the display as shown in the video below.  
   ![displayfacepcbtest-4](../img/displayfacepcbs/displayfacepcbtest-4.webp)  
   ![temperaturetest](../img/displayfacepcbs/temperaturetest.webp)
1. From the command terminal pane, use the `(l)uminosity` command while shielding the LDR with your hand (or turning off the light in your room). You won't see any command output, only a change in the brightness of the display. If the LED colons are brighter or dimmer than the digit LEDs, adjust the `LEDbrightnessFactor` setting in the `digit_colons.py` file. Presently, the LED colons are set to about 1/3rd the power of the digit LEDs. After making changes to the `LEDbrightnessFactor`, upload the updated file to the controller's Raspberry Pi Pico W 2040.  
   ![displayfacepcbtest-5](../img/displayfacepcbs/displayfacepcbtest-5.webp)  
   ![brightnesstest](../img/displayfacepcbs/brightnesstest.webp)
1. From your Visual Studio Code file explorer pane:
    Open the `secrets.py` file and change the `usr` and `pwd` to your network SSID and password so the Kinetic Display can connect to your local Wi-Fi network. This step is optional and can be done later.
1. At the bottom of the `_main.py` file:
      - Comment out the `manual()` call and uncomment the `loop()` call.
      - Rename `_main.py` to `main.py`.
      - Upload the project to the controller's Raspberry Pi Pico W 2040.

!!! warning
    Forgetting to upload the renamed `main.py` file to the controller's Raspberry Pi Pico W 2040 will cause the Kinetic Display to be unresponsive.
