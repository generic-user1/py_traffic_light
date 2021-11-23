#!/usr/bin/env python3
from __future__ import annotations
from typing import Tuple

from collider import Collider
from collision import Collision
from partial_collision import PartialCollision
from proportional_bb import ProportionalBB

#PartialCollider
#a sub"interface" of Collider that has
#only a portion of its total area active for collision checks
class PartialCollider(Collider):

    #define the default active area bounds
    DEFAULT_ACTIVE_START = 0.0
    DEFAULT_ACTIVE_END = 1.0

    #override constructor while 
    #remaining a mixin class
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        #init instance var for storing the active area 
        #for this PartialCollider; by default this is the full area
        self.activeArea: ProportionalBB = ProportionalBB(
            self.DEFAULT_ACTIVE_START,     
            self.DEFAULT_ACTIVE_END,
            self.DEFAULT_ACTIVE_START,
            self.DEFAULT_ACTIVE_END)


    #override getCollisionWith to return PartialCollisions where applicable
    #returns a regular Collision if otherObj isn't a PartialCollider
    def getCollisionWith(self, otherObj: Collider) -> Collision:
        if isinstance(otherObj, PartialCollider):
            return PartialCollision(self, otherObj)
        else:
            return super().getCollisionWith(otherObj)
    
    
    #return the active area of collision as literal coordinates
    #(not proportional bounds) in the same format as getDimensionRanges:
    #a 2-tuple of 2-tuples ((x0, x1), (y0, y1))
    def getActiveAreaRanges(self) -> Tuple[Tuple[int, int], Tuple[int, int]]:
        #calculate the full ranges
        xRange, yRange = super().getDimensionRanges()

        #use the activeArea ProportionalBB to calculate the
        #active area of collision and return the result
        return self.activeArea.calculateDimensionRanges(*xRange, *yRange)

    
    #return a copy of the ProportionalBB that defines the ActiveArea
    def getActiveArea(self) -> ProportionalBB:
        return self.activeArea.getCopy()

    
    #set a new activeArea after checking to ensure it is a ProportionalBB
    def setActiveArea(self, newActiveArea: ProportionalBB):
        if not isinstance(newActiveArea, ProportionalBB):
            errMsg = f"new active area \"{newActiveArea}\" is not a ProportionalBB"
            raise TypeError(errMsg)
        else:
            self.activeArea = newActiveArea        


if __name__ == "__main__":
    print("This is a class definition used as part of a larger script")
    print("Did you mean to run py_traffic_light.py?")
  