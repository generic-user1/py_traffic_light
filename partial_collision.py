#!/usr/bin/env python3
from __future__ import annotations

from collision import Collision
from typing import TYPE_CHECKING

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
        