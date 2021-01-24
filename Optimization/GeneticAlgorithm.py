# coding:utf-8
import rhinoscriptsyntax as rs
import scriptcontext as sc
import random
random.seed(3)
import bisect
from Generation.Shape import Shape
from Evaluation.FitnessLandscape import FitnessLandscape

from scriptcontext import doc
from System.Windows.Forms import *
import Rhino.UI
from System import Environment

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
        self.generations = []       # 世代ごとに全世代のShapesインスタンスを格納
        self.nextGenaration = []    # 次世代のShapesインスタンスを格納
        self.gCnt = 0               # 今の世代カウント
        self.N = 100                 # 世代あたりの個体数
        self.G = 40                  # 最大世代数
        
        # 確率
        self.remainProbability = 0.1      # 個体をそのままコピーする確率
        self.mutationProbability = 0.1     # 突然変異する確率
        self.crossOverProbability = 1 - self.remainProbability - self.mutationProbability   # 個体を交叉する確率
        
        # 手順
        self.algorithm()                             
    
    def algorithm(self):
        rs.EnableRedraw(False)
        # https://ja.wikipedia.org/wiki/%E9%81%BA%E4%BC%9D%E7%9A%84%E3%82%A2%E3%83%AB%E3%82%B4%E3%83%AA%E3%82%BA%E3%83%A0#%E3%82%A2%E3%83%AB%E3%82%B4%E3%83%AA%E3%82%BA%E3%83%A0%E3%81%AE%E6%B5%81%E3%82%8C
        # 遺伝的アルゴリズムは一般に以下の流れで実装される。
        # なお、下記では個体数をN, 最大世代数をGと置く。
        # 1 : あらかじめ 全世代の個体が入る集合self.generationsとN個の次世代の個体が入る集合self.nextGenarationを用意する。
        # 2 : 現世代に N 個の個体をランダムに生成する。
        self.makeFirstGenerates()
        
        # 7 : 最大世代数G回まで繰り返し
        while(self.gCnt<self.G):
            print("gCnt={}".format(self.gCnt))
            # escキーでbreak
            if (sc.escape_test(False)):
                break
            
            # 3 : 評価関数により、現世代の各個体の適応度をそれぞれ計算する。
            self.evaluate()

            # 4-3 : 上位ランキングの個体をn個選択してコピーする。
            n = int(self.N*self.remainProbability)
            self.remain(n)

            # 5 : 次世代の個体数がN個になるまで上記の動作を繰り返す。
            while(len(self.nextGenaration)<self.N-1):
                # escキーでbreak
                if (sc.escape_test(False)):
                    break
                # 4 : ある確率で次の3つの動作のどれかを行い、その結果を次世代に保存する。
                rnd = random.random()
                if(rnd <= self.crossOverProbability):
                    # 4-1 : 個体を二つ選択（選択方法は後述）して交叉（後述）を行う。
                    self.crossOver()
                elif(rnd > self.crossOverProbability and
                     rnd <= self.mutationProbability + self.crossOverProbability):
                    # 4-2 : 個体を一つ選択して突然変異（後述）を行う。
                    self.mutate()
                    

            # 6 : 次世代の個体数がN個になったら次世代の内容を全て現世代に移す。
            self.generations.append(self.nextGenaration)
            self.nextGenaration = []
            self.gCnt += 1

        # 描画
        self.drawEvaluation()
        self.drawGenerations()
        rs.EnableRedraw(True)

    def makeFirstGenerates(self):
        shapes = []
        for i in range(self.N):
            gene = []
            for varRange in self.varRanges:
                var = random.uniform(varRange[0], varRange[1])
                gene.append(var)
            shape = Shape(gene, self.gCnt)
            shapes.append(shape)
        self.generations.append(shapes)

    def evaluate(self):
        # 00 shape.fitnessを設定
        for shape in self.generations[self.gCnt]:
            shape.fitness = self.fitnessLandscape.getFitness(shape.gene)
        # 『発見的最適化手法による構造のフォルムとシステム』p26参照
        # 01 個体群のすべての個体の適応度を合計して全体適応度とする
        sumFitness = 0
        for shape in self.generations[self.gCnt]:
            sumFitness += shape.fitness
        # 02 各個体の適応度を全体適応度で割って各個体の選択確率を計算する
        for shape in self.generations[self.gCnt]:
            shape.selectionProbability = shape.fitness/sumFitness
        # 03 個体群全体に対して、選択確率の累計を計算する
        sumTotalselectionProbability = 0
        for shape in self.generations[self.gCnt]:
            sumTotalselectionProbability += shape.selectionProbability
            shape.sumTotalselectionProbability = sumTotalselectionProbability
    
    def crossOver(self):
        shapes = self._selectNByRoulette(2)
        if(shapes[0].fitness>shapes[1].fitness):
            fatherShape = shapes[0]
            motherShape = shapes[1]
        else:
            fatherShape = shapes[1]
            motherShape = shapes[0]
        
        gene = []
        vec = rs.VectorSubtract(motherShape.gene, fatherShape.gene)
        fatherWeight = motherShape.fitness/(fatherShape.fitness+motherShape.fitness)
        rnd = random.randint(0,1)
        if(rnd==0):
            vec = rs.VectorScale(vec,fatherWeight)
        else:
            vec = rs.VectorScale(vec,-fatherWeight)
        vec = rs.VectorAdd(vec, fatherShape.gene)
        for i in range(2):
            if(vec[i]<self.varRanges[i][0]):
                vec[i] = self.varRanges[i][0]
            elif(vec[i]>self.varRanges[i][1]):
                vec[i] = self.varRanges[i][1]
        gene = [vec[0],vec[1]]

        # gene = [
        #     (fatherShape.gene[0]+motherShape.gene[0])/2,
        #     (fatherShape.gene[1]+motherShape.gene[1])/2
        # ]

        newShape = Shape(gene, self.gCnt+1)
        newShape.fitness = self.fitnessLandscape.getFitness(newShape.gene)
        self.nextGenaration.append(newShape)
        fatherShape.children.append(newShape)
        motherShape.children.append(newShape)

    def mutate(self):
        shapes = self._selectNByRoulette(1)
        for shape in shapes:
            gene = []
            for varRange in self.varRanges:
                var = random.uniform(varRange[0], varRange[1])
                gene.append(var)
            newShape = Shape(gene, self.gCnt+1)
            newShape.fitness = self.fitnessLandscape.getFitness(newShape.gene)
            self.nextGenaration.append(newShape)

    def remain(self,n):
        shapes = self._selectByRanking(n)
        for shape in shapes:
            newShape = Shape(shape.gene, self.gCnt+1)
            newShape.fitness = self.fitnessLandscape.getFitness(newShape.gene)
            self.nextGenaration.append(newShape)
    
    def _selectByRanking(self, n):
        selectedShapes = []
        cnt = 0
        for shape in reversed(sorted(self.generations[self.gCnt],key=lambda i: i.fitness)):
            if(cnt>=n):break
            selectedShapes.append(shape)
            cnt+=1
        return selectedShapes

    def _selectByRandom(self, n):
        selectedShapes = []
        for i in range(n):
            rnd = random.randint(0,len(self.N)-1)
            shape = self.generations[self.gCnt][rnd]
            selectedShapes.append(shape)
        return selectedShapes

    def _selectNByRoulette(self,n):
        selectedShapes = []
        for i in range(n):
            # 04 0から1までの乱数を生成し、この乱数と選択確率の累計を比較していく。
            rnd = random.random()
            for shape in self.generations[self.gCnt]:
                # 05 選択確率の累計がその乱数より大きいか等しくなったとき、その個体を選択する 
                if(shape.sumTotalselectionProbability>=rnd):
                    selectedShapes.append(shape)
                    break
        # 06 選択された個体群を返す
        return selectedShapes
        
        # # 
        # for shape in sortedShapes:
        #     print(shape.fitness)

    def drawEvaluation(self):
        # layer
        layer_fitness = rs.AddLayer("fitness")
        layer_box = rs.AddLayer("box", color=rs.CreateColor([0,0,0]), parent=layer_fitness)
        layer_axis = rs.AddLayer("axis", color=rs.CreateColor([0,0,0]), parent=layer_fitness)
        layer_text = rs.AddLayer("text", color=rs.CreateColor([0,0,0]), parent=layer_fitness)
        layer_contour = rs.AddLayer("contour", color=rs.CreateColor([150,150,150]), parent=layer_fitness)
        # axis
        for i in range(4):
            guid = rs.AddLine(self.fitnessLandscape.guid_boundingBox[i],self.fitnessLandscape.guid_boundingBox[i+4])
            rs.ObjectLayer(guid, layer_box)
        for i in range(4):
            guid = rs.AddLine(self.fitnessLandscape.guid_boundingBox[i],self.fitnessLandscape.guid_boundingBox[(i+1)%4])
            rs.ObjectLayer(guid, layer_box)
        for i in range(4):
            guid = rs.AddLine(self.fitnessLandscape.guid_boundingBox[i+4],self.fitnessLandscape.guid_boundingBox[(i+1)%4+4])
            rs.ObjectLayer(guid, layer_box)
        # measure
        divisionX = 10
        divisionY = 10
        divisionZ = 20
        xDis = self.fitnessLandscape.xMax - self.fitnessLandscape.xMin
        yDis = self.fitnessLandscape.yMax - self.fitnessLandscape.yMin
        zDis = self.fitnessLandscape.zMax - self.fitnessLandscape.zMin
        xPitch = xDis/divisionX
        yPitch = yDis/divisionY
        zPitch = zDis/divisionZ
        for i in range(divisionX+1):
            sPt = [xPitch*i,  0, 0]
            sPt = rs.VectorAdd(sPt, self.fitnessLandscape.guid_boundingBox[0])
            ePt = [xPitch*i, -30, 0]
            ePt = rs.VectorAdd(ePt, self.fitnessLandscape.guid_boundingBox[0])
            guid = rs.AddLine(sPt,ePt)
            rs.ObjectLayer(guid, layer_axis)
        for i in range(divisionY+1):
            sPt = [0, yPitch*i, 0]
            sPt = rs.VectorAdd(sPt, self.fitnessLandscape.guid_boundingBox[1])
            ePt = [30, yPitch*i, 0]
            ePt = rs.VectorAdd(ePt, self.fitnessLandscape.guid_boundingBox[1])
            guid = rs.AddLine(sPt,ePt)
            rs.ObjectLayer(guid, layer_axis)
        for i in range(divisionZ+1):
            sPt = [0, 0, zPitch*i]
            sPt = rs.VectorAdd(sPt, self.fitnessLandscape.guid_boundingBox[0])
            ePt = [-30, 0, zPitch*i]
            ePt = rs.VectorAdd(ePt, self.fitnessLandscape.guid_boundingBox[0])
            guid = rs.AddLine(sPt,ePt)
            rs.ObjectLayer(guid, layer_axis)
        # text
        for i in range(divisionX+1):
            pt = [xPitch*i, -40, 0]
            pt = rs.VectorAdd(pt, self.fitnessLandscape.guid_boundingBox[0])
            text = "{:.1f}".format(pt[0])
            height=12
            font="Arial"
            font_style=0
            justification=2+262144  
            guid = rs.AddText(text, pt, height=height, font=font, font_style=font_style, justification=justification)
            rs.ObjectLayer(guid, layer_text)
        for i in range(divisionY+1):
            pt = [40, yPitch*i, 0]
            pt = rs.VectorAdd(pt, self.fitnessLandscape.guid_boundingBox[1])
            text = "{:.1f}".format(pt[1])
            height=12
            font="Arial"
            font_style=0
            justification=1+131072   
            guid = rs.AddText(text, pt, height=height, font=font, font_style=font_style, justification=justification)
            rs.ObjectLayer(guid, layer_text)
        for i in range(divisionZ+1):
            pt = [-40, 0, zPitch*i]
            pt = rs.VectorAdd(pt, self.fitnessLandscape.guid_boundingBox[0])
            text = "{:.1f}".format(pt[2])
            height=12
            font="Arial"
            font_style=0
            justification=4+131072 
            guid = rs.AddText(text, pt, height=height, font=font, font_style=font_style, justification=justification)
            rs.ObjectLayer(guid, layer_text)
        # xAxis title
        pt = rs.VectorAdd(self.fitnessLandscape.guid_boundingBox[0],self.fitnessLandscape.guid_boundingBox[1])
        pt = rs.VectorDivide(pt,2) 
        pt = [pt[0],pt[1]-100,pt[2]]
        text = "GENE0"
        height=18
        font="Arial"
        font_style=0
        justification=2+262144  
        guid = rs.AddText(text, pt, height=height, font=font, font_style=font_style, justification=justification)
        rs.ObjectLayer(guid, layer_text)
        # yAxis title
        pt = rs.VectorAdd(self.fitnessLandscape.guid_boundingBox[1],self.fitnessLandscape.guid_boundingBox[2])
        pt = rs.VectorDivide(pt,2) 
        pt = [pt[0]+100,pt[1],pt[2]]
        text = "GENE1"
        height=18
        font="Arial"
        font_style=0
        justification=1+131072   
        guid = rs.AddText(text, pt, height=height, font=font, font_style=font_style, justification=justification)
        rs.ObjectLayer(guid, layer_text)
        # zAxis title
        pt = rs.VectorAdd(self.fitnessLandscape.guid_boundingBox[0],self.fitnessLandscape.guid_boundingBox[4])
        pt = rs.VectorDivide(pt,2) 
        pt = [pt[0]-100,pt[1],pt[2]]
        text = "FITNESS"
        height=18
        font="Arial"
        font_style=0
        justification=4+131072   
        guid = rs.AddText(text, pt, height=height, font=font, font_style=font_style, justification=justification)
        rs.ObjectLayer(guid, layer_text)
        # contour
        guid = rs.AddSrfContourCrvs(self.fitnessLandscape.guid_fitnesslandscape, [self.fitnessLandscape.guid_boundingBox[0], self.fitnessLandscape.guid_boundingBox[4]], zPitch)
        rs.ObjectLayer(guid, layer_contour)
    
    def drawGenerations(self):
        # generations title
        layer_title = rs.AddLayer("title",color=rs.CreateColor([0,0,0]),parent="fitness")
        pt = rs.VectorAdd(self.fitnessLandscape.guid_boundingBox[0],self.fitnessLandscape.guid_boundingBox[1])
        pt = rs.VectorDivide(pt,2) 
        pt = [pt[0],pt[1]-200,pt[2]]
        text = "GENERATION"
        height=18
        font="Arial"
        font_style=0
        justification=2+262144  
        textTitle = rs.AddText(text, pt, height=height, font=font, font_style=font_style, justification=justification)
        rs.ObjectLayer(textTitle, layer_title)
        # draw generations
        for i, generation in enumerate(self.generations):
            # r = random.randint(0,255)
            # b = random.randint(0,255)
            # g = random.randint(0,255)
            # color = rs.CreateColor([r,g,b])
            color = rs.CreateColor([180,0,0])
            layer_generation = rs.AddLayer("generation{}".format(i),color=color)
            layer_shape = rs.AddLayer("shape{}".format(i),color=color,parent=layer_generation)
            layer_chilren = rs.AddLayer("children{}".format(i),color=color,visible=False,parent=layer_generation)
            for shape in generation:
                # shapes
                guid = rs.AddPoint(shape.gene[0], shape.gene[1], shape.fitness)
                rs.ObjectLayer(guid,layer_shape)
                # children
                for child in shape.children:
                    sPt = [shape.gene[0], shape.gene[1], shape.fitness]
                    ePt = [child.gene[0], child.gene[1], child.fitness]
                    dis = rs.Distance(sPt, ePt)
                    if(dis<0.01):break
                    guid = rs.AddLine(sPt,ePt)
                    rs.ObjectLayer(guid,layer_chilren)
                    # arrow
                    dimstyle = rs.CurrentDimStyle()
                    rs.DimStyleLeaderArrowSize( dimstyle, 0.1)
                    rs.CurveArrows(guid,2)
                # title
                text = "GENERATION {}".format(i)
                rs.TextObjectText(textTitle,text)
                
            # captureView
            self.captureView(i)
            rs.LayerVisible(layer_generation,visible=False)
    
    def captureView(self,i):
        #https://wiki.mcneel.com/developer/rhinocommonsamples/screencaptureview
        bitmap = doc.Views.ActiveView.CaptureToBitmap(False,False,False)
        bitmap.Save("image/image{}.png".format(i))
