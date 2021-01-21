# coding:utf-8
import rhinoscriptsyntax as rs

class Shape(object):
    """
    Shape
    """
    def __init__(self, x):
        self.x = x

    def draw(self):
        objs = []
        obj = rs.AddPoint(self.x,0,0) 
        objs.append(obj)
        return objs     