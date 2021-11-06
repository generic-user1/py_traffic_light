#!/usr/bin/env python3

from position_reporter import PositionReporter
from typing import Tuple

#Collider
#a sub"interface" of PositionReporter that can detect 
#collisions between itself and other Collider instances


class Collider(PositionReporter):

    #returns two ranges as 2-tuples (start, stop)
    #the first range is the x range of the object, the second is the y range
    #these ranges encompass all points along each axis that are
    #within the bounds of the object
    def getDimensionRanges(self):
        cornerTL, cornerBR = self.getCorners()
        xRange = (cornerTL[0], cornerBR[0])
        yRange = (cornerTL[1], cornerBR[1])
        return (xRange, yRange)

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


    #returns a list of tuples (widget, overlapX, overlapY, overlapWidth, overlapHeight)
    #where each tuple is a widget that this collider overlaps along with
    #the position and dimensions of the overlapping area
    #checks against objectsToCheck if provided
    #checks against this object's direct siblings if objectsToCheck is left empty
    def getCollisions(self, objectsToCheck = None):

        #if no object list was provided, use siblings of this object
        if objectsToCheck == None:
            objectsToCheck = self.master.winfo_children()
    

        #if object list is empty, return None
        if len(objectsToCheck) == 0:
            print(f"<{self}>.getCollidingObjects called, but objectsToCheck was empty!")
            return None

        #get the range that this object spans in both x and y dimensions
        thisRange = self.getDimensionRanges()

        #init list of found collisions
        foundCollisions = []

        #iterate through objectsToCheck
        #filter is used to filter out this 
        #object from the list, if present
        for obj in filter(lambda x: x != self, objectsToCheck):

            #if object is not a Collider, then skip collision
            #check and continue to the next object
            if not isinstance(obj, Collider):
                continue
            #note: given that PositionReporter has static methods
            #that should work for any rectangular object, only checking against
            #other Colliders isn't strictly necessary. It is done here for performance;
            #to skip checking collision with objects that we aren't 
            #interested in collisions with (such as the background)

            #get range the object spans
            objRange = obj.getDimensionRanges()

            #get the overlapping range (x, y, length, width)
            #this may be None if the two objects don't overlap
            collision = self.getRectangleOverlap(thisRange, objRange)

            #if objects don't overlap, continue to next object
            if collision == None:
                continue
            else:
                #if objects do overlap, record this collision's details
                foundCollisions.append((obj, *collision))

        #after iterating through all objects, return the
        #set of found collisions
        return foundCollisions


    #similar to getCollisions, but only returns
    #the widgets that this object collides with; 
    #no data on the position or size of the collision is included.
    #objectsToCheck works the same as in getCollisions
    def getCollidingObjects(self, objectsToCheck = None):
        
        #get collisions along with unneeded data
        collisions = self.getCollisions(objectsToCheck)

        #strip unneeded data using map
        #list is used to evaluate the result of map into a list
        #if this wasn't done, the function would return an iterator
        #instead of a list, which could lead to unusual problems
        #Unfortunately, doing this mostly negates the performance benefit of using map
        #but this lost performance is probably worth it in this case
        return list(map(lambda x: x[0], collisions))





            


        