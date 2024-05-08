import datetime
import logging
import csv
import multiprocessing

def LogLoop(instrumentConfigData:dict, measurements: multiprocessing.Array, isOpen: multiprocessing.Value, 
            isLogging: multiprocessing.Value, logIntervalInSecs: multiprocessing.Value) -> None:
    try:
        filehandle = open("Logs/"+str(datetime.datetime.today().strftime("%H:%M_%d_%m_%y"))+"data.log","x")
    except FileExistsError:
        logging.warning(
            f'Data log file {str(datetime.datetime.today().strftime("%H:%M_%d_%m_%y"))}data.log already exists. \nAppending...')
        filehandle = open("Logs/"+str(datetime.datetime.today().strftime("%H:%M_%d_%m_%y"))+"data.log","+")
    except OSError:
        logging.error("Data log file could not be opened")
        try:
            raise OSError
        except:
            logging.exception('Exception occurred: ')
            raise
    
    #Make sure to include a filehandle.close() in all non-standard exits form this point forward
    
    writer = csv.writer(filehandle)

    #set up units for csv table
    timeRow = [datetime.datetime.today().time()]
    headerRow = ["Time"]
    unitRow = ["Seconds"]
    for i in instrumentConfigData:
        headerRow.append(i["label"])
        unitRow.append(i["unit"])
    
    writer.writerow(timeRow)
    writer.writerow(headerRow)
    writer.writerow(unitRow)

    #Start logging
    logStartTime = datetime.datetime.today().timestamp()
    lastLogTime = datetime.datetime.today().timestamp()
    while(isOpen.value):
        if(not isLogging.value):
            pass
        elif (datetime.datetime.today().timestamp() - lastLogTime < logIntervalInSecs.value):
            pass
        else:
            logValues(writer,measurements,instrumentConfigData,logStartTime)
            lastLogTime = datetime.datetime.today().timestamp()

    #Close file
    filehandle.close()

    return

def logValues(csvHandle: csv.writer, measurements: multiprocessing.Array, instrumentConfigData: dict, startTime: float):
    row = [datetime.datetime.today().timestamp()-startTime]
    for i in instrumentConfigData:
        #row.append(voltageData[i["index"]])
        row.append(measurements[i["index"]])
    csvHandle.writerow(row)