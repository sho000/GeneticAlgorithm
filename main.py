# coding:utf-8
import random
from Generation.Shape import Shape

# globals
g_population = 50
g_shapes = []

def main():
    global g_population, g_shapes
    # 初期個体生成
    for i in range(g_population):
        x = random.uniform(0,1000)
        y = random.uniform(0,1000)
        z = 0
        shape = Shape([x,y,z])
        g_shapes.append(shape)

    # 初期個体描画
    for shape in g_shapes:
        objs = shape.draw()


# ga = GeneticAlgorithm(g_population)

if(__name__ == "__main__") :
    main()