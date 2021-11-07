#!/usr/bin/env python3
from __future__ import annotations

from typing import Tuple, TYPE_CHECKING
if TYPE_CHECKING:
    from collider import Collider


#Collision
#Class to represent a collision between two objects
#Includes members to store both collided objects 
#as well as the area of intersection

class Collision():

    #given two ranges as 2-tuples (start, stop)
    #returns one range that is the intersection of the two
    #provided ranges, or None if they do not intersect at all
    @staticmethod
    def getRangeOverlap(rangeA: Tuple[int, int], rangeB: Tuple[int, int]) -> Tuple[int, int]:
        
        #first, ensure that each tuple is ordered
        #properly, with the first value being less or equal
        #to the second value
        if rangeA[0] > rangeA[1]:
            #if tuple is ordered incorrectly,
            #swap positions of the values 
            rangeA = (rangeA[1], rangeA[0])

        #same logic as rangeA
        if rangeB[0] > rangeB[1]:
            rangeB = (rangeB[1], rangeB[0])


        #determine whether any overlap exists.
        #This expression can be read as:
        #if A starts before B ends and B starts before A ends
        if rangeA[0] <= rangeB[1] and rangeB[0] <= rangeA[1]:
            #If overlap exists, determine the overlapping range
            #do this by finding the largest start and smallest end
            overlapStart = rangeA[0] if rangeA[0] > rangeB[0] else rangeB[0]
            overlapEnd = rangeA[1] if rangeA[1] < rangeB[1] else rangeB[1]
            return (overlapStart, overlapEnd)

        else:
            #if no overlap was found, return None
            #this would be done implicitly but I choose to
            #explicitly do it here for clarity's sake
            return None


    #Similar to getRangeOverlap, but takes two sets of 
    #(xRange, yRange) and compares them in two dimensions
    #returns a 4-tuple (x, y, width, height) of the overlapping area
    #or None if there is no overlap
    @classmethod
    def getRectangleOverlap(cls, 
        rectA: Tuple[Tuple[int, int], Tuple[int, int]], 
        rectB: Tuple[Tuple[int, int], Tuple[int, int]]
        ) -> Tuple[int, int, int, int]:

        #check for overlap in x dimension
        xOverlap = cls.getRangeOverlap(rectA[0], rectB[0])
        
        #if there is no overlap in the x dimension, return None
        if xOverlap == None:
            return None

        #check for overlap in y dimension
        yOverlap = cls.getRangeOverlap(rectA[1], rectB[1])

        #return None if no overlap found
        if yOverlap == None:
            return None

        #determine the position of the overlap area
        areaX = xOverlap[0]
        areaY = yOverlap[0]

        #determine dimensions of the overlap area
        areaWidth = xOverlap[1] - xOverlap[0]
        areaHeight = yOverlap[1] - yOverlap[0]

        #return the position and dimensions of the overlap area
        return (areaX, areaY, areaWidth, areaHeight)


    #calculates the collision area between collisionSource and collidedWith
    #uses these calculations to set appropriate instance vars
    #to read these calculated values, use the appropriate getter functions defined below
    #a return value of True indicates that a collision area between the two objects exists,
    #whereas a return value of False indicates that no collision was found
    def calculateCollision(self) -> bool:
        
        #get the ranges that both objects cover
        srcRanges = self.collisionSource.getDimensionRanges()
        objRanges = self.collidedWith.getDimensionRanges()

        #calculate the area of overlap between these ranges
        collisionArea = self.getRectangleOverlap(srcRanges, objRanges)

        #if collisionArea is None, then no collision was found
        #in this case set no instance vars and return False
        if collisionArea == None:
            return False

        #if collisionArea is not None, 
        #set instance vars and return True
        else:
            self.collisionX = collisionArea[0]
            self.collisionY = collisionArea[1]
            self.collisionWidth = collisionArea[2]
            self.collisionHeight = collisionArea[3]
            return True

    def updateCollision(self, event = None):
        print(f"updating collision: {self}")
        self.calculateCollision()

    #constructor requires two Collider objects; these are the objects involved
    #with this specific Collision instance
    def __init__(self, collisionSource: Collider, collidedWith: Collider):

        #init collider storage vars
        self.collisionSource: Collider = collisionSource
        self.collidedWith: Collider = collidedWith

        #init collision area vars
        self.collisionX: int = None
        self.collisionY: int = None
        self.collisionWidth: int = None
        self.collisionHeight: int = None

        #attempt to calculate collision area and
        #set the collision area vars
        self.calculateCollision()

        #init vars for funcids (from bindings)
        #these are needed to unbind later
        self._collisionSourceFuncId = None
        self._collidedWithFuncId = None


    #adds <Configure> bindings to both Collider objects
    #that will update the collision area when their size changes
    #if overwrite is set to True (the default), then existing bindings
    #(that were caused by this object) will be overwritten. If overwrite is False,
    #a ValueError is raised when attempting to add bindings if bindings already exist
    def addBindings(self, overwrite = True):
        
        if self._collisionSourceFuncId != None or self._collidedWithFuncId != None:
            if overwrite:
                print(f"Warning: overwriting bindings on {self}")
                self.removeBindings()
            else:
                raise ValueError("Cannot add bindings because bindings already exist!")
                

        self._collisionSourceFuncId = self.collisionSource.bind("<Configure>", self.updateCollision, add=True),
        self._collidedWithFuncId = self.collidedWith.bind("<Configure>", self.updateCollision, add=True)


    #removes the <Configure> bindings set on Collider objects
    #prints a message and returns False if either binding is already unset
    #returns True if both bindings were set
    def removeBindings(self):
        
        bothWereSet = True

        if self._collisionSourceFuncId != None:
            self.collisionSource.unbind("<Configure>", self._collisionSourceFuncId)
            self._collisionSourceFuncId = None
        else:
            print(f"Warning: Couldn't remove binding on <{self}>.collisionSource because it didn't exist")
            bothWereSet = False

        if self._collidedWithFuncId != None:
            self.collidedWith.unbind("<Configure>", self._collidedWithFuncId)
            self._collidedWithFuncId = None
        else:
            print(f"Warning: Couldn't remove binding on <{self}>.collidedWith because it didn't exist")
            bothWereSet = False

        return bothWereSet

    #methods for use with the python "with" expression
    def __enter__(self):
        return self

    def __exit__(self):        
        self.removeBindings()

    #returns True if all collision area vars are set
    #returns False if any collision area vars aren't set
    def hasCollisionArea(self):
        hasArea = (
            self.collisionX      != None and
            self.collisionY      != None and
            self.collisionWidth  != None and
            self.collisionHeight != None
            )
        return hasArea

    #method to set collision area
    #params that are set are updated; those left as None are 
    #left unchanged. To remove a collision area var, use delCollisionArea
    def setCollisionArea(self, x: int = None, y: int = None, width: int = None, height:int = None):
        if x != None:
            self.collisionX = x
        if y != None:
            self.collisionY = y
        if width != None:
            self.collisionWidth = width
        if height != None:
            self.collisionHeight = height

    
    #sets collision area vars to None. Each var specified True is removed,
    #any left as False are unchanged. Set 'all' to true to affect all vars;
    #this will override any other parameters set.
    def delCollisionArea(self, x = False, y = False, width = False, height = False, all = False):
        if all or x:
            self.collisionX = None
        if all or y:
            self.collisionY = None
        if all or width:
            self.collisionWidth = None
        if all or height:
            self.collisionHeight = None


    #methods to return collision variables
    #each of these raises a ValueError if the specified var isn't set
    def getCollisionX(self) -> int:
        if self.collisionX == None:
            raise ValueError(f"Attempted to read <{self}>.collisionX but it wasn't set")
        else:
            return self.collisionX

    def getCollisionY(self) -> int:
        if self.collisionY == None:
            raise ValueError(f"Attempted to read <{self}>.collisionY but it wasn't set")
        else:
            return self.collisionY

    def getCollisionWidth(self) -> int:
        if self.collisionWidth == None:
            raise ValueError(f"Attempted to read <{self}>.collisionWidth but it wasn't set")
        else:
            return self.collisionWidth

    def getCollisionHeight(self) -> int:
        if self.collisionHeight == None:
            raise ValueError(f"Attempted to read <{self}>.collisionHeight but it wasn't set")
        else:
            return self.collisionHeight

    
    #returns a 2-tuple (x, y) of the origin coordinates
    #of this collision. Raises a ValueError if either coordinate
    #is currently unset
    def getCollisionOrigin(self) -> Tuple[int, int]:
        try:
            origin = (
                self.getCollisionX(),
                self.getCollisionY()
            )
        except ValueError:
            #catch ValueError to set new message
            newMsg = f"Attempted to run <{self}>.getCollisionOrigin but not all required vars were set!"
            raise ValueError(newMsg)
        else:
            return origin
    

    #returns a 2-tuple (width, height) of the
    #dimensions of the collision area. 
    #Raises a ValueError if either dimension
    #is currently unset
    def getCollisionDimensions(self) -> Tuple[int, int]:
        try:
            dimensions = (
                self.getCollisionWidth(),
                self.getCollisionHeight()
            )
        except ValueError:
            #catch ValueError to set new message
            newMsg = f"Attempted to run <{self}>.getCollisionDimensions but not all required vars were set!"
            raise ValueError(newMsg)
        else:
            return dimensions


    #returns a 4-tuple (x, y, width, height) including
    #both the origin coordinates and dimensions of the
    #collision area. Raises a ValueError if any of these are unset
    def getCollisionGeometry(self) -> Tuple[int, int, int, int]:
        if self.hasCollisionArea():
            #if all area vars are set, return in a 4-tuple
            geometry = (
                self.getCollisionX(),
                self.getCollisionY(),
                self.getCollisionWidth(),
                self.getCollisionHeight()
            )
            return geometry
        else:
            #if not all area vars are set, raise a ValueError
            newMsg = f"Attempted to run <{self}>.getCollisionGeometry but not all required vars were set!"
            raise ValueError(newMsg)
            

    #returns a 2-tuple of 2-tuples ((x0,y0), (x1, y1))
    #these are the coordinates of the top left and bottom right
    #corners of the collision area; this could be useful
    #for drawing a rectangle that covers the area
    #raises a ValueError if any of the collision area vars are unset
    def getCollisionCorners(self) -> Tuple[Tuple[int, int], Tuple[int, int]]:
        if self.hasCollisionArea():
            #if all area vars are set, calculate corners
            #and return as a tuple of tuples
            x, y, width, height = self.getCollisionGeometry()
            cornerTL = (x, y)
            cornerBR = (x + width, y + height)
            return (cornerTL, cornerBR)
        else:
            #if not all area vars are set, raise a ValueError
            newMsg = f"Attempted to run <{self}>.getCollisionCorners but not all required vars were set!"
            raise ValueError(newMsg)

    def __repr__(self):
        return f'Collision({repr(self.collisionSource)}, {repr(self.collidedWith)})'

    #override __str__ to describe collision
    def __str__(self):
        fStr = repr(self)
        fStr += f'; (x: {self.collisionX}, y:{self.collisionY}, width:{self.collisionWidth}, height: {self.collisionHeight})'
        return fStr
