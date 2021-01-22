# coding:utf-8
import rhinoscriptsyntax as rs
import random
from Generation.Shape import Shape
from Evaluation.FitnessLandscape import FitnessLandscape

class GeneticAlgorithm(object):
    """
    GA : 遺伝的アルゴリズム
    """
    def __init__(   self, 
                    populationNum,
                    constraints):
        """
        コンストラクタ
        """
        self.populationNum = populationNum    # 世代あたりの個体数
        self.constraints = constraints          # 設計変数
        self.generations = []
        self.fitnessLandscape = FitnessLandscape()

        self.step()
    
    def step(self):
        """
        手順
        """
        # 01. Generate : 生成
        self.generate()
        self.drawGenerations()

        # 02. Evaluate : 評価
        self.evaluate()
        # self.drawEvaluation()
        
        # 03. Select : 選択

        # 04. Breed : 交配
        
        # 05. Mutate : 突然変異

    def generate(self):
        """
        generate
        """
        shapes = []
        for i in range(self.populationNum):
            gene = []
            for constraint in self.constraints:
                varName = constraint[0]
                varType = constraint[1]
                varMin = constraint[2]
                varMax = constraint[3]
                if(varType=="float"):
                    v = random.uniform(varMin, varMax)
                elif(varType=="int"):
                    v = random.randint(varMin, varMax)
                else:
                    v = 0
                gene.append(v)
            shape = Shape(gene)
            shapes.append(shape)
        self.generations.append(shapes)
    
    def drawGenerations(self):
        for i, generation in enumerate(self.generations):
            layer = rs.AddLayer("generation{}".format(i))
            for shape in generation:
                guids = shape.draw()
                rs.ObjectLayer(guids,layer)
    
    def evaluate(self):
        """
        evaluate
        """
        guids = self.fitnessLandscape.drawBoundingBox()

    
        
    