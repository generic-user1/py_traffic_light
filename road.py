#!/usr/bin/env python3

from tkinter import Canvas, Event

from collider import Collider
from collision import Collision
from typing import List

#A road widget drawn using the tkinter Canvas system
#Scales dynamically,
class Road(Canvas, Collider): 

    #define colors for elements of the road
    ROAD_COLOR = "#373B42"
    LINE_COLOR = "#FFFF00"

    #internal method
    #clears every object off the Canvas
    #this could apply to any Canvas subclass
    def _clearCanvas(self):
        allObjects = self.find_all()
        for object in allObjects:
            self.delete(object)


    #draws the traffic lines down the middle of the widget
    #normally clears the canvas before doing this,
    #set doNotClear to True to disable this functionality
    def drawRoad(self, doNotClear = False):
        from math import ceil

        #clear canvas if not specified otherwise
        if not doNotClear:
            self._clearCanvas()

        #alias width and height
        if not self.horizontal:
            currentWidth = self.currentWidth
            currentHeight = self.currentHeight
        else:
            #if this road is to be drawn horizontally,
            #swap width and height; this effectively swaps
            #the axis that calculations are based on
            currentHeight = self.currentWidth
            currentWidth = self.currentHeight

        #determine the size of one line segment
        #the width is the closest integer approximation of
        #1/32nd the width of the canvas
        lineWidth = int(round(currentWidth/32))
        #the height of one line segment is 4 times its width
        lineHeight = lineWidth*4

        if lineWidth == 0:
            #print("Cannot draw zero width line!")
            return False

        #in order for the lines to be centered, they must
        #be offset to the right by a certain amount, shown here
        #integer approximation is used
        xOffset = int(round((currentWidth/2) - (lineWidth/2)))

        #determine the number of lines to draw
        #the line height is doubled to account for the space
        #between lines (the height of which is equal to the line height)
        #the result is rounded up to the nearest integer
        linesToDraw = ceil(currentHeight/(lineHeight*2))

        #calculate the inital space between the
        #top of the canvas and the top of the first line
        #line height is used twice here, the second usage is for the
        #space between lines
        initialYOffset = int(
            (currentHeight - (lineHeight * linesToDraw) - (lineHeight * (linesToDraw - 1))) / 2
            )
        #note: if the lines exceed the height of the canvas, this expression
        #will result in a negative value. this is fine, as this simply offsets
        #in the opposite direction (which still centers the lines)

        #draw each line
        for lineIndex in range(linesToDraw):

            #determine yOffset
            #this is the height of each previous line
            #(multiplied by two to account for space between them)
            #plus the initial offset amount
            yOffset = (lineIndex * (lineHeight*2)) + initialYOffset
            #Sidenote: Parens aren't needed here,
            #but they improve clarity

            #draw the line using the calculated offset
            if not self.horizontal:
                self.create_rectangle(xOffset, yOffset, xOffset+lineWidth, yOffset+lineHeight, fill=self.LINE_COLOR)
            else:
            #draw lines horizontally if needed
            #this is done by switching around which parameter goes where
                self.create_rectangle(yOffset, xOffset, yOffset+lineHeight, xOffset+lineWidth, fill=self.LINE_COLOR)

        #draw a blank rectangle over lines that intersect another road
        collisions = self.getCollisions()
        thisX, thisY = self.getPos()
        for collision in collisions:

            #if colliding object is not a Road,
            #ignore the collision
            if not isinstance(collision.collidedWith, Road):
                continue
            else:
                #if colliding object is a road,
                #get the corners of the collision
                collisionTL, collisionBR = collision.getCollisionCorners()

                #offset collision corners by the coordinates of this Road
                #this allows us to draw a rectangle over the collision area
                boxX0 = collisionTL[0] - thisX
                boxX1 = collisionBR[0] - thisX
                boxY0 = collisionTL[1] - thisY
                boxY1 = collisionBR[1] - thisY

                #draw a rectangle at these coordinates
                #with the given dimensions
                print("collision: ", collision)
                #print("box x y:",boxX0, boxY0)
                #print("box end:", boxX1, boxY1)
                #print("box dimensions:", colWidth, colHeight)
                self.create_rectangle(boxX0, boxY0, boxX1, boxY1, fill=self.ROAD_COLOR)



        return True

    #internal method
    #updates the internal size values
    def _updateSize(self, width = None, height = None):
        self.currentWidth = width if width != None else self.winfo_width()
        self.currentHeight = height if height != None else self.winfo_height()
        self.drawRoad()

    #internal method
    #event handler for <Configure> event which fires when resizing
    def _onResize(self, event):
        print(self, "resize")
        if event.width != self.currentWidth or event.height != self.currentHeight:
            self._updateSize(event.width, event.height)


    def __init__(self, parent, horizontal=False):
        from tkinter.constants import FLAT

        #run superclass constructor
        super().__init__(
            parent, #set parent object
            width=100, #set default width and height
            height=100, 
            bg=self.ROAD_COLOR, #set background color
            highlightthickness=0 #remove border that is applied by default to canvas widgets
            )

        #save rotation setting
        self.horizontal = horizontal

        #get dimensions
        #these will be updated dynamically at runtime
        #using the <Configure> event and onResize method
        self.currentWidth = self.winfo_width()
        self.currentHeight = self.winfo_height()
        
        #bind the _onResize method to the <Configure> event
        self.bind("<Configure>", self._onResize)

        def onClick(event: Event):
            print(self,"clicked:", event.x, event.y, "root:", event.x_root, event.y_root)
        self.bind("<Button-1>", onClick)

    #get a list of Collisions for each
    #Road that this Road intersects; these can be used
    #to draw intersections
    def getRoadCollisions(self) -> List[Collision]:

        #define a filter function that will return only 
        #Road objects that are not this one
        roadFilterFunc = lambda x: x != self and isinstance(x, Road)

        #apply that filter function to the list of this Road's parent's children
        #notably this list includes the current Road which is why we include
        #a check for it in the filter function
        siblingRoads = filter(roadFilterFunc, self.master.winfo_children())

        #test collision on these sibling roads and return the results
        roadCollisions = self.getCollisions(siblingRoads)

        return roadCollisions   


#end Road




if __name__ == "__main__":
    print("This is a class definition used as part of a larger script")
    print("Did you mean to run py_traffic_light.py?")
