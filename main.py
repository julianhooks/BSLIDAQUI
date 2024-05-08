import json
import logging
import multiprocessing
import datetime
from labjack import ljm

import DataLogger
import InterfaceUI
import DataProcessor

def main():
    logging.info(f'UI started at {datetime.datetime.today()}')

    #Attempt to connect to labjack
    try: 
        handle = ljm.openS("ANY","ANY","ANY")
    except ljm.LJMError:
        logging.critical("Could not connect to Labjack.")
    
    #Open config file and load necessary information
    with open("config.json","r") as f:
        fileObj = json.load(f)
        instrumentStyle = fileObj["instrumentStyle"]
        windowStyle = fileObj["windowStyle"]
        logConfig = fileObj["logSettings"]
    
    #Open layout file
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

    #Configure calibration
    DataProcessor.loadInstruments(instrumentConfigs)

    #Shared access arrays for dataprocessing
    
    #This is only edited by the main process and only read by the calibration process
    voltages = multiprocessing.Array('d', range(len(instrumentConfigs)))
    #This is only edited by the calibration orocess and read by the UI and recording processes
    measurements = multiprocessing.Array('d', range(len(instrumentConfigs)))
    
    #Shared access booleans (dirty way of working it)

    #This is edited by the main process and the UI process (very bad) and read by all processes
    isWindowOpen = multiprocessing.Value('i', 1)
    #This is edited by the UI process and read by the recording process
    isLogging = multiprocessing.Value('i', 0)
    
    #Shared access numbers (dirty way of working it)
    #Edited by the UI process and cleared by the calibration process. 
    #Works by sending the index of the measurement array member to be zeroed from the button on its graph widget to the calibration 
    # process where the zeroing is conducted and the value is set back to -1. The -1 value is the safe value since it is an illegal index
    zero = multiprocessing.Value('i', -1)
    #Edited by the UI process and read by the recording process. Sets the interval between recorded data points in the log file
    logInterval = multiprocessing.Value('f', logConfig["defaultSampleRateSec"])

    #Define each parallel process in the multiprocessing library
    UIProcess = multiprocessing.Process(target=InterfaceUI.UILoop,
                                        args=(measurements,instrumentConfigs,isWindowOpen,isLogging,windowStyle,
                                              instrumentStyle,logConfig,logInterval,zero,))
    logProcess = multiprocessing.Process(target=DataLogger.LogLoop,
                                         args=(instrumentConfigs,measurements,isWindowOpen,isLogging,logInterval,))
    dataProcess = multiprocessing.Process(target=DataProcessor.dataProcessorLoop,
                                          args=(voltages,measurements,instrumentConfigs,isWindowOpen,zero,))

    #Start parallel processes
    dataProcess.start()
    logging.info(f'Calibrating process started')

    logProcess.start()
    logging.info(f'Logging process started')

    UIProcess.start()
    logging.info(f'UI process started')
 
    #Main loop
    while (isWindowOpen.value):
        #Try to read voltages from LabJack
        try:
            GetVoltages(voltages,instrumentConfigs,handle)
        #If LabJack is disconnected, exit program
        except ljm.LJMError:
            logging.critical("An LJM library or hardware error occured")
            isWindowOpen.value = 0
            break
        except UnboundLocalError:
            logging.critical("Labjack not connected")
            isWindowOpen.value = 0
            break
        #Any other exception, break
        except:
            break

    #Attempt to clean up parallel processes
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

    #Clean up labjack connection
    try:
        ljm.close(handle)
    except ljm.LJMError:
        logging.error("Closing labjack connection failed")
    except UnboundLocalError:
        logging.error("Labjack not connected at program termination")
        pass #Case where there is no connection to disconnect

    exit()

#Get voltages from labjack
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
