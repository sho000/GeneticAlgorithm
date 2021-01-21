# coding:utf-8
import random
from Optimization.GeneticAlgorithm import GeneticAlgorithm
from Generation.Shape import Shape
from Evaluation.Evaluation import Evaluation
import rhinoscriptsyntax as rs

# 設計変数、制約条件: [name,type,min,max]
constraints = [
    ["x","float",0,1000]
]

# evaluation
evaluation = Evaluation()

# ga
populationNum = 50
optimization = GeneticAlgorithm(
                    populationNum,
                    constraints,
                    evaluation)



# draw first generation
# rs.AddLayer("generation0")
# for i,individual in enumerate(optimization.generations[0]):
#     shape = Shape(individual.gene)
#     objs = shape.draw()
    
#     rs.ObjectLayer(objs,"generation0")