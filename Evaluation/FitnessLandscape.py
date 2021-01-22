# coding:utf-8
import rhinoscriptsyntax as rs
class FitnessLandscape(object):
    """
    FitnessLandscape
    """
    def __init__(self):
        """
        constructor
        """
        self.guid_fitnesslandscape = rs.GetObject("select fitness landscape")
        self.guid_boundingBox = rs.BoundingBox(self.guid_fitnesslandscape)
    
    def setScale(self):
        w = rs.VectorSubtract(self.guid_boundingBox[1]-self.guid_boundingBox[0])
        d = rs.VectorSubtract(self.guid_boundingBox[3]-self.guid_boundingBox[2])
    
    
    def drawBoundingBox(self):
        guids = []
        for pt in self.guid_boundingBox:
            guid = rs.AddPoint(pt)
            guids.append(guid)
        return guids
        

    def getFitness(self,gene):
        fitness = 0
        return fitness
        