#!/usr/bin/env python3
from __future__ import annotations

from position_reporter import PositionReporter
from typing import List
from collision import Collision

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


    #returns a list of Collision objects; 
    #one for each object this collider overlaps with
    #if you just want a list of widgets this object 
    #collides with, use getCollidingObjects instead
    #checks against objectsToCheck if provided
    #checks against this object's direct siblings if objectsToCheck is left empty
    def getCollisions(self, objectsToCheck = None) -> List[Collision]:

        #if no object list was provided, use siblings of this object
        if objectsToCheck == None:
            objectsToCheck = self.master.winfo_children()
    

        #if object list is empty, return None
        if len(objectsToCheck) == 0:
            print(f"<{self}>.getCollidingObjects called, but objectsToCheck was empty!")
            return None

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

            #create a Collision object for these two Colliders
            newCollision = Collision(self, obj)

            #if objects don't overlap, continue to next object
            if not newCollision.hasCollisionArea() :
                continue
            else:
                #if objects do overlap, record this collision
                foundCollisions.append(newCollision)

        #after iterating through all objects, return the
        #set of found collisions
        return foundCollisions


    #similar to getCollisions, but only returns
    #the widgets that this object collides with; 
    #no data on the position or size of the collision is included.
    #objectsToCheck works the same as in getCollisions
    def getCollidingObjects(self, objectsToCheck = None) -> List[Collider]:
        
        #get collisions along with unneeded data
        collisions = self.getCollisions(objectsToCheck)

        #strip unneeded data using map
        #list is used to evaluate the result of map into a list
        #if this wasn't done, the function would return an iterator
        #instead of a list, which could lead to unusual problems
        #Unfortunately, doing this mostly negates the performance benefit of using map
        #but this lost performance is probably worth it in this case
        return list(map(lambda x: x.collidedWith, collisions))





            


        