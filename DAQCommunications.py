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
        print(handle.readline())
        time.sleep(0.5)
        

#Get voltages from labjack
def GetVoltagesUSB(voltageData: multiprocessing.Array, instrumentConfigData: dict, serialHandle: serial.Serial):
    for i in instrumentConfigData:
        #Read voltage
        # Make read request
        serialHandle.write()
        # Wait
        # Read value
        voltageData[i["index"]] = 5.0*(int(serialHandle.read(size = 2))/65536)
        #Error check
        #Set value


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
        
def LoadLabJack() -> None:
    #Attempt to connect to labjack
    try: 
        handle = ljm.openS("ANY","ANY","ANY")
    except ljm.LJMError:
        logging.critical("Could not connect to Labjack.")
    return handle

def LoadSerial() -> serial.Serial:
    handle = serial.Serial()
    handle.baudrate = 115200
    ports = [comport.device for comport in serial.tools.list_ports.comports()]
    for port in ports:
        handle.port = port
        try:
            handle.open()
        except serial.serialutil.SerialException:
            print(port + "is open")
            continue
        if (not handle.is_open):
            continue
        # Test connection?
        # if good, return handle
        # else, move onto next port
    if (not handle.is_open):
        raise serial.SerialException
    return handle
        
if (__name__=="__main__"):
    main()