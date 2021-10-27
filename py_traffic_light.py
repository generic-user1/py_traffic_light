#!/usr/bin/env python3

import tkinter

#traffic light
#a simulation of a 4 way intersection controlled by traffic lights

#open the UI
def main():
    from tkinter import Tk
    from primary_frame import PrimaryFrame

    #Create main window, set title, and force static size
    mainWindow = Tk()
    mainWindow.title("Traffic Light Simulator")
    mainWindow.resizable(False, False)
    
    #Create main content frame with padding and border
    contentFrame = PrimaryFrame(mainWindow)

    #Run main loop of window (listens for events and blocks until window is closed)
    mainWindow.mainloop()

    


if __name__ == "__main__":
    main()