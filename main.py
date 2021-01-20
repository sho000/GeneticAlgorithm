# coding:utf-8
import random
from Generation.Shape import Shape

# globals
population = 50
shapes = []

# 初期個体生成
for i in range(population):
    x = random.uniform(0,1000)
    y = random.uniform(0,1000)
    z = 0
    shape = Shape([x,y,z])
    shapes.append(shape)

# 初期個体描画
for shape in shapes:
    objs = shape.draw()


# ga = GeneticAlgorithm(g_population)

