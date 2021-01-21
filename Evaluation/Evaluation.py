# coding:utf-8
import rhinoscriptsyntax as rs
class Evaluation(object):
    """
    Evaluation
    """
    def __init__(self):
        """
        constructor
        """
        self.fitnessLandscape = rs.GetObject("select fitness landscape")

    def getFitness(self,gene):
        fitness = 0
        return fitness
        