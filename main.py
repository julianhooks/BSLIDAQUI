from labjack import ljm
import tkinter as tk
import tkinter.font as tkFont
import json
import datetime
import csv

isWindowOpen = True

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

class DataLogger:
    def __init__(self,mainFrame: tk.Frame,config: dict,instrumentConfig:dict) -> None:
        self.config = config
        self.filehandle = None
        try:
            self.filehandle = open(str(datetime.datetime.today().strftime("%S_%M_%H_%d_%m_%y"))+".log","x")
        except:
            print("Could not open a logfile")
        
        self.writer = csv.writer(self.filehandle)
        self.widgetFrame = mainFrame
        self.startButton = tk.Button(self.widgetFrame, text="Start Data Log", command=self.startLog).grid(row=3,column=0)
        self.stopButton = tk.Button(self.widgetFrame, text="End Data Log", command = self.stopLog).grid(row=3,column=1)
        self.isLogging = False
        self.lastLogTime = datetime.datetime.today().timestamp()
        self.logIntervalSec = config["sampleRateSec"]

        headerRow = ["Time"]
        unitRow = [""]

        for i in instrumentConfig:
            headerRow.append(i["label"])
            unitRow.append(i["unit"])

        self.writer.writerow(headerRow)
        self.writer.writerow(unitRow)

    def __del__(self) -> None:
        if (self.filehandle):
            self.filehandle.close()
        pass

    def startLog(self):
        self.isLogging = True
    
    def stopLog(self):
        self.isLogging = False

    def updateLogger(self, masterFrame: tk.Frame, instrumentConfig: dict):
        if ((datetime.datetime.today().timestamp() - self.lastLogTime > self.logIntervalSec) and self.isLogging):
            self.lastLogTime = datetime.datetime.today().timestamp()
            row = [datetime.datetime.today().time()] #TODO: add timestamp
            for i in instrumentConfig:
                row.append(masterFrame.getvar(name=i["label"]))
            self.writer.writerow(row)

def onClosing():
    global isWindowOpen
    isWindowOpen = False

def main():
    #Open connection to labjack via ETHERNET
    try: 
        handle = ljm.openS("ANY","ETHERNET","ANY")
    except:
        print("Could not connect to Labjack via Ethernet, restart program")
        #TODO: Add a popup box to display this message
        #exit()
    
    with open("config.json","r") as f:
        superObj = json.load(f)
        instrumentConfigs = superObj["instruments"]
        instrumentStyle = superObj["instrumentStyle"]
        windowStyle = superObj["windowStyle"]
        logConfig = superObj["logSettings"]

    root = tk.Tk()
    
    root.protocol("WM_DELETE_WINDOW", onClosing)

    mainFrame = tk.Frame(root)
    mainFrame.grid()
    mainFrame.config(bg=windowStyle["backgroundColor"])
    mainFrame.config(padx=windowStyle["padding"],pady=windowStyle["padding"])
    mainFrame.config()
    

    loadDataVars(root,instrumentConfigs)

    loadInstruments(mainFrame,instrumentConfigs,instrumentStyle)

    dataLogger = DataLogger(mainFrame,logConfig,instrumentConfigs)

    mainFrame.grid_columnconfigure(tk.ALL,weight=1,pad=instrumentStyle["margin"],minsize=instrumentStyle["minWidth"])
    mainFrame.grid_rowconfigure(tk.ALL,weight=1,pad=instrumentStyle["margin"],minsize=instrumentStyle["minHeight"])

    while (isWindowOpen):
        updateDataVars(mainFrame, instrumentConfigs, handle)
        dataLogger.updateLogger(mainFrame,instrumentConfigs)
        root.update_idletasks()
        root.update()

    dataLogger.stopLog()
    root.destroy()
    ljm.close(handle)

if (__name__ == "__main__"):
    main()