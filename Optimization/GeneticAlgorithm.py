# coding:utf-8
import random
from Optimization.Individual import Individual

class GeneticAlgorithm(object):
    """
    GA : 遺伝的アルゴリズム
    """
    def __init__(   self, 
                    populationNum,
                    constraints,
                    evaluation):
        """
        コンストラクタ
        """
        self.populationNum = populationNum    # 世代あたりの個体数
        self.constraints = constraints          # 設計変数
        self.evaluation = evaluation
        self.generations = []

        self.step()

    def step(self):
        """
        手順
        """
        # 01. Generate : 生成
        self.generate()

        # 02. Evaluate : 評価
        self.evaluate()

        # 03. Select : 選択

        # 04. Breed : 交配
        
        # 05. Mutate : 突然変異

    def generate(self):
        """
        generate
        """
        individuals = []
        for i in range(self.populationNum):
            gene = []
            for var in self.constraints:
                varName = var[0]
                varType = var[1]
                varMin = var[2]
                varMax = var[3]
                if(varType=="float"):
                    v = random.uniform(varMin, varMax)
                    gene.append(v)
            individual = Individual(gene)
            individuals.append(individual)
        self.generations.append(individuals)
    
    def evaluate(self):
        """
        evaluate
        """
        self.evaluation.getFitness()