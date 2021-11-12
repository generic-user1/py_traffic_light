#!/usr/bin/env python3
from __future__ import annotations

from collision import Collision
from typing import TYPE_CHECKING
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
    
    ### NOTES ON ACTIVE AREA DEFINITION ###
    # The active area of each Collider is defined by four bounds in total:
    # - the X dimension start bound
    # - the X dimension end bound
    # - the Y dimension start bound
    # - the Y dimension end bound
    # this allows you to define an inner rectangle. by default,
    # all start bounds are set to 0 and all end bounds to 1, so 
    # the inner rectangle has the full size of the Collider
    #
    # bounds in PartialCollision are defined as the portion 
    # of the total dimension (x or y) that lays behind the boundary
    # for example:
    #  a bound at 0.0 is at the start
    #  a bound at 0.5 is in the middle
    #  a bound at 1.0 is at the end
    # bounds are defined in this way so that if the size of
    # a Collider changes, the bounds stay in the same positions
    # relative to each other and the borders of the widget (though
    # this necessarily changes the actual pixel position of the bound)
    ########################################

    #override constructor
    def __init__(self, collisionSource: Collider, collidedWith: Collider):

        #run superclass constructor
        super().__init__(collisionSource, collidedWith)

        #init the active area bound vars
        #each Collider needs four bounds:
        #one start and one end for each dimension (x and y)
        raise NotImplementedError("PartialCollision is not yet implemented!")
        