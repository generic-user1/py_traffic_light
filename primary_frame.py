#!/usr/bin/env python3

from tkinter import Frame

from traffic_light import TrafficLight

#The primary frame for the application
class PrimaryFrame(Frame):

    #define the names of the traffic lights
    #as well as their ordering when selecting them
    #sequentially
    TLIGHT_NAMES = (
        "north",
        "east",
        "south",
        "west"
        )

    #define the coordinates of each traffic light
    #as 2-tuples (row, column)
    TLIGHT_COORDINATES = {
        "north" : (0, 1),
        "south" : (2, 1),
        "east"  : (1, 2),
        "west"  : (1, 0)
        }


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
        from traffic_light import TrafficLight

        #create and position each light
        for tlightName in PrimaryFrame.TLIGHT_NAMES:
            
            #create the light
            trafficLight = TrafficLight(self)

            #get the traffic light's coordinates 
            rowCoord, colCoord = self.TLIGHT_COORDINATES[tlightName]
            
            #place the traffic light within this frame
            trafficLight.grid(row=rowCoord, column=colCoord)

            #save the light by name in the self.trafficLights dictionary
            #this allows it to be accessed later
            self.trafficLights[tlightName] = trafficLight

            


    def __init__(self, parentWindow):
        from typing import Dict
        from traffic_light import TrafficLight

        #run superclass constructor
        Frame.__init__(self, parentWindow)
        
        #save parent
        self.parentWindow = parentWindow
        
        #setup frame attributes
        self._setFrameAttributes()

        #init traffic lights dictionary (with type hint)
        self.trafficLights : Dict[str, TrafficLight] = {}
        #setup traffic lights
        self._placeTrafficLights()

        #initialize selected light name with the first 
        #this can be used to interact with the lights sequentially
        #using the getSelectedLight and incrementSelectedLight methods
        self.selectedLightName = PrimaryFrame.TLIGHT_NAMES[0]


    #returns the currently selected light name
    def getSelectedLightName(self):
        return self.selectedLightName

    #increments the currently selected light name
    def incrementSelectedLightName(self):
        #get the index of the currently selected light naame
        selectedLightIndex = PrimaryFrame.TLIGHT_NAMES.index(self.selectedLightName)

        #get the index of the next light by adding 1
        nextIndex = selectedLightIndex + 1

        #if the selected light name is not the last one in the list,
        #set the new selected light name to the next name in the list
        if nextIndex < len(PrimaryFrame.TLIGHT_NAMES):
            self.selectedLightName = PrimaryFrame.TLIGHT_NAMES[nextIndex]

        #if the selected light name is the last one in the list,
        #set the new selected light name to the first one in the list
        else:
            self.selectedLightName = PrimaryFrame.TLIGHT_NAMES[0]

    
    #similar to getSelectedLightName but returns the actual
    #TrafficLight instance instead
    def getSelectedLight(self) -> TrafficLight:
        selectedName = self.getSelectedLightName()
        return self.trafficLights[selectedName]

    #alias for incrementSelectedLightName
    #to better match the form of getSelectedLight
    def incrementSelectedLight(self):
        self.incrementSelectedLightName()
            

    

#end PrimaryFrame

if __name__ == "__main__":
    print("This is a class definition used as part of a larger script")
    print("Did you mean to run py_traffic_light.py?")