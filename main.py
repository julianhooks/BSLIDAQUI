from labjack import ljm
import tkinter as tk
import json
import logging
import DataLogger
import Instrument
#TODO: Add crash logging

isWindowOpen = True

def onClosing():
    global isWindowOpen
    isWindowOpen = False

def main():
    try: 
        handle = ljm.openS("ANY","ETHERNET","ANY")
    except ljm.LJMError:
        print("Could not connect to Labjack via Ethernet, restart program")
        exit()
    
    with open("styleConfig.json","r") as f:
        fileObj = json.load(f)
        instrumentStyle = fileObj["instrumentStyle"]
        windowStyle = fileObj["windowStyle"]
        logConfig = fileObj["logSettings"]

    with  open("windowConfig.json","r") as f:
        fileObj = json.load(f)
        instrumentConfigs = fileObj["instruments"]

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
        Instrument.updateDataVars(mainFrame, instrumentConfigs, handle)
        dataLogger.updateLogger(mainFrame,instrumentConfigs)
        root.update_idletasks()
        root.update()

    dataLogger.stopLog()
    root.destroy()
    ljm.close(handle)

if (__name__ == "__main__"):
    main()