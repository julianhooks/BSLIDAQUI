### Requirements
* Live readings for all sensors
* Scaling equations to convert voltage values to units
* data logging
* clear indication of where each value is coming from on the stand
### How
* Backend is the labjack ljm python library, which lets us connect tothe T7 over ethernet and read values from its inputs in real time (hopefully)
* Frontend will be some sort of easy to use python GUI Library
 * currently looking like Tkinter since its so well supported
#### Vague-vague program structure
1. Initialize GUI
2. Attempt to open connection to T7
 1. If connection fails, Error to GUI and wait for user instruction to reattempt connection
3. Load monitoring GUI
4. Open new logfile
5. Begin Loop
 1. Read values from T7
 2. Scale values
 3. Send values to GUI
 4. Log values in logfile
 5. Repeat until user quit
6. Close logfile
7. Close connection to T7
8. Close GUI