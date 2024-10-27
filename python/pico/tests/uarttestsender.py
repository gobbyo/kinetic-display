from uart_protocol import uartProtocol, uartChannel, uartCommand, commandHelper, uartActions
import time


def main():

    while True:
        for u in range(15):
            for i in range(2):
                print("UART{0} test".format(i))
                uart = uartProtocol(i, commandHelper.baudRate[3])
                uart.clearQueue()
                cmdStr = '0{0}{1:02}'.format(i,u)
                print("sending command: {0}".format(cmdStr))
                cmd = uartCommand(cmdStr)
                uart.sendCommand(cmd)
                time.sleep(1)         
                del(uart)

if __name__ == "__main__":
    main()