
from road import Road

#A road intersection widget - similar to a Road,
#but has intersection lines at its edges rather than
#lane lines in its center

class RoadIntersection(Road):

    #override line color to better suit
    #intersection border lines
    LINE_COLOR = "#FFFFFF"

    #override constructor to remove the horizontal option
    def __init__(self, parent):
        super().__init__(parent)

    #override drawRoad method to draw an intersection
    #rather than a normal road segment
    def drawRoad(self, doNotClear=False):
        
        if not doNotClear:
            self._clearCanvas()

        #alias width and height
        currentWidth = self.currentWidth
        currentHeight = self.currentHeight

        #determine the size of one line
        #the height is the closest integer approximation of
        #1/32nd the height of the canvas
        lineHeight = int(round(currentHeight/32))
        #the width is the closest integer approximation of
        #1 half of the width of the canvas 
        lineWidth = int(round(currentWidth/2))
        
        #calculate offsets for the bottom line
        #the top line doesn't need any offsets
        lineXOffset = currentWidth - lineWidth
        lineYOffset = currentHeight - lineHeight


        self.create_rectangle(
            0, 
            0, 
            lineWidth, 
            lineHeight, 
            fill=self.LINE_COLOR,
            outline=self.LINE_COLOR
            )

        self.create_rectangle(
            lineXOffset, 
            lineYOffset, 
            currentWidth, 
            currentHeight, 
            fill=self.LINE_COLOR,
            outline=self.LINE_COLOR
            )
        

#end RoadIntersection