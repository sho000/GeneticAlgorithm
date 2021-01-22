# coding:utf-8
from Optimization.GeneticAlgorithm import GeneticAlgorithm

# 設計変数、制約条件: [name,type,min,max]
constraints = [
    ["x","float",0,900]
]

# GA
populationNum = 50
ga = GeneticAlgorithm(populationNum, constraints)

