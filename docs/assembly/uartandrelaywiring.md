# UART and Relay Wiring

UART (Universal Asynchronous Receiver-Transmitter) facilitates communication between the conductor and the digit PCBs. The conductor acts as the central hub, transmitting commands and receiving status updates from the digits.

1. **Conductor (Transmitter and Receiver)**:
      - The conductor's UART `Tx` (transmit) pin sends data to the digits, such as display commands and brightness levels.
      - The conductor's UART `Rx` (receive) pin listens for acknowledgment or status updates from the digits.
2. **Digits (Receivers and Transmitters)**:
      - Each digit PCB's UART `Rx` pin receives commands from the conductor.
      - The digit PCBs' UART `Tx` pins send status updates or responses back to the conductor.

This bidirectional communication ensures synchronized operation of the display, enabling the conductor to manage all digits effectively.

## UART Wiring

The UART wiring diagram illustrates the communication connections between the conductor and the digit PCBs. It shows how the UART `Tx` (transmit) and `Rx` (receive) pins are connected using the two UART channels 0 and 1.

- The conductor's channel 1 `Tx` pin is connected to the channel 1 `Rx` pin on the digit 2 PCB. The conductor PCB has tracing that connects the conductor's channel 0 `Tx` pin to channel 0 `Rx` pin on digit 1.
- The conductor's channel 1 `Rx` pin is connected to the channel 1 `Tx` pin of the digit 2 PCB. The conductor PCB has tracing that connects the conductor's channel 0 `Rx` pin to channel 0 `Tx` pin on digit 1.
- Digit 2 and 3 PCB's `Tx` pins are connected and Digit 0 PCB and Digit 1 on the conductor PCB's `Tx` pin are connected. The same is true for the `Rx` pins for Digits 0-3.

![uartwiring](../img/uartwiring/uartwiring.webp)

Note the wire color references in the section below are in yellow and blue which can be substituted by white and black.

1. Follow the picture below for Digit 0 and 1 UART wiring. On Digit 0 PCB, **(A)** connect the yellow (white) wire to the `Rx-0` and the blue (black) wire to the `Tx-0` terminal block connector. Route the wires to the Digit 1 `Rx-0` and `Tx-0` terminal block connectors and give the wires about 10mm of extra length, then cut. **(B)** Slide the heat shrink over the wires and position them according to the picture. On Digit 1 PCB, **(C)** connect the yellow (white) wire to the `Rx-0` and the blue (black) wire to the `Tx-0` terminal block connector.
![uartwiring-1](../img/uartwiring/uartwiring-1.webp)
1. Follow the picture below for Digit 2 and 3 UART wiring. On Digit 2 PCB, **(A)** connect the yellow (white) wire to the `Rx-1` and the blue (black) wire to the `Tx-1` terminal block connector. Route the wires to the Digit 3 `Rx-1` and `Tx-1` terminal block connectors and give the wires about 10mm of extra length, then cut. **(B)** slide the heat shrink over the wires and position them according to the picture. On Digit 3 PCB, **(C)** connect the yellow (white) wire to the `Rx-1` and the blue (black) wire to the `Tx-1` terminal block connector.
![uartwiring-2](../img/uartwiring/uartwiring-2.webp)
1. Follow the picture below for the conductor to Digit 2 UART wiring. On the conductor PCB, **(A)** connect the yellow (white) wire to the `Rx-1` and the blue (black) wire to the `Tx-1` terminal block connector. Route the wires to the Digit 2 `Rx-1` and `Tx-1` terminal block connectors and give the wires about 10mm of extra length, then cut. On Digit 3 PCB, **(C)** connect the yellow (white) wire to the `Tx-1` and the blue (black) wire to the `Rx-1` terminal block connector.
![uartwiring-3](../img/uartwiring/uartwiring-3.webp)

## Relay Wiring

1. Follow the picture below starting from the back side of the conductor PCB. Using any color 28 AWG wire, connect the **(A)** terminal block connector pin `GPIO19` from the conductor PCB to the **(B)** terminal block connector pin `GPIO19` on the power management PCB.
![relaywiring-1](../img/uartwiring/relaywiring-1.webp)
1. Following the picture below, turn the conductor PCB over so the front face is up. **(A)** Strip 3mm of insulation then tin the stripped end with solder. Connect the white wire to the `+` on the `5v-OUT` terminal block connector and the black wire onto the `-`. **(B)** Route the white wire to the `5v +` and the black wire to the `5v -` on the power management PCB, then cut the wires with at least 2cm of slack. Strip 3mm of insulation, tin the stripped end with solder, then connect each wire to the appropriate terminal block connector.
![relaywiring-2](../img/uartwiring/relaywiring-2.webp)
1. Following the picture below, position the heat shrink and apply heat with a heat gun. Add the two remaining M1.7x6mm self tapping screws to the power management PCB. Ensure all 4 screws securing the power management PCB are snug, but do not over tighten.
![relaywiring-3](../img/uartwiring/relaywiring-3.webp)
