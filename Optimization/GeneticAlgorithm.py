# coding:utf-8
import rhinoscriptsyntax as rs
import random
random.seed(1)
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
        self.generationNum = 0
        self.generations = []
        self.fitnessLandscape = FitnessLandscape()

        self.step()
    
    def step(self):
        """
        手順
        """
        # 01. Generate : 生成
        self.generate()

        # 02. Evaluate : 評価
        self.evaluate()
        self.drawEvaluation()
        
        # 03. Select : 選択

        # 04. Breed : 交配
        
        # 05. Mutate : 突然変異

        #
        self.drawGenerations()

    def generate(self):
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

    def evaluate(self):
        rs.EnableRedraw(False)
        for shape in self.generations[self.generationNum]:
            fitness = self.fitnessLandscape.getFitness(shape.gene)
            shape.fitness = fitness
        rs.EnableRedraw(True)
    
    def drawEvaluation(self):
        rs.EnableRedraw(False)
        # fitness layer
        layer_fitness = rs.AddLayer("fitness")
        # boudingbox
        color = rs.CreateColor([200,200,200])
        layer = rs.AddLayer("boundingbox", color=color, parent=layer_fitness)
        plane = rs.WorldXYPlane()
        w = rs.Distance(self.fitnessLandscape.guid_boundingBox[1], self.fitnessLandscape.guid_boundingBox[0])
        h = rs.Distance(self.fitnessLandscape.guid_boundingBox[2], self.fitnessLandscape.guid_boundingBox[1])
        guid = rs.AddRectangle(plane,w,h)
        rs.ObjectLayer(guid, layer)
        # measure
        color = rs.CreateColor([150,150,150])
        layer = rs.AddLayer("measure", color=color, parent=layer_fitness)
        division = 10
        xPitch = w/division
        yPitch = h/division
        for i in range(division+1):
            sPt = [0, yPitch*i, 0]
            ePt = [-30, yPitch*i, 0]
            guid = rs.AddLine(sPt,ePt)
            rs.ObjectLayer(guid, layer)
        # fitnessLandscape
        color = rs.CreateColor([255,150,0])
        layer = rs.AddLayer("landscape", color=color, parent=layer_fitness)
        rs.ObjectLayer(self.fitnessLandscape.guid_fitnesslandscape, layer)
        rs.EnableRedraw(True)
    
    def drawGenerations(self):
        rs.EnableRedraw(False)
        for i, generation in enumerate(self.generations):
            r = random.randint(0,255)
            b = random.randint(0,255)
            g = random.randint(0,255)
            color = rs.CreateColor([r,g,b])
            layer_generation = rs.AddLayer("generation{}".format(i),color=color)
            for shape in generation:
                guid = rs.AddPoint(shape.gene[0],shape.fitness,0)
                rs.ObjectLayer(guid,layer_generation)
        rs.EnableRedraw(True)
        
        

    
        
    