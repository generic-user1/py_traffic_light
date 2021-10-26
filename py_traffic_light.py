#!/usr/bin/env python3

import tkinter

#traffic light
#a simulation of a 4 way intersection controlled by traffic lights

#applies grid column and row settings to the specified frame
#allowing the use of placeTrafficLights on the frame
def initTrafficLightGrid(parent: tkinter.Frame):

    #configure columns
    for x in range(3):
        parent.columnconfigure(x, minsize=100, weight=1)

    #configure rows
    for x in range(3):
        parent.rowconfigure(x, minsize=100, weight=1)

    #return parent to indicate success
    return parent


#initializes traffic light widgets with their proper settings
#parentContainer is the containing widget (or window)
#returns all created components in a list
def placeTrafficLights(parent: tkinter.Frame):
    from tkinter import Label
    from typing import List

    #create a column layout within the container
    initTrafficLightGrid(parent)

    trafficLights: List[Label] = []

    north = Label(parent, text="north")
    north.grid(row=0, column=1)
    trafficLights.append(north)

    south = Label(parent, text="south")
    south.grid(row=2, column=1)
    trafficLights.append(south)

    east = Label(parent, text="east")
    east.grid(row=1, column=0)
    trafficLights.append(east)

    west = Label(parent, text="west")
    west.grid(row=1, column=2)
    trafficLights.append(west)

    for trafficLight in trafficLights:
        trafficLight.config(background="#00FFFF")
        trafficLight.grid(sticky="NESW")

    return trafficLights




#open the UI
def main():
    from tkinter import Tk

    #Create main window, set title, and force static size
    mainWindow = Tk()
    mainWindow.title("Traffic Light Simulator")
    mainWindow.resizable(None, None)
    
    #Create main content frame with padding and border
    contentFrame = tkinter.Frame(mainWindow, borderwidth=2, relief="solid")
    contentFrame.pack(padx=25, pady=25)

    #Place traffic light widgets into main content frame
    placeTrafficLights(contentFrame)

    #Run main loop of window (listens for events and blocks until window is closed)
    mainWindow.mainloop()

    


if __name__ == "__main__":
    main()