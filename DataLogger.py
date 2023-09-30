import tkinter as tk
import datetime
import logging
import csv
import multiprocessing

def LogLoop(instrumentConfigData:dict, voltageData: multiprocessing.Array, isOpen: multiprocessing.Value, logging: multiprocessing.Value, logIntervalInSecs) -> None:
    try:
        filehandle = open(str(datetime.datetime.today().strftime("%S_%M_%H_%d_%m_%y"))+".log","x")
    except OSError:
        logging.error("File could not be opened")
        try:
            raise OSError
        except:
            logging.exception('Exception occurred: ')
            raise
    
    #Make sure to include a filehandle.close() in all non-standard exits form this point forward
    
    writer = csv.writer(filehandle)

    #set up units for csv table
    headerRow = ["Time"]
    unitRow = [""]
    for i in instrumentConfigData:
        headerRow.append(i["label"])
        unitRow.append(i["unit"])
    
    #Start logging
    lastLogTime = datetime.datetime.today().timestamp()
    while(isOpen.value):
        if(not logging):
            pass
        elif (datetime.datetime.today().timestamp() - lastLogTime < logIntervalInSecs):
            pass
        else:
            logValues(writer,voltageData,instrumentConfigData)
            lastLogTime = datetime.datetime.today().timestamp()

    #Close file
    filehandle.close()

    return

def logValues(csvHandle: csv.writer, voltageData: multiprocessing.Array, instrumentConfigData: dict):
    row = [datetime.datetime.today().time()]
    for i in instrumentConfigData:
        row.append(voltageData[i["index"]])
    csvHandle.writerow(row)

class DataLogger:
    def __init__(self,mainFrame: tk.Frame,config: dict,instrumentConfig:dict) -> None:
        self.config = config
        self.filehandle = None
        
        self.filehandle = open(str(datetime.datetime.today().strftime("%S_%M_%H_%d_%m_%y"))+".log","x")
        self.writer = csv.writer(self.filehandle)
        self.widgetFrame = mainFrame
        self.startButton = tk.Button(self.widgetFrame, text="Start Data Log", command=self.startLog).grid(row=3,column=0) #These should be in UILoop
        self.stopButton = tk.Button(self.widgetFrame, text="End Data Log", command = self.stopLog).grid(row=3,column=1)

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
            row = [datetime.datetime.today().time()]
            for i in instrumentConfig:
                row.append(masterFrame.getvar(name=i["label"]))
            self.writer.writerow(row)