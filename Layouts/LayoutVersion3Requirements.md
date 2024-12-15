"version": int (1/2/3)
- Required

### Panels
- Contain sets of instruments
- instruments in each panel can only access other instruments in the same panel 

### Instruments

"label": string
- Required
- Label of instrument

"type": "Voltage"/"Hidden"/"Number"/"Graph"
- Required
- Voltages are hidden

#### All commands
"customScale": true/false
- Required
"scaleComand": \[command,{parameters}\]
Only necessary if customScale true
- sum {indexes to sum}
  - sum values from a number of indexes and applies linear calibration from scaling factor and offset parameters
- calibrate {index}
  - applies linear calibration from scaling factor and offset parameters
- polyfit4 {index, \[coefficients most to least significant\]}
  - fourth order polynomial fit

"offset": float
- Required
"scalingFactor": float
- Required

"windowLength": int > 0
- Sets the number of samples after the most recent sample that are saved
- Required

"smoothing": true/false
- Applies a moving average filter across the window
  - Adds delay of half of a window length
- Required

"differential": true/false
- Calculates the value as a difference between the last two data points
  - Not normalized by delta T
- Required

"filtering": true/false
- When true, sets the value of the instrument using a set of coefficients across the window
  - Adds delay of half of a window length
  - Overwrites smoothing
- Required
"filterCoefficients": \[float\]
- Array of coefficiencies
- Only necessary if filtering true

#### Voltage only
"pin": "labjackPin"
- Not necessary
- Pulls labjack pin of that name, consult labjack website

#### Number and Graph only commands
"unit": string
- Unit for instrument
"row": int >= 0 
- Grid location left to right
"column": int >= 0
- Grid location top down
- Graphs take 4 column slots total

#### Graph only commands
"range": 50
- x range for graph
"interval": 0.1
- number of data points per interval, total displayed data is x range*interval
"yRange": 20
- range of y axis on graph