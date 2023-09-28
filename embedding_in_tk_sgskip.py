import tkinter
import random

from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
# Implement the default Matplotlib key bindings.
from matplotlib.figure import Figure
import matplotlib.animation as animation

import numpy as np

root = tkinter.Tk()
root.wm_title("Embedding in Tk")

fig = Figure(figsize=(5, 4), dpi=100)
t = np.arange(0, 3, .01) #replace max with i.range / i.interval
ax = fig.add_subplot()
line, = ax.plot(t, 2 * np.sin(2 * np.pi * t))

dummyArray = [random.random() for x in range(300)] #replace range value with i.range / i.interval

def animate(i):
    line.set_ydata(np.array(dummyArray))  # update the data.
    return line,

ax.set_xlabel("time [s]")
ax.set_ylabel("f(t)")

canvas = FigureCanvasTkAgg(fig, master=root)  # A tk.DrawingArea.
canvas.draw()

canvas.get_tk_widget().pack(side=tkinter.TOP, fill=tkinter.BOTH, expand=True)

ani = animation.FuncAnimation(fig, animate, interval=20, blit=True, save_count=50)

### Need updateData(dataArray[])

while(True):
    dummyArray = [random.random() for x in range(300)]
    root.update_idletasks()
    root.update()