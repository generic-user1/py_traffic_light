#!/usr/bin/env python3

from position_reporter import PositionReporter

#Collider
#a sub"interface" of PositionReporter that can detect 
#collisions between itself and other Collider instances


class Collider(PositionReporter):

    #returns a list of widgets that collide with this one
    #checks against objectsToCheck if provided
    #checks against this objects direct siblings if objectsToCheck is left empty
    def getCollidingObjects(self, objectsToCheck = None):

        #if no object list was provided, use siblings of this object
        if objectsToCheck == None:
            objectsToCheck = self.master.winfo_children()
    

        #if object list is empty, return None
        if len(objectsToCheck) == 0:
            print(f"<{self}>.getCollidingObjects called, but objectsToCheck was empty!")
            return None

        #iterate through objectsToCheck
        #filter is used to filter out this 
        #object from the list, if present
        raise NotImplementedError("getCollidingObjects is not yet implemented!")
        