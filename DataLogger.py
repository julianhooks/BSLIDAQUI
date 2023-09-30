import tkinter as tk
import datetime
import logging
import csv
import multiprocessing

def LogLoop(instrumentConfigData:dict, voltageData: multiprocessing.Array, isOpen: multiprocessing.Value, isLogging: multiprocessing.Value, logIntervalInSecs) -> None:
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
        if(not isLogging.value):
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