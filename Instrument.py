import tkinter as tk
import multiprocessing

def loadInstrument(parentFrame: tk.Frame, instrument: dict, styleDict: dict) -> None:
    widgetFrame = tk.Frame(parentFrame)
    widgetFrame.grid(sticky=(tk.N,tk.S,tk.E,tk.W))
    widgetFrame.config(padx=styleDict["padding"],pady=styleDict["padding"])
    tk.Label(widgetFrame, text = instrument["label"], 
             font = (styleDict["labelFont"],styleDict["labelSize"],"normal"), 
             fg=styleDict["labelColor"]).grid(column=0,row=0,columnspan=2)
    tk.Label(widgetFrame, text = instrument["unit"], 
             font = (styleDict["labelFont"],styleDict["labelSize"],"normal"), 
             fg=styleDict["labelColor"]).grid(column=1,row=1)
    tk.Label(widgetFrame, textvariable = instrument["label"],
             font = (styleDict["valueFont"],styleDict["valueSize"],"bold"), 
             fg=styleDict["valueColor"]).grid(column=0,row=1)
    widgetFrame.grid(column=instrument["column"],row=instrument["row"])

def loadDataVars(masterFrame: tk.Frame, instrumentConfigDict: dict) -> None:
    for i in instrumentConfigDict:
        tk.StringVar(masterFrame, i["label"])

def updateInstrument(masterFrame: tk.Frame, instrument: dict,  voltageData: multiprocessing.Array) -> None:
    scaledData = voltageData[instrument["index"]]*instrument["scalingFactor"] + instrument["offset"]
    masterFrame.setvar(name=instrument["label"],value=str(scaledData)[0:10])