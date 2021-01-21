# coding:utf-8
import random
from Generation.Shape import Shape

class GeneticAlgorithm(object):
    """
    GA : 遺伝的アルゴリズム
    """
    def __init__(self, 
                    population=50):
        """
        コンストラクタ
        """
        self.population = population    # 世代あたりの個体数
        self.minX = 0
        self.maxX = 1000
        self.phenotypes = []
        self.genotypes = []
        self.step()

    def step(self):
        """
        手順
        """
        # 01. Generate : 生成
        self.generate()
        self.phenotypesDraw()

        # 02. Evaluate : 評価

        # 03. Select : 選択

        # 04. Breed : 交配
        
        # 05. Mutate : 突然変異

    def generate(self):
        """
        generate
        """
        for i in range(self.population):
            x = random.uniform(self.minX, self.maxX)
            phenotype = Shape(x)
            self.phenotypes.append(phenotype)
            self.genotypes.append(x)
    
    def phenotypesDraw(self):
        """
        generationDraw
        """
        for phenotype in self.phenotypes:
            phenotype.draw()