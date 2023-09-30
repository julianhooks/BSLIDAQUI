import tkinter as tk
import multiprocessing
import time

import Graphs
import Instrument

isWindowOpen = True

def loadWidgets(mainFrame: tk.Frame, instrumentConfigDict: dict, styleDict: dict, isLogging: multiprocessing.Value) -> None:
    for i in instrumentConfigDict:
        if (i["type"] == "Number"):
            Instrument.loadInstrument(mainFrame,i,styleDict)
        elif (i["type"] == "Graph"):
            Graphs.loadGraph(mainFrame,i,styleDict)

    Instrument.loadDataVars(mainFrame,instrumentConfigDict)

    # LOAD LOGGING BUTTONS

    def startLog():
        isLogging.value = 1

    def stopLog():
        isLogging.value = 0

    tk.Button(mainFrame, text="Start Data Logging", command = startLog).grid(row=3,column=0)
    tk.Button(mainFrame, text="End Data Loging", command = stopLog).grid(row=3,column=1)

def updateWidgets(masterFrame: tk.Frame, instrumentConfigDict: dict, voltageData: multiprocessing.Array) -> None:
    for i in instrumentConfigDict:
        if (i["type"] == "Number"):
            Instrument.updateInstrument(masterFrame, i, voltageData)
        elif (i["type"] == "Graph"):
            Graphs.updateGraph(i, voltageData)

def UILoop(voltageData: multiprocessing.Array, instrumentConfigData: dict, 
           isWindowOpenGlobal: multiprocessing.Value, isLogging: 
           multiprocessing.Value, windowStyle: dict, instrumentStyle: dict) -> None:
    
    root = tk.Tk()

    def onClosing():
        isWindowOpenGlobal.value = 0

    root.protocol("WM_DELETE_WINDOW", onClosing)

    mainFrame = tk.Frame(root)

    mainFrame.grid()
    mainFrame.config(bg=windowStyle["backgroundColor"])
    mainFrame.config(padx=windowStyle["padding"],pady=windowStyle["padding"])
    mainFrame.grid_columnconfigure(tk.ALL,weight=1,pad=instrumentStyle["margin"],minsize=instrumentStyle["minWidth"])
    mainFrame.grid_rowconfigure(tk.ALL,weight=1,pad=instrumentStyle["margin"],minsize=instrumentStyle["minHeight"])

    loadWidgets(mainFrame,instrumentConfigData,instrumentStyle, isLogging)

    while(isWindowOpenGlobal.value):
        root.update()
        root.update_idletasks()
        startTime = time.time()
        updateWidgets(mainFrame,instrumentConfigData,voltageData)
        #Add an update buffer to smooth graphs?
        while(time.time()-startTime < 0.04): #25 FPS lock
            pass
    
    isWindowOpenGlobal.value = 0
    root.destroy()

    exit()