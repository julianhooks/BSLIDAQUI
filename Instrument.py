import tkinter as tk
import numpy as np
from labjack import ljm

from matplotlib.backends.backend_tkagg import (
    FigureCanvasTkAgg, NavigationToolbar2Tk)
from matplotlib.figure import Figure


class Graph(tk.Widget):
    def __init__(self, inputVariable: str, maxLength: int) -> None:
        self.tkVariable = inputVariable
        self.data = []
        self.length = maxLength
        #do graph setup

        fig = Figure(figsize=(5, 4), dpi=100)
        t = np.arange(0, 3, .01)
        ax = fig.add_subplot()
        line = ax.plot(t, 2 * np.sin(2 * np.pi * t))
        ax.set_xlabel("time [s]")
        ax.set_ylabel("f(t)")

        self.canvas = FigureCanvasTkAgg(fig, master=root)   


    def updateGraph(self) -> None:
        if (len(self.data) == self.length):
            trash = self.data.pop(0)
            self.data.append(float(tk.Frame.getvar(self.tkVariable)))
            return
        elif (len(self.data) <= self.length):
            self.data.append(float(tk.Frame.getvar(self.tkVariable)))
            return
        else:
            while(len(self.data) > self.length):
                trash = self.data.pop(0)
            return

def loadInstrument(parentFrame: tk.Frame, label: str, units: str, rowParam: int, columnParam: int, styleDict: dict) -> None:
    widgetFrame = tk.Frame(parentFrame)
    widgetFrame.grid(sticky=(tk.N,tk.S,tk.E,tk.W))
    widgetFrame.config(padx=styleDict["padding"],pady=styleDict["padding"])
    tk.Label(widgetFrame, text = label, font = (styleDict["labelFont"],styleDict["labelSize"],"normal"), fg=styleDict["labelColor"]).grid(column=0,row=0,columnspan=2)
    tk.Label(widgetFrame, text = units, font = (styleDict["labelFont"],styleDict["labelSize"],"normal"), fg=styleDict["labelColor"]).grid(column=1,row=1)
    tk.Label(widgetFrame, textvariable = label,font = (styleDict["valueFont"],styleDict["valueSize"],"bold"), fg=styleDict["valueColor"]).grid(column=0,row=1)
    widgetFrame.grid(column=columnParam,row=rowParam)
    #widgetFrame.config(background="white")

def loadGraph(parentFrame: tk.Frame, label: str, units: str, rowParam: int, columnParam: int, styleDict: dict) -> None:
    widgetFrame = tk.Frame(parentFrame)
    widgetFrame.grid(sticky=(tk.N,tk.S,tk.E,tk.W))
    widgetFrame.config(padx=styleDict["padding"],pady=styleDict["padding"])
    tk.Label(widgetFrame, text = label, font = (styleDict["labelFont"],styleDict["labelSize"],"normal"), fg=styleDict["labelColor"]).grid(column=0,row=0,columnspan=2)
    #create and pack a graph into this frame
    widgetFrame.grid(column=columnParam,row=rowParam)
    pass

def loadDataVars(masterFrame: tk.Frame, instrumentConfigDict: dict) -> None:
    for i in instrumentConfigDict:
        tk.StringVar(masterFrame, i["label"])

def loadInstruments(mainFrame: tk.Frame, instrumentConfigDict: dict, styleDict: dict) -> None:
    for i in instrumentConfigDict:
        loadInstrument(mainFrame,i["label"],i["unit"],i["row"],i["column"],styleDict)

def updateGraph(masterFrame: tk.Frame, graph: dict, labjackHandle: int) -> None:
    pass

def updateInstrument(masterFrame: tk.Frame, instrument: dict, labjackHandle: int) -> None:
    voltageData = ljm.eReadName(labjackHandle,instrument["pin"])
    scaledData = voltageData*instrument["scalingFactor"] + instrument["offset"]
    masterFrame.setvar(name=instrument["label"],value=str(scaledData)[0:10])

def updateDataVars(masterFrame: tk.Frame, instrumentConfigDict: dict, labjackHandle: int) -> None:
    for i in instrumentConfigDict:
        if (i["type"] == "Number"):
            updateInstrument(masterFrame, i, labjackHandle)
        elif (i["type"] == "Graph"):
            updateGraph(masterFrame, i, labjackHandle)