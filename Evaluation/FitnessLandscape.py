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
        self.guid_fitnesslandscape = rs.GetObject("select fitness landscape surface", filter=rs.filter.surface)
        self.guid_boundingBox = rs.BoundingBox(self.guid_fitnesslandscape)
        self.xMin = self.guid_boundingBox[0][0]
        self.xMax = self.guid_boundingBox[1][0]
        self.yMin = self.guid_boundingBox[1][1]
        self.yMax = self.guid_boundingBox[2][1]
        self.zMin = self.guid_boundingBox[0][2]
        self.zMax = self.guid_boundingBox[4][2]

    def getFitness(self,gene):
        fitness = -1
        h = self.zMax - self.zMin
        sPt = [gene[0], gene[1], 0]
        ePt = [gene[0], gene[1], h*2]
        ray = rs.AddLine(sPt, ePt)
        intersection = rs.CurveSurfaceIntersection(ray, self.guid_fitnesslandscape)
        rs.DeleteObject(ray)
        fitness = intersection[0][1][2]
        return fitness
        