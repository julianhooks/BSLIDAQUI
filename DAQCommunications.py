import logging
import multiprocessing
import time

import serial
import serial.serialutil
import serial.tools.list_ports
from labjack import ljm

def main():
    handle = loadSerial()
    print(handle)
    while(True):
        print("Testing...")
        print(handle.write(b'RD000\n'))
        print(handle.readline()[:-2])
        time.sleep(1)

def getVoltagesLabjack(voltageData: multiprocessing.Array, instrumentConfigData: dict, labjackHandle: int) -> None:
    for i in instrumentConfigData:
        try: 
            voltageData[i["index"]] = ljm.eReadName(labjackHandle, i["pin"])
        except KeyError:
            logging.debug(f"{i['label']} has no assigned pin.")
            pass
        except ljm.LJME_INVALID_NAME:
            logging.debug(f"{i['label']} has no assigned pin.")
            if (i["pin"] == None):
                pass
            else:
                raise ljm.LJMError     
        except ljm.LJMError:
            raise ljm.LJMError
        except UnboundLocalError:
            raise UnboundLocalError
        
def loadLabJack() -> int:
    #Attempt to connect to labjack
    try: 
        handle = ljm.openS("ANY","ANY","ANY")
    except ljm.LJMError:
        logging.critical("Could not connect to Labjack.")
        handle = -1
    return handle

def closeLabJack(handle:int) -> None:
    #Clean up labjack connection
    try:
        ljm.close(handle)
    except ljm.LJMError:
        logging.error("Closing labjack connection failed")
    except UnboundLocalError:
        logging.error("Labjack not connected at program termination")
        pass #Case where there is no connection to disconnect

def getVoltagesUSB(voltageData: multiprocessing.Array, instrumentConfigData: dict, serialHandle: serial.Serial):
    #serialHandle.write_timeout = 0.001
    #serialHandle.timeout = 0.001
    for i in instrumentConfigData:
        # Skip for non-voltage inputs
        # Read voltage
        # Make read request
        serialHandle.write(bytes("RD"+i["pin"]+"\n",encoding="utf8"))
        # Calibrate
        try:
            response = serialHandle.readline()
            if (response == b''):
                continue
            voltageData[i["index"]] = ((5.0*int(response[:-2]))/1024)
        except ValueError:
            logging.info(f"Bad read: {response}")
            pass

def loadSerial() -> serial.Serial:
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

def closeSerial(handle: serial.Serial) -> None:    
    handle.close()
        
if (__name__=="__main__"):
    main()