
from road import Road

#A road intersection widget - similar to a Road,
#but has intersection lines at its edges rather than
#lane lines in its center

class RoadIntersection(Road):

    #override line color to better suit
    #intersection border lines
    LINE_COLOR = "#FFFFFF"

    #override drawRoad method to draw an intersection
    #rather than a normal road segment
    def drawRoad(self, doNotClear=False):
        
        if not doNotClear:
            self._clearCanvas()

        #TODO: add crosswalk lines

#end RoadIntersection