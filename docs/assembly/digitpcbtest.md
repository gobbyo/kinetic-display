# Digit PCB Test

Run the tests in this section after assembling each digit PCB to ensure all components are soldered correctly and functional. Any defective electronic component on the digit PCB must be replaced before completing the project.

## Prerequisites

- [Completed digit PCB ready for actuators](./digitpcbassembly.md)
- Computer and microcontroller with the [prerequisite software](../prerequisitesoftware.md)
- An [assembled actuator](actuatorassembly.md)

## Test the Motor and LED Segments

1. **Open the Deployed Project**:  
  From Visual Studio Code, open the deployed `digit` project.
     **(A)** Click the file menu, **(B)** select the `digit` folder, then **(C)** click the **Select Folder** button.  
![testpcbactuator-prerequisite](../img/digitpcbtest/prerequisite.webp)
1. **Connect the Raspberry Pi Pico**:  
      - Plug a USB cable from your computer into the Raspberry Pi Pico's USB port on the digit PCB.  
      - Open the **MicroPico vREPL** in the terminal dropdown as described in [Verify Micropython on your Raspberry Pi Pico](../prerequisitesoftware.md/#verify_micropython_on_your_raspberry_pi_pico).  
![digitpcbtest-1](../img/digitpcbtest/digitpcbtest-2.webp)
1. **Connect the Actuator**:  
      - Plug the Dupont connector from the actuator into the `SEG-A` pins.  
      - Ensure the **white wire** is connected to the `CW` pin and the **black wire** to the `CCW` pin.  
![digitpcbtest-2](../img/digitpcbtest/digitpcbtest-3.webp)
1. **Open the Test File**:  
  From Visual Studio Code, **(A)** click on the `digit.py` file, then **(B)** select the MicroPico vREPL from the terminal menu.  
![digitpcbtest-3](../img/digitpcbtest/digitpcbtest-4.webp)
1. **Run the Test Application**:  
      - **(A)** Verify the connection between your computer and the Raspberry Pi Pico.  
      - **(B)** Click the **Run** button to execute the test application for the digit PCB.  
![digitpcbtest-4](../img/digitpcbtest/digitpcbtest-5.webp)
1. **Test Segment A**:  
      - The console test application displays options for segments 0-6, corresponding to segments A-G.  
      - Extend `SEG-A` by typing **e0** in the console.  
![digitpcbtest-6](../img/digitpcbtest/digitpcbtest-6.webp)
1. **Verify Segment A**:  
      - The 4 `SEG-A` LEDs should light up, and the motor should briefly turn on.  
      - Retract `SEG-A` by typing **r0** in the console.  
![digitpcbtest-7](../img/digitpcbtest/digitpcbtest-7.webp)
1. **Test Remaining Segments**:  
      - Repeat steps 6 and 7 for `SEG-B` through `SEG-G` to verify all segments work as expected.  
      - Perform this test for all digit PCBs (0-3).
