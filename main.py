import json
import logging
import multiprocessing
from collections import deque

from labjack import ljm

import DataLogger
import InterfaceUI

def main():
    try: 
        handle = ljm.openS("ANY","ANY","ANY")
    except ljm.LJMError:
        logging.error("Could not connect to Labjack via Ethernet, restart program")
        exit()
    
    with open("styleConfig.json","r") as f:
        fileObj = json.load(f)
        instrumentStyle = fileObj["instrumentStyle"]
        windowStyle = fileObj["windowStyle"]
        logConfig = fileObj["logSettings"]

    with  open("windowConfig.json","r") as f:
        fileObj = json.load(f)
        instrumentConfigs = fileObj["instruments"]
    
    #Add indexes for multiprocessing array and value arrays for graphs

    dummyIndex = 0
    for i in instrumentConfigs:
        i["index"] = dummyIndex
        dummyIndex += 1
        if (i["type"] == "Graph"):
            i["values"] = deque([i["yRange"]]*int(i["range"]/i["interval"]),maxlen=int(i["range"]/i["interval"]))
            i["values"].pop()
            i["values"].append(0)

    voltages = multiprocessing.Array('d', range(dummyIndex))
    isWindowOpen = multiprocessing.Value('i', 1)
    isLogging = multiprocessing.Value('i', 0)

    UIProcess = multiprocessing.Process(target=InterfaceUI.UILoop,
                                        args=(voltages,instrumentConfigs,isWindowOpen,isLogging,windowStyle,instrumentStyle,))
    logProcess = multiprocessing.Process(target=DataLogger.LogLoop,
                                         args=(instrumentConfigs,voltages,isWindowOpen,isLogging,logConfig["sampleRateSec"],))

    UIProcess.start()
    logProcess.start()
 
    while (isWindowOpen.value):
        try:
            GetVoltages(voltages,instrumentConfigs,handle)
        except ljm.LJMError:
            isWindowOpen = 0
            pass

    try:
        UIProcess.join(5)
    except:
        UIProcess.terminate()
    try:
        logProcess.join(5)
    except:
        logProcess.terminate()
    try:
        ljm.close(handle)
    except ljm.LJMError:
        logging.error("Closing labjack connection failed")

    exit()

def GetVoltages(voltageData: multiprocessing.Array, instrumentConfigData: dict, labjackHandle: int) -> None:
    for i in instrumentConfigData:
        try: 
            voltageData[i["index"]] = ljm.eReadName(labjackHandle, i["pin"])
        except ljm.LJMError:
            logging.error("An LJM library or hardware error occured")
            raise ljm.LJMError

if (__name__ == "__main__"):
    main()