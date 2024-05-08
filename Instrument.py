import tkinter as tk
import multiprocessing

#tk setup
def loadInstrument(parentFrame: tk.Frame, instrument: dict, styleDict: dict) -> None:
    #Configure widget frame
    widgetFrame = tk.Frame(parentFrame)
    widgetFrame.grid(sticky=(tk.N,tk.S,tk.E,tk.W))
    widgetFrame.config(padx=styleDict["padding"],pady=styleDict["padding"],background = styleDict["backgroundColor"])
    
    #Setup title
    tk.Label(widgetFrame, text = instrument["label"], 
             font = (styleDict["labelFont"],styleDict["labelSize"],"normal"), 
             fg=styleDict["labelColor"],
             background = styleDict["backgroundColor"]).grid(column=0,row=0,columnspan=2)
    
    #Setup unit
    tk.Label(widgetFrame, text = instrument["unit"], 
             font = (styleDict["labelFont"],styleDict["labelSize"],"normal"), 
             fg=styleDict["labelColor"],
             background = styleDict["backgroundColor"]).grid(column=1,row=1)
    
    #Setup data
    tk.Label(widgetFrame, textvariable = instrument["label"],
             font = (styleDict["valueFont"],styleDict["valueSize"],"bold"), 
             fg=styleDict["valueColor"],
             background = styleDict["backgroundColor"]).grid(column=0,row=1)
    
    #Place instrument in correct grid location
    widgetFrame.grid(column=instrument["column"],row=instrument["row"])

def loadDataVars(masterFrame: tk.Frame, instrumentConfigDict: dict) -> None:
    #Setup tk strings (can probably be included in loadInstrument)
    for i in instrumentConfigDict:
        tk.StringVar(masterFrame, i["label"])

def updateInstrument(masterFrame: tk.Frame, instrument: dict,  measurementData: multiprocessing.Array) -> None:
    #Update data label with most recent value from calibration process
    masterFrame.setvar(name=instrument["label"],value=str(measurementData[instrument["index"]])[0:5])