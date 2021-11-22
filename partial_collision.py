#!/usr/bin/env python3
from __future__ import annotations

from collision import Collision
from typing import TYPE_CHECKING, Tuple

from proportional_bb import ProportionalBB
if TYPE_CHECKING:
    from collider import Collider


#PartialCollision
#A subclass of Collision that supports setting
#an 'active' area for collision checks
#PartialCollisions will only check for overlapping area
#within the active area of both Colliders
#The active area of each Collider is defined using 
#proportions of its dimensions; see below for details
class PartialCollision(Collision):

    #define the default active area bounds
    DEFAULT_ACTIVE_START = 0.0
    DEFAULT_ACTIVE_END = 1.0
    

    #override constructor
    def __init__(self, collisionSource: Collider, collidedWith: Collider):

        #run superclass constructor
        super().__init__(collisionSource, collidedWith)

        #init the active area bound vars
        #each Collider needs a ProportionalBB
        #to store the bounding box of its active area
        self.collisionSourceActiveArea = ProportionalBB(
            self.DEFAULT_ACTIVE_START,
            self.DEFAULT_ACTIVE_END,
            self.DEFAULT_ACTIVE_START,
            self.DEFAULT_ACTIVE_END
            )

        self.collidedWithActiveArea = ProportionalBB(
            self.DEFAULT_ACTIVE_START,
            self.DEFAULT_ACTIVE_END,
            self.DEFAULT_ACTIVE_START,
            self.DEFAULT_ACTIVE_END
            )

    #override collision area calculation
    #to only include active areas for each Collider
    def getCollisionArea(self) -> Tuple[int, int, int, int]:
        #get the ranges that both objects cover
        srcRanges = self.collisionSource.getDimensionRanges()
        objRanges = self.collidedWith.getDimensionRanges()

        #use the ProportionalBB of each Collider to get the
        #active area for collision
        srcActiveRanges = self.collisionSourceActiveArea.calculateDimensionRanges(*srcRanges[0], *srcRanges[1])
        objActiveRanges = self.collidedWithActiveArea.calculateDimensionRanges(*objRanges[0], *objRanges[1])

        #calculate the area of overlap between these ranges
        collisionArea = self.getRectangleOverlap(srcActiveRanges, objActiveRanges)

        #return the result of the collision
        #this will be None if no collision was found
        return collisionArea
        
if __name__ == "__main__":
    print("This is a class definition used as part of a larger script")
    print("Did you mean to run py_traffic_light.py?")