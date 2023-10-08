import tkinter as tk
import multiprocessing
from copy import deepcopy, copy

import numpy as np
import matplotlib.figure
import matplotlib.animation
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

import Instrument

ani = []

def updateGraph(graph: dict, voltageData: multiprocessing.Array) -> None:
    trash = graph["values"].pop()
    graph["values"].appendleft(voltageData[graph["index"]] * graph["scalingFactor"] + graph["offset"])
    #print(graph["values"])

def loadGraph(parentFrame: tk.Frame, graph: dict, styleDict: dict) -> None:
    #setting up the tk frame
    widgetFrame = tk.Frame(parentFrame)
    widgetFrame.grid(sticky=(tk.N,tk.S,tk.E,tk.W))
    widgetFrame.config(padx=styleDict["padding"],pady=styleDict["padding"],background = styleDict["backgroundColor"])

    globalColumn = graph["column"]
    globalRow = graph["row"]

    graph["column"] = 0
    graph["row"] = 0

    Instrument.loadInstrument(widgetFrame,graph,styleDict)

    #setting up the matplot plot
    fig = matplotlib.figure.Figure(figsize=(3, 3), dpi=100)
    t = np.arange(0, graph["range"], graph["interval"]) #replace max with i.range / i.interval
    ax = fig.add_subplot()
    line, = ax.plot(t, graph["values"])

    #define the animation function, since it's within this function we can use variables in our upper scope
    def animate(i):
        line.set_ydata(np.array(graph["values"]))  # update the data.
        return line,
    
    ax.set_xlabel("time [s]")
    ax.set_ylabel(graph["unit"])

    canvas = FigureCanvasTkAgg(fig, master=widgetFrame)  # A tk.DrawingArea.
    canvas.draw()

    canvas.get_tk_widget().grid(row=1,column=0)

    #The FuncAnimation used for each graph must last as long as the animation, 
    #so we have to delare a global variable to avoid the function being destroyed
    #when the loadGraph function ends. By appending to a list instead of setting 
    #a unique variable, we allow for multiple independent graphs.

    global ani

    ani.append(matplotlib.animation.FuncAnimation(fig, animate, interval=20, blit=True, save_count=50))

    def zero() -> None:
        graph["offset"] -= graph["values"][0]

    tk.Button(widgetFrame, text = "Zero", command = zero, 
              padx = styleDict["padding"], pady = styleDict["padding"],
              font = (styleDict["labelFont"],styleDict["labelSize"],"normal"),
              background = styleDict["backgroundColor"]).grid(row=2,column=0)

    widgetFrame.grid(column=globalColumn,row=globalRow,rowspan=4)