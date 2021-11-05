#!/usr/bin/env python3

from position_reporter import PositionReporter

#Collider
#a sub"interface" of PositionReporter that can detect 
#collisions between itself and other Collider instances


class Collider(PositionReporter):

    #test method; will be removed
    def testCollide(self):
        print("collision: ", self)