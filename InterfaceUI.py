import tkinter as tk
import multiprocessing
import time

import Graphs
import Instrument

isWindowOpen = True

def loadWidgets(mainFrame: tk.Frame, instrumentConfigDict: dict, styleDict: dict, isLoggingQueue: multiprocessing.queue) -> None:
    for i in instrumentConfigDict:
        if (i["type"] == "number"):
            Instrument.loadInstrument(mainFrame,i,styleDict)
        elif (i["type"] == "graph"):
            Graphs.loadGraph(mainFrame,i,styleDict)
    # LOAD LOGGING BUTTONS
        tk.Button(mainFrame, text="Start Data Logging", command=isLoggingQueue.queue(1)).grid(row=3,column=0)
        tk.Button(mainFrame, text="End Data Loging", command =isLoggingQueue.queue(0)).grid(row=3,column=1)

def updateWidgets(masterFrame: tk.Frame, instrumentConfigDict: dict, voltageData: multiprocessing.Array) -> None:
    for i in instrumentConfigDict:
        if (i["type"] == "Number"):
            Instrument.updateInstrument(masterFrame, i, voltageData)
        elif (i["type"] == "Graph"):
            Graphs.updateGraph(i, voltageData)

def UILoop(voltageData: multiprocessing.Array, instrumentConfigData: dict, isWindowOpenGlobal: multiprocessing.Value, isLogging: multiprocessing.Value, windowStyle: dict, instrumentStyle: dict) -> None:
    
    root = tk.Tk()

    root.protocol("WM_DELETE_WINDOW", onClosing)

    mainFrame = tk.Frame(root)
    mainFrame.grid()
    mainFrame.config(bg=windowStyle["backgroundColor"])
    mainFrame.config(padx=windowStyle["padding"],pady=windowStyle["padding"])
    mainFrame.grid_columnconfigure(tk.ALL,weight=1,pad=instrumentStyle["margin"],minsize=instrumentStyle["minWidth"])
    mainFrame.grid_rowconfigure(tk.ALL,weight=1,pad=instrumentStyle["margin"],minsize=instrumentStyle["minHeight"])

    #Add logging buttons

    loadWidgets(mainFrame,instrumentConfigData,instrumentStyle)
    Instrument.loadDataVars(mainFrame,instrumentConfigData)

    while(isWindowOpen):
        startTime = time.time()
        updateWidgets()
        root.update()
        root.update_idletasks()
        #Add an update buffer to smooth graphs?
        while(time.time()-startTime < 0.04): #25 FPS lock
            pass
    
    isWindowOpenGlobal.value = int(isWindowOpen)