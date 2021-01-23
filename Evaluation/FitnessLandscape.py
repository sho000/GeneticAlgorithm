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
        movePt = rs.VectorSubtract([0,0,0],self.guid_boundingBox[0])
        guid = rs.CopyObject(self.guid_fitnesslandscape)
        self.guid_fitnesslandscape = rs.MoveObject(guid,movePt)

    def getFitness(self,gene):
        fitness = -1
        h = rs.Distance(self.guid_boundingBox[2], self.guid_boundingBox[1])
        sPt = [gene[0],0,0]
        ePt = [gene[0],h,0]
        ray = rs.AddLine(sPt, ePt)
        intersection = rs.CurveCurveIntersection(self.guid_fitnesslandscape,ray)
        rs.DeleteObject(ray)
        fitness = intersection[0][1][1]
        return fitness
        