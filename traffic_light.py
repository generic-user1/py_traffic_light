#!/usr/bin/env python3

from tkinter import Canvas

#a class for a traffic light widget

class TrafficLight(Canvas):

    LAMP_SIZE = 25

    def __init__(self, parent):
        #alias constant lamp size
        lampSize = TrafficLight.LAMP_SIZE

        #run superclass constructor with defined width, height, and bg color
        Canvas.__init__(self, 
            parent, 
            width=lampSize+3, 
            height=(lampSize+3)*3, 
            background="#FFFFFF"
            )
        
        #store parent
        self.parent = parent

        #create a dict to store lamp ids
        self.lampIds = {
            "red": None,
            "yellow": None,
            "green": None
        }
        
        #create and position lamps
        #store each lamp's id in the self.lampIds dict
        previousY1 = 1
        for lampName in self.lampIds.keys():
            x0 = 2
            y0 = previousY1 + 2
            x1 = x0 + lampSize
            y1 = y0 + lampSize
            self.lampIds[lampName] = self.create_oval(x0, y0, x1, y1, fill="#000000")
            previousY1 = y1



if __name__ == "__main__":
    print("testing TrafficLight")
    from tkinter import Tk

    testWindow = Tk()
    testLight = TrafficLight(testWindow)
    testLight.pack(padx=25, pady=25)
    testWindow.mainloop()
