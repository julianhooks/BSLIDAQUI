import json
import logging
import datetime
import re
import sys

logging.basicConfig(level=logging.DEBUG)

def main(filepath) -> None:
    logging.info(f'LayoutChecker started at {datetime.datetime.today()}')

    # Check new configs for all required values, diagnose errors, apply formatting
    layoutFilePath = filepath
    # Load desired config
    try:
        with open(layoutFilePath,"r") as f:
            layoutFileDict = json.load(f)
    except OSError:
        logging.error(f"Window config file {layoutFilePath} does not exist.")
        exit()

    versionNumber = layoutFileDict['version']
    if (versionNumber == 1):
        print("Version 1 layouts are no longer supported, update your layout to version 2.")
    if (versionNumber == 2):
        version2Checks(layoutFileDict)
    if (versionNumber == 3):
        pass

    return

def version2Checks(layout:dict) -> None:
    validTypes = ["Hidden","Number","Graph"]    
    for instrument in layout['instruments']:
        if ("type" not in instrument):
            logging.info(f"{instrument['label']}: has no type")    
        elif (instrument['type'] not in validTypes):
            logging.info(f"{instrument['label']}: type {instrument['type']} is not a valid type")
        else:
            # For version two, number encompasses all of the functions present in hidden and graph encompasses all of the functions in number, so we call all the checks each time
            if (instrument['type'] == "Hidden"):
                hiddenCheckv2(instrument)
            if (instrument['type'] == "Number"):
                hiddenCheckv2(instrument)
                numberCheckv2(instrument)
            if (instrument['type'] == "Hidden"):
                hiddenCheckv2(instrument)
                numberCheckv2(instrument)
                graphCheckv2(instrument)
            
def hiddenCheckv2(instrument:dict) -> None:
    # Check that the instrument contains all necessary keys and keys are of proper types
    # Running prompts with multiple types means that every entry needs an iterable type, so single lists of types are needed 
    requiredKeys = [("pin",[str]),
                    ("label",[str]),
                    ("windowLength",[int]),
                    ("scalingFactor",[int,float]),
                    ("offset",[int,float]),
                    ("customScale",[bool]),
                    ("smoothing",[bool]),
                    ("differential",[bool]),
                    ("filtering",[bool])]
    
    if ("label" not in instrument):
        logging.info(f"Instrument is unlabelled")
        return

    fatalKeyError = False

    for key in requiredKeys:
        if (key[0] not in instrument):
            logging.info(f"{instrument['label']}: missing tag {key[0]}")
            fatalKeyError = True
            continue
        elif (type(instrument[key[0]]) not in key[1]):
            logging.info(f"{instrument['label']}: {key[0]} = {instrument[key[0]]} is not of type {key[1]}")
            

    if (fatalKeyError == True):
        return

    # Check that filter window length is positive and non-zero (sanity check)
    if (instrument['windowLength'] < 1):
        logging.info(f"{instrument['label']}: window length {instrument['windowLength']} is invalid")

    # Check for filter coefficients and windowLength agreements
    if (instrument['filtering'] == True):
        if ("filterCoefficients" not in instrument):
            logging.info(f"{instrument['label']}: filtering is true but filterCoefficients is not present")
        elif (len(instrument['filterCoefficients']) != instrument['windowLength']+1):
            logging.info(f"{instrument['label']}: window length: {instrument['windowLength']} does not agree with number of filter coefficients {len(instrument['filterCoefficients'])}")
    
    # Check custom scale commands
    validCustomCommands = ["sum","calibrate","polyfit4"]
    if (instrument['customScale'] == True):
        # Check for invalid scale commands
        if ("scaleCommand" not in instrument):
            logging.info(f"{instrument['label']}: customScaling is true but scaleCommand is not present")
        elif (instrument['scaleCommand'][0] not in validCustomCommands):
            logging.info(f"{instrument['label']}: command {instrument['scaleCommand']} is not a valid command")
    
        # Check sum command
        if (instrument['scaleCommand'][0] == "sum"):
            for i in range(1,len(instrument['scaleCommand'])):
                if ((instrument['scaleCommand'][i] < 1) or (type(instrument['scaleCommand'][i]) != int)):
                    logging.info(f"{instrument['label']}: invalid index in sum command {instrument['scaleCommand'][i]}")

        # Check calibrate command
        if (instrument['scaleCommand'][0] == "calibrate"):
            if ((instrument['scaleCommand'][1] < 1) or (type(instrument['scaleCommand'][1]) != int)):
                logging.info(f"{instrument['label']}: invalid index in calibrate command {instrument['scaleCommand'][1]}")        

        # Check polyfit command
        if (instrument['scaleCommand'][0] == "polyfit4"):
            if (len(instrument['scaleCommand'][2]) != 4):
                logging.info(f"{instrument['label']}: incorrect number of coefficients in polyfit command")

            if ((instrument['scaleCommand'][1] < 1) or (type(instrument['scaleCommand'][1]) != int)):
                logging.info(f"{instrument['label']}: invalid index in polyfit4 command {instrument['scaleCommand'][1]}")        

            for coeff in instrument['scaleCommand'][2]:
                if ((type(coeff) not in [float,int])):
                    logging.info(f"{instrument['label']}: invalid coefficient in polyfit4 command")

    # Check pin is valid
    pinVerifier = re.compile("AIN\d{1,3}|TEMPERATURE_DEVICE_K|TEMPERATURE_AIR_K")
    if (pinVerifier.match(instrument['pin']) == None):
        logging.info(f"{instrument['label']}: invalid pin {instrument['pin']}")
    if ((instrument['pin'][0:2] == "AIN") and (int(instrument['pin'][3:]) > 255)):
        logging.info(f"{instrument['label']}: invalid pin {instrument['pin']}")

    return

def numberCheckv2(instrument:dict) -> None:
    # Check that the instrument contains all necessary keys and keys are of proper types
    requiredKeys = [("unit",str),
                    ("row",int),
                    ("column",int)] 
    fatalKeyError = False

    for key in requiredKeys:
        if (key[0] not in instrument):
            logging.info(f"{instrument['label']}: missing tag {key[0]}")
            fatalKeyError = True
            continue
        elif (type(instrument[key[0]]) != key[1]):
            logging.info(f"{instrument['label']}: {key[0]} = {instrument[key[0]]} is not of type {key[1]}")

    if (fatalKeyError == True):
        return

    # Check rows and columns make sense
    if (instrument['row'] < 0):
        logging.info(f"{instrument['label']}: invalid row {instrument['row']}")
    if (instrument['column'] < 0):
        logging.info(f"{instrument['label']}: invalid column {instrument['column']}")

    return

def graphCheckv2(instrument:dict) -> None:
    # Check that the instrument contains all necessary keys and keys are of proper types
    requiredKeys = [("range",int),
                    ("interval",float),
                    ("yRange",int)] 
    fatalKeyError = False

    for key in requiredKeys:
        if (key[0] not in instrument):
            logging.info(f"{instrument['label']}: missing tag {key[0]}")
            fatalKeyError = True
            continue
        elif (type(instrument[key[0]]) != key[1]):
            logging.info(f"{instrument['label']}: {key[0]} = {instrument[key[0]]} is not of type {key[1]}")

    if (fatalKeyError == True):
        return

    return

if (__name__ == "__main__"):
    main(sys.argv[1])