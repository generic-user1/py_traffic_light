#!/usr/bin/env python3

from tkinter import Frame

#The primary frame for the application
class PrimaryFrame(Frame):

    #internal method used to
    #set up attributes for PrimaryFrame
    def _setFrameAttributes(self):
        #pack frame into parent window
        self.pack(padx=25, pady=25)
        
        #set border attributes
        self.configure(borderwidth=2, relief="solid")

        #set background color
        self.configure(background="#FFFFFF")
        
        #setup grid structure
        for x in range(3):
            self.rowconfigure(index=x, weight=1, minsize=100)
            self.columnconfigure(index=x, weight=1, minsize=100)
    
    

    #internal method used to
    #set up the traffic light widgets on the page
    def _placeTrafficLights(self):
        from tkinter import Label
        from traffic_light import TrafficLight

        #create and position each light
        #self.trafficLights["north"] = Label(self, text="north")
        self.trafficLights["north"] = TrafficLight(self)
        self.trafficLights["north"].grid(row=0, column=1)

        #self.trafficLights["south"] = Label(self, text="south")
        self.trafficLights["south"] = TrafficLight(self)
        self.trafficLights["south"].grid(row=2, column=1)

        #self.trafficLights["east"] = Label(self, text="east")
        self.trafficLights["east"] = TrafficLight(self)
        self.trafficLights["east"].grid(row=1, column=0)

        #self.trafficLights["west"] = Label(self, text="west")
        self.trafficLights["west"] = TrafficLight(self)
        self.trafficLights["west"].grid(row=1, column=2)
        
        #set attributes common to each light
        #for trafficLight in self.trafficLights.values():
        #    #set foreground and background colors
        #    trafficLight.configure(background="#00FFFF", foreground="#000000")
        #    #enable sticky on all four corners; effectively a fill
        #    trafficLight.grid(sticky="NESW")


    def __init__(self, parentWindow):
        from tkinter import Label
        from typing import Dict

        #run superclass constructor
        Frame.__init__(self, parentWindow)
        
        #save parent
        self.parentWindow = parentWindow
        
        #setup frame attributes
        self._setFrameAttributes()

        #init traffic lights dictionary (with type hint)
        self.trafficLights : Dict[str, Label] = {}
        #setup traffic lights
        self._placeTrafficLights()


if __name__ == "__main__":
    print("testing PrimaryFrame")
    from tkinter import Tk
    testWindow = Tk()
    testFrame = PrimaryFrame(testWindow)
    testWindow.mainloop()