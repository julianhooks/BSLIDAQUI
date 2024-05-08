import multiprocessing
from collections import deque

def dataProcessorLoop(voltageData: multiprocessing.Array, measurementData: multiprocessing.Array, instruments: dict, 
                      isWindowOpenGlobal: multiprocessing.Value, zeroIndex: multiprocessing.Value) -> None:
    while(isWindowOpenGlobal.value):
        for i in instruments:
            updateInstrument(i,voltageData,measurementData,zeroIndex)

def loadInstruments(instrumentConfigs: dict):
    dummyIndex = 0
    for i in instrumentConfigs:
        i["index"] = dummyIndex
        dummyIndex += 1
        i["workingArray"] = [0]*i["windowLength"] #length of averaging/filtering window
        i["values"] = deque([i["yRange"]]*int(i["range"]/i["interval"]),maxlen=int(i["range"]/i["interval"]))
        i["values"].pop()
        i["values"].append(0)

def updateInstrument(instrument: dict,  voltageData: multiprocessing.Array, measurementData: multiprocessing.Array,zeroIndex: multiprocessing.Value) -> None:
    if(zeroIndex.value == instrument["index"]):
        instrument["offset"] -= measurementData[instrument["index"]]
        instrument["workingArray"] = [0]*instrument["windowLength"]
        zeroIndex.value = -1
    
    if(instrument["customScale"] == True):
        scaledData = customScale(instrument["scaleCommand"],measurementData)*instrument["scalingFactor"] + instrument["offset"]
        nextDataPoint = scaledData
    else:
        scaledData = voltageData[instrument["index"]]*instrument["scalingFactor"] + instrument["offset"]
        nextDataPoint = scaledData

    instrument["workingArray"].pop()
    instrument["workingArray"].insert(0,scaledData)

    if(instrument["smoothing"] == True): #Moving average filter
        nextDataPoint = sum(instrument["workingArray"]) / instrument["windowLength"]

    if(instrument["filtering"] == True): #DSP type beat
        nextDataPoint = 0
        for i in range(min(len(instrument["filterCoefficients"]),instrument["windowLength"])):
            nextDataPoint += (instrument["workingArray"][i])*instrument["filterCoefficients"][i]

    if(instrument["differential"] == True):
        nextDataPoint = (instrument["workingArray"][0]-instrument["workingArray"][1])

    measurementData[instrument["index"]] = nextDataPoint

def customScale(command: list, measurements: multiprocessing.Array) -> float:
    output = 0
    if(command[0] == "calibrate"):
        output = measurements[command[1]]
    if(command[0] == "sum"):
        for i in range(int(len(command)-1)):
            output += measurements[command[i+1]]
    if(command[0] == "calibrate&sum"):
        for i in range(int(len(command)-1)):
            output += measurements[command[i+1][0]]*command[i+1][1] + command[i+1][2]
    return output