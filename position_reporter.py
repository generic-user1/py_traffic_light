#!/usr/bin/env python3

from typing import Tuple
from tkinter import Widget

#position reporter
#An "interface" for widgets to report their current position
#I say "interface" but the definition is concrete; I simply intend for
#this class to be used in addition to a more useful base class

class PositionReporter():

    #return coordinates within parent
    #as a 2-tuple (x, y)
    #adjusts for parent having a border
    def getPos(self) -> Tuple[int,int]:
        
        #get "base" (unadjusted) coordinates
        baseX = self.winfo_x()
        baseY = self.winfo_y()

        #get parent's border width
        parentBorderWidth = self.master.cget("borderwidth")

        #adjust coordinates and store in a tuple
        coordinates = (
            baseX - parentBorderWidth,
            baseY - parentBorderWidth
        )

        return coordinates

    #return the x and y coordinates of the top left
    #and bottom right corners of the specified widget 
    @staticmethod
    def getCornersOfWidget(targetWidget: Widget) -> Tuple[Tuple[int, int], Tuple[int, int]]:
        
        #get the top left corner
        cornerTL = (
            targetWidget.winfo_x(),
            targetWidget.winfo_y()
        )

        #adjust top left corner by parent's border width
        #as border width seems to offset the return value of winfo_x/y
        parentBorderWidth = targetWidget.master.cget("borderwidth")
        cornerTL = tuple([x - parentBorderWidth for x in cornerTL])
         

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