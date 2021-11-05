#!/usr/bin/env python3

from typing import Tuple
from tkinter import Widget
from tkinter import Misc as BaseWidget 
#I import tkinter.Misc as BaseWidget to be more representative of what it is;
#This is a personal preference and is by no means required

#Position Reporter
#An "interface" for widgets to report their current position
#I say "interface" but the definition is concrete; I simply intend for
#this class to be used in addition to a more useful base class

class PositionReporter(BaseWidget):

    #return coordinates within parent
    #as a 2-tuple (x, y)
    #adjusts for parent having a border
    #by default, if targetWidget is a PositionReporter instance,
    #then the targetWidget's getPos method will be used
    #setting forceStatic to True will disable this behavior
    #if targetWidget is not a PositionReporter, forceStatic has no effect
    @staticmethod
    def getPosOfWidget(targetWidget: Widget, forceStatic = False) -> Tuple[int, int]:

        #if forceStatic is false and the target is a PositionReporter,
        # use the target's getPos method
        if not forceStatic and isinstance(targetWidget, PositionReporter):
            return targetWidget.getPos()

        #get "base" (unadjusted) coordinates
        baseX = targetWidget.winfo_x()
        baseY = targetWidget.winfo_y()

        #get parent's border width
        parentBorderWidth = targetWidget.master.cget("borderwidth")

        #adjust coordinates and store in a tuple
        coordinates = (
            baseX - parentBorderWidth,
            baseY - parentBorderWidth
        )

        return coordinates
        
    
    #return the (x, y) coordinates of this widget
    #you can override this method to define custom 
    #corner-locating behavior on a class by class basis
    #(e.g. offsetting coordinates by a constant, rotating 
    #coordinates about an axis, translating to and 
    #from different coordinate spaces, etc)
    def getPos(self) -> Tuple[int,int]:

        #by default, getPos simply uses getPosOfWidget with forceStatic set to True 
        #(if forceStatic were False, getPosOfWidget would call getPos again and we
        # would be stuck in an infinite loop)
        return self.getPosOfWidget(self, forceStatic=True)
        

    #return the x and y coordinates of the top left
    #and bottom right corners of the specified widget 
    @staticmethod
    def getCornersOfWidget(targetWidget: Widget) -> Tuple[Tuple[int, int], Tuple[int, int]]:
        
        #get the top left corner
        cornerTL = PositionReporter.getPosOfWidget(targetWidget)

        #get the width and height of the widget
        widgetWidth = targetWidget.winfo_width()
        widgetHeight = targetWidget.winfo_height()
        
        #calculate the bottom right corner given the
        #widget's height and width
        cornerBR = (
            cornerTL[0] + widgetWidth,
            cornerTL[1] + widgetHeight
        )

        return (cornerTL, cornerBR)

    #return the x and y coordinates of the top left
    #and bottom right corners of this widget
    def getCorners(self) -> Tuple[Tuple[int, int], Tuple[int, int]]:
        return self.getCornersOfWidget(self)