#!/usr/bin/env python3

import tkinter


#traffic light
#a simulation of a 4 way intersection controlled by traffic lights

#open the UI
def main():
    from tkinter import Tk
    from primary_frame import PrimaryFrame

    #Create main window and set title
    mainWindow = Tk()
    mainWindow.title("Traffic Light Simulator")

    #Create main content frame
    contentFrame = PrimaryFrame(mainWindow)

    def testFunc():

        light = contentFrame.getSelectedLight()
        light.incrementState()
        contentFrame.incrementSelectedLight()

        roadTL, roadBR = contentFrame.vertRoad.getCorners()
        vSize = contentFrame.vehicle.winfo_width()

        contentFrame.vehicle.place(x=roadTL[0], y=roadTL[1])
        def driveToBottom():
            x, y = [pos - vSize for pos in roadBR]
            def cbTest(event=None):
                print("<<DriveComplete>> event!")
            contentFrame.vehicle.bind("<<DriveComplete>>", cbTest)
            contentFrame.vehicle.driveToPos(x, y)
        contentFrame.after(10, driveToBottom)
        
    
    changeButton = tkinter.Button(contentFrame, command=testFunc)
    changeButton.grid(row=2, column=2)

    #Run main loop of window (listens for events and blocks until window is closed)
    mainWindow.mainloop()

    


if __name__ == "__main__":
    main()