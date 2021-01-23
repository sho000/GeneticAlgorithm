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
        # instance of fitnessLandscape
        self.fitnessLandscape = FitnessLandscape()  

        # 設計変数の範囲[min,max]
        self.varRanges = [          
                [self.fitnessLandscape.xMin, self.fitnessLandscape.xMax],
                [self.fitnessLandscape.yMin, self.fitnessLandscape.yMax]
        ]
        
        # instance of Shapes
        self.generations = []       # 世代ごとにShapesインスタンスを格納
        self.N = 50                 # 世代あたりの個体数
        self.G = 0                  # 最大世代数
        self.gCnt = 0               # 今の世代カウント
        
        # 確率
        self.remainProbability = 0.1       # 個体をそのままコピーする確率
        self.mutationProbability = 0.1     # 突然変異する確率
        self.crossOverProbability = 1 - self.remainProbability - self.mutationProbability   # 個体を交叉する確率
        
        # 手順
        self.run()                             
    
    def run(self):
        # 遺伝的アルゴリズムは一般に以下の流れで実装される。
        # なお、下記では個体数を N, 最大世代数を G と置く。
        # 1 : あらかじめ 各世代のN 個の個体が入る集合self.generationsを用意する。
        #     以下、この二つの集合を「現世代」、「次世代」と呼ぶことにする。
        # 2 : 現世代に N 個の個体をランダムに生成する。
        self.makeFirstGenerates()
        
        # 7 : 最大世代数 G 回まで繰り返し
        while(self.gCnt<=self.G):
            # escキーでbreak
            if (sc.escape_test(False)):
                print "TimeConsumingTask cancelled."
                break

            # 3 : 評価関数により、現世代の各個体の適応度をそれぞれ計算する。
            self.evaluate()
            
            # 4 : ある確率で次の3つの動作のどれかを行い、その結果を次世代に保存する。
            #   4-1 : 個体を二つ選択（選択方法は後述）して交叉（後述）を行う。
            #   4-2 : 個体を一つ選択して突然変異（後述）を行う。
            #   4-3 : 個体を一つ選択してそのままコピーする。
            # self.makeNextGenarations()
            # 5 : 次世代の個体数が N 個になるまで上記の動作を繰り返す。
            # 6 : 次世代の個体数が N 個になったら次世代の内容を全て現世代に移す。
            self.gCnt += 1

        # 描画
        self.drawEvaluation()
        self.drawGenerations()

    def makeFirstGenerates(self):
        shapes = []
        for i in range(self.N):
            gene = []
            for varRange in self.varRanges:
                var = random.uniform(varRange[0], varRange[1])
                gene.append(var)
            shape = Shape(i, gene, self.gCnt)
            shapes.append(shape)
        self.generations.append(shapes)

    def evaluate(self):
        rs.EnableRedraw(False)
        for shape in self.generations[self.gCnt]:
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
        # layer
        layer_fitness = rs.AddLayer("fitness")
        layer_axis = rs.AddLayer("axis", color=rs.CreateColor([150,150,150]), parent=layer_fitness)
        layer_text = rs.AddLayer("text", color=rs.CreateColor([100,100,100]), parent=layer_fitness)
        layer_contour = rs.AddLayer("contour", color=rs.CreateColor([200,200,200]), parent=layer_fitness)
        # contour
        guid = rs.AddSrfContourCrvs(
            self.fitnessLandscape.guid_fitnesslandscape,
            [self.fitnessLandscape.guid_boundingBox[0], self.fitnessLandscape.guid_boundingBox[4]],
            10)
        rs.ObjectLayer(guid, layer_contour)
        # axis
        guid = rs.AddLine(self.fitnessLandscape.guid_boundingBox[0],self.fitnessLandscape.guid_boundingBox[1])
        rs.ObjectLayer(guid, layer_axis)
        guid = rs.AddLine(self.fitnessLandscape.guid_boundingBox[0],self.fitnessLandscape.guid_boundingBox[3])
        rs.ObjectLayer(guid, layer_axis)
        guid = rs.AddLine(self.fitnessLandscape.guid_boundingBox[0],self.fitnessLandscape.guid_boundingBox[4])
        rs.ObjectLayer(guid, layer_axis)
        # measure
        division = 10
        xDis = self.fitnessLandscape.xMax - self.fitnessLandscape.xMin
        yDis = self.fitnessLandscape.yMax - self.fitnessLandscape.yMin
        zDis = self.fitnessLandscape.zMax - self.fitnessLandscape.zMin
        xPitch = xDis/division
        yPitch = yDis/division
        zPitch = zDis/division
        for i in range(division+1):
            sPt = [xPitch*i,  0, 0]
            sPt = rs.VectorAdd(sPt, self.fitnessLandscape.guid_boundingBox[0])
            ePt = [xPitch*i, -30, 0]
            ePt = rs.VectorAdd(ePt, self.fitnessLandscape.guid_boundingBox[0])
            guid = rs.AddLine(sPt,ePt)
            rs.ObjectLayer(guid, layer_axis)
        for i in range(division+1):
            sPt = [0, yPitch*i, 0]
            sPt = rs.VectorAdd(sPt, self.fitnessLandscape.guid_boundingBox[0])
            ePt = [-30, yPitch*i, 0]
            ePt = rs.VectorAdd(ePt, self.fitnessLandscape.guid_boundingBox[0])
            guid = rs.AddLine(sPt,ePt)
            rs.ObjectLayer(guid, layer_axis)
        for i in range(division+1):
            sPt = [0, 0, zPitch*i]
            sPt = rs.VectorAdd(sPt, self.fitnessLandscape.guid_boundingBox[0])
            ePt = [-30, 0, zPitch*i]
            ePt = rs.VectorAdd(ePt, self.fitnessLandscape.guid_boundingBox[0])
            guid = rs.AddLine(sPt,ePt)
            rs.ObjectLayer(guid, layer_axis)
        # text
        for i in range(division+1):
            pt = [xPitch*i, -40, 0]
            pt = rs.VectorAdd(pt, self.fitnessLandscape.guid_boundingBox[0])
            text = "{:.1f}".format(pt[0])
            height=12
            font="Arial"
            font_style=0
            justification=2+262144  
            guid = rs.AddText(text, pt, height=height, font=font, font_style=font_style, justification=justification)
            rs.ObjectLayer(guid, layer_text)
        for i in range(division+1):
            pt = [-40, yPitch*i, 0]
            pt = rs.VectorAdd(pt, self.fitnessLandscape.guid_boundingBox[0])
            text = "{:.1f}".format(pt[1])
            height=12
            font="Arial"
            font_style=0
            justification=4+131072   
            guid = rs.AddText(text, pt, height=height, font=font, font_style=font_style, justification=justification)
            rs.ObjectLayer(guid, layer_text)
        for i in range(division+1):
            pt = [-40, 0, zPitch*i]
            pt = rs.VectorAdd(pt, self.fitnessLandscape.guid_boundingBox[0])
            text = "{:.1f}".format(pt[2])
            height=12
            font="Arial"
            font_style=0
            justification=4+131072 
            guid = rs.AddText(text, pt, height=height, font=font, font_style=font_style, justification=justification)
            rs.ObjectLayer(guid, layer_text)
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
                guid = rs.AddPoint(shape.gene[0], shape.gene[1], shape.fitness)
                rs.ObjectLayer(guid,layer_generation)
        rs.EnableRedraw(True)
        
        

    
        
    