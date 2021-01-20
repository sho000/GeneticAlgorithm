# coding:utf-8
import rhinoscriptsyntax as rs

class Shape(object):
    """
    Shape
    """
    def __init__(self, pt):
        self.pt = pt

    def draw(self):
        objs = []
        obj = rs.AddPoint(self.pt) 
        objs.append(obj)
        return objs     