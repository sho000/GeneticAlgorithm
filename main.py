# coding:utf-8
import random
from GA.GeneticAlgorithm import GeneticAlgorithm
from Generate.Generate import Generate

# globals
g_population = 50
g_phenotypes = []
g_genotypes = []

# 初期個体生成
for i in range(g_population):
    x = random.uniform(0,1000)
    y = random.uniform(0,1000)
    z = 0
    genotype = [x,y]
    phenotype = Generate([x,y,z])
    g_genotypes.append(genotype)
    g_phenotypes.append(phenotype)

# 初期個体描画
for phenotype in g_phenotypes:
    objs = phenotype.draw()


# ga = GeneticAlgorithm(g_population)