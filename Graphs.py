import numpy as np
import tkinter as tk
import multiprocessing
import matplotlib.figure
import matplotlib.animation
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

ani = []

def updateGraph(graph: dict, voltageData: multiprocessing.Array) -> None:
    trash = graph["values"].pop()
    graph["values"].appendleft(voltageData[graph["index"]] * graph["scalingFactor"] + graph["offset"])
    #print(graph["values"])

def loadGraph(parentFrame: tk.Frame, graph: dict, styleDict: dict) -> None:
    #setting up the tk frame
    widgetFrame = tk.Frame(parentFrame)
    widgetFrame.grid(sticky=(tk.N,tk.S,tk.E,tk.W))
    widgetFrame.config(padx=styleDict["padding"],pady=styleDict["padding"])
    tk.Label(widgetFrame, text = graph["label"], font = (styleDict["labelFont"],styleDict["labelSize"],"normal"), fg=styleDict["labelColor"]).grid(column=0,row=0,columnspan=2)

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

    widgetFrame.grid(column=graph["column"],row=graph["row"])