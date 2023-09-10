import tkinter as tk
import datetime
import csv

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