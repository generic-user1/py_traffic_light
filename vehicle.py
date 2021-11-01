#!/usr/bin/env python3

from tkinter import Canvas

#a widget to represent a vehicle; can "drive"
#across a Frame

class Vehicle(Canvas):

    DEFAULT_COLOR = "#FF0000"

    DEFAULT_WIDTH = 50
    DEFAULT_HEIGHT = 50

    #draws vehicle
    def drawVehicle(self):
        self.create_rectangle(0,0, self.winfo_width(), self.winfo_height())


    #override constructor to track parent
    def __init__(self, parent):
        super().__init__(
            parent,
            width=self.DEFAULT_WIDTH,
            height=self.DEFAULT_HEIGHT,
            bg=self.DEFAULT_COLOR
            )
