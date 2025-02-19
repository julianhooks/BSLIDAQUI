import logging
import multiprocessing
import serial
import serial.serialutil
import serial.tools.list_ports
import time
from labjack import ljm

def main():
    handle = LoadSerial()
    print(handle)
    while(True):
        print("Testing...")
        print(handle.write(b'RD000\n'))
        print(handle.readline()[:-2])
        time.sleep(1)
        
#Get voltages from labjack
def GetVoltagesUSB(voltageData: multiprocessing.Array, instrumentConfigData: dict, serialHandle: serial.Serial):
    for i in instrumentConfigData:
        # Skip for non-voltage inputs
        if (i["pin"] == None):
            continue
        # Read voltage
        # Make read request
        serialHandle.write(b'RD' + i["pin"] + b'\n')
        # Calibrate
        voltageData[i["index"]] = 5.0*(int(serialHandle.readline()[:-2])/1024)


def GetVoltagesLabjack(voltageData: multiprocessing.Array, instrumentConfigData: dict, labjackHandle: int) -> None:
    for i in instrumentConfigData:
        try: 
            voltageData[i["index"]] = ljm.eReadName(labjackHandle, i["pin"])
        except KeyError:
            #logging.debug(f"{i["label"]} has no assigned pin.")
            pass
        except ljm.LJME_INVALID_NAME:
            #logging.debug(f"{i["label"]} has no assigned pin.")
            if (i["pin"] == None):
                pass
            else:
                raise ljm.LJMError     
        except ljm.LJMError:
            raise ljm.LJMError
        except UnboundLocalError:
            raise UnboundLocalError
        
def LoadLabJack() -> int:
    #Attempt to connect to labjack
    try: 
        handle = ljm.openS("ANY","ANY","ANY")
    except ljm.LJMError:
        logging.critical("Could not connect to Labjack.")
    return handle

def LoadSerial() -> serial.Serial:
    handle = serial.Serial()
    handle.baudrate = 115200
    handle.timeout = 1
    ports = [comport.device for comport in serial.tools.list_ports.comports()]
    for port in ports:
        handle.port = port
        try:
            handle.open()
        except serial.serialutil.SerialException:
            pass
        if (not handle.is_open):
            continue
        
        # Test connection
        # if good, return handle
        # else, move onto next port
        time.sleep(1)
        handle.write(b'whatislove\n')
        response = handle.read(64)
        if (response.find(b'babydonthurtme') == -1):
            logging.info(f"Connection to port {port} failed.")
            continue
        else:
            logging.info(f"Successfully established connection on port {port}.")
            return handle
        
    if (not handle.is_open):
        raise serial.SerialException
    return None
        
if (__name__=="__main__"):
    main()