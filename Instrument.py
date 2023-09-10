import tkinter as tk
from labjack import ljm

def loadInstrument(parentFrame: tk.Frame, label: str, units: str, rowParam: int, columnParam: int, styleDict: dict) -> None:
    widgetFrame = tk.Frame(parentFrame)
    widgetFrame.grid(sticky=(tk.N,tk.S,tk.E,tk.W))
    widgetFrame.config(padx=styleDict["padding"],pady=styleDict["padding"])
    tk.Label(widgetFrame, text = label, font = (styleDict["labelFont"],styleDict["labelSize"],"normal"), fg=styleDict["labelColor"]).grid(column=0,row=0,columnspan=2)
    tk.Label(widgetFrame, text = units, font = (styleDict["labelFont"],styleDict["labelSize"],"normal"), fg=styleDict["labelColor"]).grid(column=1,row=1)
    tk.Label(widgetFrame, textvariable = label,font = (styleDict["valueFont"],styleDict["valueSize"],"bold"), fg=styleDict["valueColor"]).grid(column=0,row=1)
    widgetFrame.grid(column=columnParam,row=rowParam)
    #widgetFrame.config(background="white")


def loadDataVars(masterFrame: tk.Frame, instrumentConfigDict: dict) -> None:
    for i in instrumentConfigDict:
        tk.StringVar(masterFrame, i["label"])

def updateDataVars(masterFrame: tk.Frame, instrumentConfigDict: dict, labjackHandle: int) -> None:
    for i in instrumentConfigDict:
        voltageData = ljm.eReadName(labjackHandle,i["pin"])
        scaledData = voltageData*i["scalingFactor"] + i["offset"]
        masterFrame.setvar(name=i["label"],value=str(scaledData)[0:10])

def loadInstruments(mainFrame: tk.Frame, instrumentConfigDict: dict, styleDict: dict) -> None:
    for i in instrumentConfigDict:
        loadInstrument(mainFrame,i["label"],i["unit"],i["row"],i["column"],styleDict)