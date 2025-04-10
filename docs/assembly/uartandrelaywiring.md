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

1. Digit 0 and 1 UART wiring.
![uartwiring-1](../img/uartwiring/uartwiring-1.webp)
1. Digit 2 and 3 UART wiring.
![uartwiring-2](../img/uartwiring/uartwiring-2.webp)
1. Controller to Digit 2 UART wiring.
![uartwiring-3](../img/uartwiring/uartwiring-3.webp)

## Relay Wiring

![relaywiring-1](../img/uartwiring/relaywiring-1.webp)

![relaywiring-2](../img/uartwiring/relaywiring-2.webp)

![relaywiring-3](../img/uartwiring/relaywiring-3.webp)