from labjack import ljm
import tkinter as tk
import json
import logging
import multiprocessing
from collections import deque

import DataLogger
import Instrument
import InterfaceUI
#TODO: Add crash logging

def main():
    try: 
        handle = ljm.openS("ANY","ETHERNET","ANY")
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
        if (i["type"] == "graph"):
            i["values"] = deque(range(i["range"])) 

    voltages = multiprocessing.Array('d', range(dummyIndex))
    isWindowOpen = multiprocessing.Value('i', 1)

    UIProcess = multiprocessing.Process(target=InterfaceUI.UILoop,
                                        args=(voltages,instrumentConfigs,isWindowOpen,windowStyle,instrumentStyle))
    logProcess = multiprocessing.Process(target=DataLogger.LogLoop,args=(instrumentConfigs,voltages,isWindowOpen))

    root = tk.Tk()

    root.protocol("WM_DELETE_WINDOW", onClosing)

    mainFrame = tk.Frame(root)
    mainFrame.grid()
    mainFrame.config(bg=windowStyle["backgroundColor"])
    mainFrame.config(padx=windowStyle["padding"],pady=windowStyle["padding"])
    mainFrame.grid_columnconfigure(tk.ALL,weight=1,pad=instrumentStyle["margin"],minsize=instrumentStyle["minWidth"])
    mainFrame.grid_rowconfigure(tk.ALL,weight=1,pad=instrumentStyle["margin"],minsize=instrumentStyle["minHeight"])

    Instrument.loadDataVars(root,instrumentConfigs)

    Instrument.loadInstruments(mainFrame,instrumentConfigs,instrumentStyle)

    dataLogger = DataLogger.DataLogger(mainFrame,logConfig,instrumentConfigs)

    while (isWindowOpen):
        GetVoltages(voltages,instrumentConfigs,handle)
        
        InterfaceUI.updateDataVars(mainFrame, instrumentConfigs, handle)
        dataLogger.updateLogger(mainFrame,instrumentConfigs)
        root.update_idletasks()
        root.update()

    dataLogger.stopLog()
    root.destroy()
    ljm.close(handle)

def GetVoltages(voltageData: multiprocessing.Array, instrumentConfigData: dict, labjackHandle: int) -> None:
    for i in instrumentConfigData:
        try: 
            voltageData[i["index"]] = ljm.eReadName(labjackHandle, i["pin"])
        except ljm.LJMError:
            logging.error("An LJM library or hardware error occured")
            raise ljm.LJMError

if (__name__ == "__main__"):
    main()