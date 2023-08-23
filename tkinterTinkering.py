import tkinter as tk
import json
import random

root = tk.Tk()
isWindowOpen = True

def onClose():
    global isWindowOpen
    isWindowOpen = False


def main():
    #Setup exit protocol for loop
    root.protocol("WM_DELETE_WINDOW",onClose)

    frame = tk.Frame(root)
    frame.grid()

    tk.StringVar(frame, "LABELTEXT")

    testLabel = tk.Label(frame,textvariable="LABELTEXT").grid(column= 0, row= 0)

    #Custom tk.mainloop()
    while (isWindowOpen):
        root.update_idletasks()
        root.update()
        frame.setvar(name="LABELTEXT",value = str(random.choice(range(10))))


    root.destroy()

    #UI needs: textbox for sensor name, textbox for sensor data, start log button, stop log button, exit handling


if (__name__ == "__main__"):
    main()