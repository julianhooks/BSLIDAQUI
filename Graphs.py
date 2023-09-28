import numpy as np
import tkinter as tk
import multiprocessing

import matplotlib.animation
import matplotlib.figure
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg


def updateGraph(graph: dict, voltageData: multiprocessing.Array) -> None:
    trash = graph["values"].pop()
    graph["values"].append_left(voltageData[graph["index"]])

def loadGraph(parentFrame: tk.Frame, graph: dict, styleDict: dict) -> None:
    #setting up the tk frame
    widgetFrame = tk.Frame(parentFrame)
    widgetFrame.grid(sticky=(tk.N,tk.S,tk.E,tk.W))
    widgetFrame.config(padx=styleDict["padding"],pady=styleDict["padding"])
    tk.Label(widgetFrame, text = graph["label"], font = (styleDict["labelFont"],styleDict["labelSize"],"normal"), fg=styleDict["labelColor"]).grid(column=0,row=0,columnspan=2)

    #setting up the matplot plot
    fig = matplotlib.figure.Figure(figsize=(5, 4), dpi=100)
    t = np.arange(0, graph["range"]*graph["interval"], graph["interval"]) #replace max with i.range / i.interval
    ax = fig.add_subplot()
    line, = ax.plot(t, 0)

    #define the animation function, since it's within this function we can use variables in our upper scope
    def animate(i):
        line.set_ydata(np.array(graph["values"]))  # update the data.
        return line,
    
    ax.set_xlabel("time [s]")
    ax.set_ylabel(graph["unit"])

    canvas = FigureCanvasTkAgg(fig, master=widgetFrame)  # A tk.DrawingArea.
    canvas.draw()

    canvas.get_tk_widget().pack(side=tk.TOP, fill=tk.BOTH, expand=True)

    ani = matplotlib.animation.FuncAnimation(fig, animate, interval=20, blit=True, save_count=50)

    widgetFrame.grid(column=graph["columnParam"],row=graph["rowParam"])