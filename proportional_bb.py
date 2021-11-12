#!/usr/bin/env python3
from __future__ import annotations

from dataclasses import dataclass

#ProportionalBB (Short for Proportional Bounding Box)
#A data class used to store a bounding box that is defined
#as proportions of some rectangle.
#Each dimension is defined by a start and end bound,
#with each of those being a floating point number from 0.0 to 1.0
@dataclass
class ProportionalBB:

    xStart: float
    xEnd: float
    yStart: float
    yEnd: float

    silent: bool = False

    #ensure that all bounds are floats (attempt conversion if not),
    #ensure that all bounds are within the range 0 to 1 inclusive,
    #and ensure that start bounds are less than end bounds (swap positions if not)
    #Raises TypeError if bounds are not floats and conversion isn't possible
    #Raises ValueError if bounds are outside the 0 to 1 range, or if bounds are equal
    def validate(self):

        try:
            #check type of bounds
            if not isinstance(self.xStart, float):
                #attempt conversion if not a float
                #after printing a warning message
                if not self.silent:
                    print(f"Warning: casting xStart ({self.xStart}) to float")
                self.xStart = float(self.xStart)

            if not isinstance(self.xEnd, float):
                if not self.silent:
                    print(f"Warning: casting xEnd ({self.xEnd}) to float")
                self.xEnd = float(self.xEnd)

            if not isinstance(self.yStart, float):
                if not self.silent:
                    print(f"Warning: casting yStart ({self.yStart}) to float")
                self.yStart = float(self.yStart)
            
            if not isinstance(self.yEnd, float):
                if not self.silent:
                    print(f"Warning: casting yEnd ({self.yEnd}) to float")
                self.yEnd = float(self.yEnd)
        
        except (ValueError, TypeError):
            #A ValueError may be thrown if a string is passed
            #that can't be converted to a float
            #A TypeError may be thrown if another type of object is passed
            #In both cases, raise a TypeError with a custom message
            errMsg = f"ProportionalBB: Failed to cast all bounds to float ({self.xStart}, {self.xEnd}, {self.yStart}, {self.yEnd})"
            raise TypeError(errMsg)

        #init erroringBoundName to None
        erroringBoundName = None

        #ensure each bound is not outside the 0 to 1 range
        if self.xStart < 0 or self.xStart > 1:
            erroringBoundName = "xStart" #save name of erroring bound
        elif self.xEnd < 0 or self.xEnd > 1:
            erroringBoundName = "xEnd"
        elif self.yStart < 0 or self.yEnd > 1:
            erroringBoundName = "yStart"
        elif self.yEnd < 0 or self.yEnd > 1:
            erroringBoundName = "yEnd"
        
        #if an erroring bound was detected, raise a ValueError
        if erroringBoundName != None:
            errMsg =  f"ProportionalBB: {erroringBoundName} bound is out of range ({self.xStart}, {self.xEnd}, {self.yStart}, {self.yEnd})"
            raise ValueError(errMsg)

        #init erroingDimensionName to None
        erroringDimensionName = None

        #ensure start bounds come before end bounds
        #if they are out of order, swap them
        #if they are exactly equal, raise a ValueError
        if self.xStart > self.xEnd:
            if not self.silent:
                print("Warning: swapping x bounds")
            temp = self.xStart
            self.xStart = self.xEnd
            self.xEnd = temp
            del temp
        elif self.xStart == self.xEnd:
            erroringDimensionName = "x"
        
        elif self.yStart > self.yEnd:
            if not self.silent:
                print("Warning: swapping y bounds")
            temp = self.yStart
            self.yStart = self.yEnd
            self.yEnd = temp
            del temp

        elif self.yStart == self.yEnd:
            erroringDimensionName = "y"

        #if an erroring dimension was detected, raise a ValueError
        if erroringDimensionName != None:
            errMsg =  f"ProportionalBB: {erroringDimensionName} dimension has zero size ({self.xStart}, {self.xEnd}, {self.yStart}, {self.yEnd})"
            raise ValueError(errMsg)


    #override __post_init__ (runs after auto-generated init method)
    #to run the validation method
    def __post_init__(self):
        self.validate()