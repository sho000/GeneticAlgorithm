# coding:utf-8
import rhinoscriptsyntax as rs
import scriptcontext as sc
import random
random.seed(1)
import bisect
from Generation.Shape import Shape
from Evaluation.FitnessLandscape import FitnessLandscape

class GeneticAlgorithm(object):
    """
    GA : 遺伝的アルゴリズム
    """
    def __init__(self):
        """
        コンストラクタ
        """
        self.generations = []       # 世代ごとにのShapeインスタンスを格納
        self.fitnessLandscape = FitnessLandscape()  # FitnessLandscapeインスタンスを格納
        w = self.fitnessLandscape.guid_boundingBox[1][0] - self.fitnessLandscape.guid_boundingBox[0][0]

        self.populationNum = 10             # 世代あたりの個体数
        self.varRanges = [[0,w]]            # 設計変数の範囲[min,max]
        self.generationLimitNum = 0         # 繰り返す世代数
        self.generationCnt = 0              # 今の世代カウント
        self.selectionProbability = 0.5    # 上位何%を次の世代に残すか
        
        
        # 手順
        self.step()                             
    
    def step(self):
        # 01. Generate : 初期世代生成
        self.generate()
        # 02. Evaluate : 評価
        self.evaluate()
        self.drawEvaluation()

        while(self.generationCnt<=self.generationLimitNum):
            # escキーでbreak
            if (sc.escape_test(False)):
                print "TimeConsumingTask cancelled."
                break

            # 03. Select : 選択
            selectedShapes = self.selectByRoulette()
            for shape in selectedShapes:
                rs.AddPoint([shape.gene[0],shape.fitness,0])

            # 04. Breed : 交配
            
            # 05. Mutate : 突然変異

            self.generationCnt += 1


        # drawGenerations
        self.drawGenerations()

    def generate(self):
        shapes = []
        for i in range(self.populationNum):
            gene = []
            for varRange in self.varRanges:
                var = random.uniform(varRange[0], varRange[1])
                gene.append(var)
            shape = Shape(gene)
            shapes.append(shape)
        self.generations.append(shapes)

    def evaluate(self):
        rs.EnableRedraw(False)
        for shape in self.generations[self.generationCnt]:
            fitness = self.fitnessLandscape.getFitness(shape.gene)
            shape.fitness = fitness
        rs.EnableRedraw(True)
    
    def selectByRoulette(self):
        selectedShapes = []
        # 『発見的最適化手法による構造のフォルムとシステム』p26参照
        # 01 個体群のすべての個体の適応度を合計して全体適応度とする
        sumFitness = 0
        for shape in self.generations[self.generationCnt]:
            sumFitness += shape.fitness
        # 02 各個体の適応度を全体適応度で割って各個体の選択確率を計算する
        for shape in self.generations[self.generationCnt]:
            shape.selectionProbability = shape.fitness/sumFitness
        # 03 個体群全体に対して、選択確率の累計を計算する
        sumTotalselectionProbability = 0
        for shape in self.generations[self.generationCnt]:
            sumTotalselectionProbability += shape.selectionProbability
            shape.sumTotalselectionProbability = sumTotalselectionProbability
        # 04 0から1までの乱数を生成し、この乱数と選択確率の累計を比較していく。
        # 05 選択確率の累計がその乱数より大きいか等しくなったとき、その個体を選択する 
        print()
        for i in range(self.populationNum):
            rnd = random.random()
            print("----------")
            print("rnd={}".format(rnd))
            print("----------")
            for shape in self.generations[self.generationCnt]:
                print("shape.fitness={}".format(shape.fitness))
                print("shape.selectionProbability={}".format(shape.selectionProbability))
                print("shape.sumTotalselectionProbability={}".format(shape.sumTotalselectionProbability))
                if(shape.sumTotalselectionProbability>=rnd):
                    selectedShapes.append(shape)
                    break
        # 06 選択された個体群を返す
        return selectedShapes
        
        
        # shape.fitnessでソート
        sortedShapes = reversed(sorted(self.generations[self.generationCnt],key=lambda i: i.fitness))
        # 
        for shape in sortedShapes:
            print(shape.fitness)

    def drawEvaluation(self):
        rs.EnableRedraw(False)
        # fitness layer
        layer_fitness = rs.AddLayer("fitness")
        # boudingbox
        color = rs.CreateColor([230,230,230])
        layer = rs.AddLayer("boundingbox", color=color, parent=layer_fitness)
        plane = rs.WorldXYPlane()
        w = rs.Distance(self.fitnessLandscape.guid_boundingBox[1], self.fitnessLandscape.guid_boundingBox[0])
        h = rs.Distance(self.fitnessLandscape.guid_boundingBox[2], self.fitnessLandscape.guid_boundingBox[1])
        guid = rs.AddRectangle(plane,w,h)
        rs.ObjectLayer(guid, layer)
        # measureX
        color = rs.CreateColor([150,150,150])
        layer = rs.AddLayer("measureX", color=color, parent=layer_fitness)
        division = 10
        minX = self.varRanges[0][0]
        maxX = self.varRanges[0][1]
        dis = maxX-minX
        xPitch = dis/division
        for i in range(division+1):
            sPt = [xPitch*i,   0, 0]
            ePt = [xPitch*i, -30, 0]
            guid = rs.AddLine(sPt,ePt)
            rs.ObjectLayer(guid, layer)
        # textX
        color = rs.CreateColor([150,150,150])
        layer = rs.AddLayer("textX", color=color, parent=layer_fitness)
        for i in range(division+1):
            text = "{}".format(i*xPitch)
            pt = [xPitch*i, -35, 0]
            height=15
            font="Roboto"
            font_style=0
            justification=2+262144  
            guid = rs.AddText(text, pt, height=height, font=font, font_style=font_style, justification=justification)
            rs.ObjectLayer(guid, layer)
        # measureY
        color = rs.CreateColor([150,150,150])
        layer = rs.AddLayer("measureY", color=color, parent=layer_fitness)
        division = 10
        yPitch = h/division
        for i in range(division+1):
            sPt = [0, yPitch*i, 0]
            ePt = [-30, yPitch*i, 0]
            guid = rs.AddLine(sPt,ePt)
            rs.ObjectLayer(guid, layer)
        # textY
        color = rs.CreateColor([150,150,150])
        layer = rs.AddLayer("textY", color=color, parent=layer_fitness)
        for i in range(division+1):
            text = "{:2}".format(i/10.0)
            pt = [-35, yPitch*i, 0]
            height=15
            font="Roboto"
            font_style=0
            justification=4+131072 
            guid = rs.AddText(text, pt, height=height, font=font, font_style=font_style, justification=justification)
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
        
        

    
        
    