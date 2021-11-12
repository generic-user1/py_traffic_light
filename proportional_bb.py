#!/usr/bin/env python3
from __future__ import annotations

from typing import ClassVar, Tuple, Dict, Any
from dataclasses import dataclass

#ProportionalBB (Short for Proportional Bounding Box)
#A data class used to store a bounding box that is defined
#as proportions of some rectangle.
#Each dimension is defined by a start and end bound,
#with each of those being a floating point number from 0.0 to 1.0
#note: a dataclass is not a great fit for this purpose
#if this were production code, I would write a class from scratch instead
#this design was chosen mostly because I wanted to experiement
@dataclass
class ProportionalBB:
    
    #dictionary that associates the x and y axes
    #with a tuple of bound names (start, end)
    AXIS_BOUNDS : ClassVar[Dict[str, Tuple[str, str]]] = {
        "x": ("xStart", "xEnd"),
        "y": ("yStart", "yEnd")
        }

    #define the instance vars for bounds
    xStart: float
    xEnd: float
    yStart: float
    yEnd: float

    #define the 'silent' instance var with
    #a default value of False
    silent: bool = False

    ### NOTES ON PROPORTIONAL AREA DEFINITION ###
    # A proportional area is defined by four bounds in total:
    # - the X dimension start bound
    # - the X dimension end bound
    # - the Y dimension start bound
    # - the Y dimension end bound
    # this allows you to define a rectangle
    # relative to some other rectangle
    #
    # bounds are defined as the portion 
    # of the total dimension (x or y) that lays behind the boundary
    # for example:
    #  a bound at 0.0 is at the start
    #  a bound at 0.5 is in the middle
    #  a bound at 1.0 is at the end
    # bounds are defined in this way so that if the size of
    # a rectangle changes, the  bounds stay in the same positions
    # relative to each other and the borders of the widget (though
    # this necessarily changes the actual pixel position of the bound)
    ########################################

    #internal method
    #ensure that bound is within the range 0 to 1 inclusive
    #return the value as a float
    #raise a ValueError if bound is outside the range 0 to 1 inclusive
    #raise a TypeError if bound isn't and can't be converted to a float
    @staticmethod
    def _validateBoundValue(bound: float, silent: bool = False):
        try:
            #check type of bound
            if not isinstance(bound, float):
                #attempt conversion if not a float
                #after printing a warning message
                if not silent:
                    print(f"Warning: casting {bound} to float")
                bound = float(bound)
        except (TypeError, ValueError):
            #A ValueError may be thrown if a string is passed
            #that can't be converted to a float
            #A TypeError may be thrown if another type of object is passed
            #In both cases, raise a TypeError with a custom message
            errMsg = f"Bound value is not a float and could not be converted ({repr(bound)})"
            raise TypeError(errMsg)

        #ensure bound is not outside the 0 to 1 range
        if bound < 0 or bound > 1:
            #if an erroring bound was detected, raise a ValueError
            errMsg =  f"Bound is out of range ({repr(bound)})"
            raise ValueError(errMsg)

        return bound

    #returns a list of all configured bound names
    #as provided by AXIS_BOUNDS
    def getBoundNames(self):
        boundNames = []
        boundNameSets = self.AXIS_BOUNDS.values()
        for nameSet in boundNameSets:
            boundNames += nameSet
        return boundNames

    #override __setattr__ (called when any attribute is set)
    #to run the bound validation method on the prospective
    #new bound before actually setting it
    #see definition of validateBound for details on raised exceptions
    def __setattr__(self, name: str, value: Any) -> None:
        
        #if the attribute is not a bound, use the normal
        #__setattr__ method instead of this custom one
        if name not in self.getBoundNames():
            print("name not found:", name)
            print("current names:", self.__dict__.keys())
            return super().__setattr__(name, value)
        
        else:
            #ensure the value is of valid type and not outside the 0 to 1 range
            value = self._validateBoundValue(value, silent = self.silent)

            #determine whether this is the start or end bound
            #and which axis it is on
            isStart = None
            selectedAxis = None
            for axisName, boundNames in self.AXIS_BOUNDS.items():
                
                #check the selected name against both bound names
                #if it matches, set isStart appropriately
                if name == boundNames[0]:
                    isStart = True
                elif name == boundNames[1]:
                    isStart = False

                #if the name was matched, capture 
                #the axis name and stop iterating
                if isStart != None:
                    selectedAxis = axisName
                    break

            
            try:
                #get the value of the opposite bound
                if isStart:
                    oppositeValue = getattr(self, self.AXIS_BOUNDS[selectedAxis][1])
                else:
                    oppositeValue = getattr(self, self.AXIS_BOUNDS[selectedAxis][0])

            except AttributeError:
                #AttributeError may be raised if 
                #the opposite value does not yet exist
                #in this case, accept the value immedately
                return super().__setattr__(name, value)

            #if the opposite bound is set, 
            #check the new value against it
            if isStart:
                #if the bound is the start,
                #raise a ValueError if the 
                #new value is not less than
                #the end bound value
                if value >= oppositeValue:
                    return super().__setattr__(name, value)
                else:
                    errMsg = f"New value for top bound ({value}) must be less than bottom bound ({oppositeValue})"
                    raise ValueError(errMsg)
            
            else:
                #if the bound is the end,
                #raise a ValueError if the 
                #end bound value is not 
                #less than the new value
                if oppositeValue <= value:
                    return super().__setattr__(name, value)
                else:
                    errMsg = f"New value for bottom bound ({value}) must be greater than than top bound ({oppositeValue})"
                    raise ValueError(errMsg)

    #end __setattr__        


if __name__ == "__main__":
    n = ProportionalBB(0.0, 1.0, 0.0, 1.0)
    print(n)
#    n.xEnd = 0.5
#    print(n)
  