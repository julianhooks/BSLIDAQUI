import tkinter as tk
import multiprocessing

import numpy as np
import matplotlib.figure
import matplotlib.animation
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

import Instrument

#Embedded matplotlib bs, see global declaration in function
ani = []

#Shift graph value array right by one, add most recent value from calibration process
def updateGraph(graph: dict, meaurementData: multiprocessing.Array) -> None:
    graph["values"].pop()
    graph["values"].appendleft(meaurementData[graph["index"]])

def loadGraph(parentFrame: tk.Frame, graph: dict, styleDict: dict, zeroIndex: multiprocessing.Value) -> None:
    #setting up the tk frame
    widgetFrame = tk.Frame(parentFrame)
    widgetFrame.grid(sticky=(tk.N,tk.S,tk.E,tk.W))
    widgetFrame.config(padx=styleDict["padding"],pady=styleDict["padding"],background = styleDict["backgroundColor"])

    #Don't understand why I did this, probably redundant
    globalColumn = graph["column"]
    globalRow = graph["row"]

    graph["column"] = 0
    graph["row"] = 0

    #Load attached instrument
    Instrument.loadInstrument(widgetFrame,graph,styleDict)

    #setting up the matplot plot
    fig = matplotlib.figure.Figure(figsize=(3, 3), dpi=0.9*styleDict["minHeight"]) #the decimal*dpi can be tuned to user preference, 0.9 worked for me
    ax = fig.add_subplot()

    #create numpy array of proper size
    t = np.arange(0, graph["range"], graph["interval"])

    #create plot
    line, = ax.plot(t, graph["values"])

    #define the animation function, since it's within this function we can use variables in our upper scope
    def animate(i):
        line.set_ydata(np.array(graph["values"]))  # update the data.
        return line,
    
    #add units and title
    ax.set_xlabel("time [s]")
    ax.set_ylabel(graph["unit"])
    ax.set_title(graph["label"])

    #Create tk canvas widget to hold matplot plot
    canvas = FigureCanvasTkAgg(fig, master=widgetFrame)
    canvas.draw()

    #Place widget below instrument
    canvas.get_tk_widget().grid(row=1,column=0)

    #The FuncAnimation used for each graph must last as long as the animation, 
    #so we have to delare a global variable to avoid the function being destroyed
    #when the loadGraph function ends. By appending to a list instead of setting 
    #a unique variable, we allow for multiple independent graphs.

    global ani

    ani.append(matplotlib.animation.FuncAnimation(fig, animate, interval=20, blit=True, save_count=50))

    #Zero button sends index of graph to calibration process for zeroing
    def zero() -> None:
        zeroIndex.value = graph["index"]
        print(f'zeroing {graph["index"]}')

    tk.Button(widgetFrame, text = "Zero", command = zero, 
              padx = styleDict["padding"], pady = styleDict["padding"],
              font = (styleDict["labelFont"],styleDict["labelSize"],"normal"),
              background = styleDict["backgroundColor"]).grid(row=2,column=0)

    #Place completed widget in window
    widgetFrame.grid(column=globalColumn,row=globalRow,rowspan=4)