#!/usr/bin/env python3

from tkinter import Canvas
from typing import Callable

from position_reporter import PositionReporter

#a widget to represent a vehicle; can "drive"
#across a Frame

class Vehicle(Canvas, PositionReporter):

    DEFAULT_COLOR = "#FF0000"

    DEFAULT_WIDTH = 50
    DEFAULT_HEIGHT = 50

    #The default delay between frames of movement
    #as an integer number of milliseconds
    DEFAULT_MOVEMENT_DELAY = 16

    #The default distance covered per frame
    #as an integer number of pixels
    DEFAULT_MOVEMENT_DISTANCE = 1


    #draws vehicle
    def drawVehicle(self):
        self.create_rectangle(0,0, self.winfo_width(), self.winfo_height())


    #given x and y coordinates (within this 
    #vehicle's parent), updates the vehicle's position
    #visually, the vehicle will appear to snap to the specified coordinates
    def setPos(self, xPos: int, yPos: int):
        self.place(x=xPos, y=yPos)

    
    #move to specified destination in an animated way
    #note that this method DOES NOT BLOCK!!!
    #execution will return from this method 
    #long before the vehicle reaches its destination
    #if you need to do something after the drive completes, set the callback paramater
    #to a callable object (like a function) and that object will be called
    #when the drive completes 
    def driveToPos(self, xPos: int, yPos: int, callback: Callable = None):

        # The way that movement animation works internally
        # is not entirely clear, so I will explain it here.
        # The basic principle is this: instead of jumping directly
        # to the destination, take multiple small steps towards the destination
        # and introduce some time delay between each step.
        # In a perfect world this delay could come from time.sleep,
        # but this would also stop execution of other GUI related code and
        # therefore can't be used in this case; tkinter's after method 
        # must be used instead

        # The after method executes a function after a delay; this means
        # that each movement step must be a discrete function call. For Vehicles,
        # the _animStep method is used. _animStep requires that _destination be set;
        # if it isn't then no movement will be performed - why the destination needs to be 
        # a class variable is left as an excersize to the reader 
        # (hint: discrete function calls means discrete scopes)

        # To actually start animation, this method only needs to set the
        # _destination variable (and _callback if provided) and call the 
        # _animStep method the first time; _animStep will call itself 
        # as many times as it needs to until the destination is reached

        # Before doing this however, the method checks if a drive is already
        # active. If there is an active drive, a ValueError is raised as two
        # drive operations can't take place simultaniously
        if self.isDriving():
            raise ValueError("Cannot start driving when a drive operation is already active")
        else:
            self._destination = (xPos, yPos)
            self._callback = callback
            self._animStep()

    #internal method to make one step of movement towards current destination
    #calls itself after a delay to continue moving, if needed
    #returns immediately if no destination is set, or if destination is already reached
    def _animStep(self):

        

        #check for missing destination        
        if self._destination == None:
            print("anim step missing destination")
            #if destination is missing, return now
            return
        #if destination isn't missing, break it out into x and y
        else:
            destX, destY = self._destination

        #get current position
        currentX, currentY = self.getPos()
        

        #if current position exactly matches destination,
        #clear destination, call the callback method if set,
        #then return without moving the vehicle
        if destX == currentX and destY == currentY:
            if self._callback != None:
                self._callback()
            else:
                print("Drive complete, no callback")
            self.abortDrive()
            return

        #determine new X position based on current position,
        #destination position, and movement distance
        if destX > currentX:
            #the min expression ensures that the destination is never overshot
            newX = currentX + min(destX - currentX, self.movementDistance)
        elif destX < currentX:
            newX = currentX - min(currentX - destX, self.movementDistance)
        else:
            #if destination X exactly equals current X, then newX
            #is set to current X, resulting in no X movement
            newX = currentX

        #determine new Y position using similar logic to X position
        if destY > currentY:
            newY = currentY + min(destY - currentY, self.movementDistance)
        elif destY < currentY:
            newY = currentY - min(currentY  - destY, self.movementDistance)
        else:
            newY = currentY

        #set the new position
        self.setPos(newX, newY)

        #repeat process after delay
        self.after(self.movementDelay, self._animStep)


    #override constructor
    def __init__(self, parent, movementDelay: int = None, movementDistance: int = None):
        #set defaults in superclass constructor
        super().__init__(
            parent,
            width=self.DEFAULT_WIDTH,
            height=self.DEFAULT_HEIGHT,
            bg=self.DEFAULT_COLOR
            )

        #init animation control variables
        self.movementDelay = movementDelay 
        self.movementDistance = movementDistance

        #set defaults if no value was provided for either control var
        if movementDelay == None:
             self.movementDelay = self.DEFAULT_MOVEMENT_DELAY
        if movementDistance == None:
             self.movementDistance = self.DEFAULT_MOVEMENT_DISTANCE

        #init _destination to None
        #this will be set to a 2-tuple (x, y)
        #when animating movement from point to point
        #being set to None indicates no active movement
        self._destination = None

        #init _callback to None
        #this can be set to a callable that will
        #be called when an animated movement (drive) completes
        #being set to None indicates no callback method
        self._callback = None
        

    #returns True if a movement is currently active; False otherwise
    def isDriving(self):
        return self._destination != None

    #stop animated movement, if one is currently active
    def abortDrive(self):
        self._callback = None
        self._destination = None
