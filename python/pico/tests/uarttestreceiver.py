from common.uart_protocol import uartProtocol, uartChannel, uartCommand, commandHelper, uartActions
import time

def main():
    uart0 = uartProtocol(0, commandHelper.baudRate[3])
    time.sleep(.2)
    uart0.clearQueue()
    uart1 = uartProtocol(1, commandHelper.baudRate[3])
    time.sleep(.2)
    uart1.clearQueue()
    
    while True:
        time.sleep(.1)
        try:
            cmd = uart0.receiveCommand()
            if cmd is not None:
                print("SUCCESS! Received reply from uart0 = {0}".format(cmd.cmdStr))
                #uart0.sendCommand('0FF')
            else:
                print("no reply from uart0")
        except Exception as e:
            print("Exception: {0}".format(e))
            cmd = None
        finally:
            pass

        time.sleep(.1)
        try:
            cmd = uart1.receiveCommand()
            if cmd is not None:
                print("SUCCESS! Received reply from uart1 = {0}".format(cmd.cmdStr))
            else:
                print("no reply from uart1")
        except Exception as e:
            print("Exception: {0}".format(e))
            cmd = None
        finally:
            pass
            
        


if __name__ == "__main__":
    main()