import json
import logging
import multiprocessing
from collections import deque
import time
import datetime

from labjack import ljm

import DataLogger
import InterfaceUI
import DataProcessor

def main():

    logging.info(f'UI started at {datetime.datetime.today()}')

    try: 
        handle = ljm.openS("ANY","ANY","ANY")
    except ljm.LJMError:
        logging.critical("Could not connect to Labjack.")
    
    with open("config.json","r") as f:
        fileObj = json.load(f)
        instrumentStyle = fileObj["instrumentStyle"]
        windowStyle = fileObj["windowStyle"]
        logConfig = fileObj["logSettings"]
    
    try:
        with  open(logConfig["configFilePath"],"r") as f:
            fileObj = json.load(f)
            instrumentConfigs = fileObj["instruments"]
    except OSError:
        logging.error(f"Window config file {logConfig['configFilePath']} does not exist.")
        exit()
    except KeyError:
        logging.error(f"config file does not include key \" configFilePath \".")
        exit()
    
    #Add indexes for multiprocessing array and value arrays for graphs

    DataProcessor.loadInstruments(instrumentConfigs)

    voltages = multiprocessing.Array('d', range(len(instrumentConfigs)))
    measurements = multiprocessing.Array('d', range(len(instrumentConfigs)))
    isWindowOpen = multiprocessing.Value('i', 1)
    isLogging = multiprocessing.Value('i', 0)
    zero = multiprocessing.Value('i', -1)
    logInterval = multiprocessing.Value('f', logConfig["defaultSampleRateSec"])

    UIProcess = multiprocessing.Process(target=InterfaceUI.UILoop,
                                        args=(measurements,instrumentConfigs,isWindowOpen,isLogging,windowStyle,
                                              instrumentStyle,logConfig,logInterval,zero,))
    logProcess = multiprocessing.Process(target=DataLogger.LogLoop,
                                         args=(instrumentConfigs,measurements,isWindowOpen,isLogging,logInterval,))
    dataProcess = multiprocessing.Process(target=DataProcessor.dataProcessorLoop,
                                          args=(voltages,measurements,instrumentConfigs,isWindowOpen,zero,))

    dataProcess.start()
    logging.info(f'Calibrating process started')

    logProcess.start()
    logging.info(f'Logging process started')

    UIProcess.start()
    logging.info(f'UI process started')
 
    while (isWindowOpen.value):
        try:
            GetVoltages(voltages,instrumentConfigs,handle)
        except ljm.LJMError:
            logging.critical("An LJM library or hardware error occured")
            isWindowOpen.value = 0
            break
        except UnboundLocalError:
            logging.critical("Labjack not connected")
            isWindowOpen.value = 0
            break
        except:
            break

    try:
        UIProcess.join(5)
    except:
        logging.error("Joining UI process failed")
        UIProcess.terminate()

    try:
        logProcess.join(5)
    except:
        logging.error("Joining logging process failed")
        logProcess.terminate()

    try:
        dataProcess.join(5)
    except:
        logging.error("Joining calibrating process failed")
        dataProcess.terminate()

    try:
        ljm.close(handle)
    except ljm.LJMError:
        logging.error("Closing labjack connection failed")
    except UnboundLocalError:
        logging.error("Labjack not connected at program termination")
        pass #Case where there is no connection to disconnect

    exit()

def GetVoltages(voltageData: multiprocessing.Array, instrumentConfigData: dict, labjackHandle: int) -> None:
    for i in instrumentConfigData:
        try: 
            voltageData[i["index"]] = ljm.eReadName(labjackHandle, i["pin"])
        except ljm.LJMError:
            raise ljm.LJMError
        except UnboundLocalError:
            raise UnboundLocalError

if (__name__ == "__main__"):
    main()
