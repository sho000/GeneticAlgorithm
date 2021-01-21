# coding:utf-8
import random
from Optimization.GeneticAlgorithm import GeneticAlgorithm
from Generation.Shape import Shape
from Evaluation.Evaluation import Evaluation
import rhinoscriptsyntax as rs

# globals
constraints = [
    ["x","float",0,1000],
    ["y","float",0,1000],
]
populationNum = 50

# evaluation = 

# instance of GeneticAlgorithm class
ga = GeneticAlgorithm(
        populationNum,
        constraints)

# draw first generation
rs.AddLayer("generation0")
for i,individual in enumerate(ga.generations[0]):
    shape = Shape(individual.gene)
    objs = shape.draw()
    
    rs.ObjectLayer(objs,"generation0")