import tkinter as tk
import multiprocessing
import time
import logging

import Graphs
import Instrument

#Might be pointless
isWindowOpen = True

#Graphics setup function
def loadWidgets(mainFrame: tk.Frame, instrumentConfigDict: dict, styleDict: dict, logDict: dict, isLogging: multiprocessing.Value, 
                zeroIndex: multiprocessing.Value, logInterval: multiprocessing.Value) -> None:
    
    #For instruments with a visibile type (not hidden), create and place widgets
    for i in instrumentConfigDict:
        if (i["type"] == "Number"):
            Instrument.loadInstrument(mainFrame,i,styleDict)
        elif (i["type"] == "Graph"):
            Graphs.loadGraph(mainFrame,i,styleDict,zeroIndex)

    #Creates tk strings for all instruments
    Instrument.loadDataVars(mainFrame,instrumentConfigDict)

    #Logging UI

    #tk string for user input 
    logFreqText = tk.StringVar()

    #tk string for logging state
    logHeaderText = tk.StringVar()
    logHeaderText.set("Not Logging")

    #Logging header
    tk.Label(mainFrame,textvariable=logHeaderText, font = (styleDict["labelFont"],styleDict["labelSize"],"normal"), 
              background = styleDict["backgroundColor"]).grid(row=0,column=5)

    #Logging control buttons

    def startLog():
        isLogging.value = 1
        logHeaderText.set(f'Logging at {int((1/logInterval.value) + 0.01)}Hz')

    startButton = tk.Button(mainFrame, text="Start Data Logging", command = startLog, 
              font = (styleDict["labelFont"],styleDict["labelSize"],"normal"), 
              background = styleDict["backgroundColor"]).grid(row=1,column=5)

    def stopLog():
        isLogging.value = 0
        logHeaderText.set("Not Logging")

    stopButton = tk.Button(mainFrame, text="End Data Logging", command = stopLog, 
              font = (styleDict["labelFont"],styleDict["labelSize"],"normal"), 
              background = styleDict["backgroundColor"]).grid(row=2,column=5)
    
    #Log frequency input

    tk.Entry(mainFrame, textvariable=logFreqText,
             font = (styleDict["labelFont"],styleDict["labelSize"],"normal"), 
              background = styleDict["backgroundColor"]).grid(row=3,column=5)
    
    #Set frequency Button

    def updateFrequency():
        try:
            logInterval.value = 1/int(logFreqText.get())
            logHeaderText.set(f'Logging at {int((1/logInterval.value) + 0.01)}Hz')
        except NameError:
            logInterval.value = logDict["defaultSampleRateSec"]
            logging.error(f'{logFreqText.get()} is not an integer frequency value')

    setLogButton = tk.Button(mainFrame, text="Set Log Frequency", command = updateFrequency, 
              font = (styleDict["labelFont"],styleDict["labelSize"],"normal"), 
              background = styleDict["backgroundColor"]).grid(row=4,column=5)


def updateWidgets(masterFrame: tk.Frame, instrumentConfigDict: dict, measurementData: multiprocessing.Array) -> None:
    for i in instrumentConfigDict:
        if (i["type"] == "Number"):
            Instrument.updateInstrument(masterFrame, i, measurementData)
        elif (i["type"] == "Graph"):
            Graphs.updateGraph(i, measurementData)
            #For instruments attached to graphs
            Instrument.updateInstrument(masterFrame, i, measurementData)

# Full UI setup and event loop
def UILoop(measurementData: multiprocessing.Array, instrumentConfigData: dict, 
           isWindowOpenGlobal: multiprocessing.Value, isLogging: 
           multiprocessing.Value, windowStyle: dict, instrumentStyle: dict, logConfig: dict, logInterval:multiprocessing.Value, 
           zeroIndex: multiprocessing.Value) -> None:
    
    #Set up frame
    root = tk.Tk()
    root.title("Test Stand Data Streamer")

    #X button setup
    def onClosing():
        isWindowOpenGlobal.value = 0

    root.protocol("WM_DELETE_WINDOW", onClosing)

    mainFrame = tk.Frame(root)

    #Configure window
    mainFrame.grid()
    mainFrame.config(bg=windowStyle["backgroundColor"])
    mainFrame.config(padx=windowStyle["padding"],pady=windowStyle["padding"])
    mainFrame.grid_columnconfigure(tk.ALL,weight=1,pad=instrumentStyle["margin"],minsize=instrumentStyle["minWidth"])
    mainFrame.grid_rowconfigure(tk.ALL,weight=1,pad=instrumentStyle["margin"],minsize=instrumentStyle["minHeight"])

    #Configure window contents
    loadWidgets(mainFrame,instrumentConfigData,instrumentStyle, logConfig, isLogging, zeroIndex, logInterval)

    #Event loop
    while(isWindowOpenGlobal.value):
        #tk rigamarole
        root.update()
        root.update_idletasks()
        
        updateWidgets(mainFrame,instrumentConfigData,measurementData)
       
        #25 FPS lock to make graphs update smoother
        startTime = time.time()
        while(time.time()-startTime < 0.04): 
            pass
    
    #tk memory cleanup
    isWindowOpenGlobal.value = 0
    root.destroy()

    exit()