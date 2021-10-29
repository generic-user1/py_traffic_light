
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

        #alias width and height
        if not self.horizontal:
            currentWidth = self.currentWidth
            currentHeight = self.currentHeight
        #swap axes if drawing horizontally
        else:
            currentWidth = self.currentHeight
            currentHeight = self.currentWidth

        #determine the size of one line
        #the height is the closest integer approximation of
        #1/32nd the height of the canvas
        lineHeight = int(round(currentHeight/32))
        #the width is the closest integer approximation of
        #1 half of the width of the canvas 
        lineWidth = int(round(currentWidth/2))
        
        #calculate offsets for the bottom line
        #the top line doesn't need any offsets
        lineXOffset = (currentWidth - 1) - lineWidth
        lineYOffset = (currentHeight - 1) - lineHeight

        #draw lines
        if not self.horizontal:
            self.create_rectangle(
                0, 
                0, 
                lineWidth, 
                lineHeight, 
                fill=self.LINE_COLOR
                )

            self.create_rectangle(
                lineXOffset, 
                lineYOffset, 
                currentWidth - 1, 
                currentHeight - 1, 
                fill=self.LINE_COLOR
                )
                
        #if set to draw horizontal, draw with rotated coordinates
        else:
            self.create_rectangle(
                0, 
                lineXOffset, 
                lineHeight, 
                currentWidth - 1,
                fill=self.LINE_COLOR
                )

            self.create_rectangle(
                lineYOffset,
                0,
                currentHeight - 1,
                lineWidth,
                fill=self.LINE_COLOR
                )

        

#end RoadIntersection