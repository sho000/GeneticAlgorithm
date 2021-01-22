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
        self.guid = rs.GetObject("select fitness landscape")
    
    def setScale(self):
        rs.BoundingBox(self.gu)

    def getFitness(self,gene):
        fitness = 0
        return fitness
        