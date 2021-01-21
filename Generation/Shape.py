# coding:utf-8
import rhinoscriptsyntax as rs

class Shape(object):
    """
    Shape
    """
    def __init__(self, gene):
        self.gene = gene

    def draw(self):
        objs = []
        obj = rs.AddPoint(self.gene[0],0,0) 
        objs.append(obj)
        return objs     