# UART and Relay Wiring

UART (Universal Asynchronous Receiver-Transmitter) facilitates communication between the controller and the digit PCBs. The controller acts as the central hub, transmitting commands and receiving status updates from the digits.

1. **Controller (Transmitter and Receiver)**:
   - The controller's UART `Tx` (transmit) pin sends data to the digits, such as display commands and brightness levels.
   - The controller's UART `Rx` (receive) pin listens for acknowledgment or status updates from the digits.
2. **Digits (Receivers and Transmitters)**:
   - Each digit PCB's UART `Rx` pin receives commands from the controller.
   - The digit PCBs' UART `Tx` pins send status updates or responses back to the controller.

This bidirectional communication ensures synchronized operation of the display, enabling the controller to manage all digits effectively.

## UART Wiring

![uartwiring](../img/uartwiring/uartwiring.webp)

## Relay Wiring