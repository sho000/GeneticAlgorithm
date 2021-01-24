# coding:utf-8

class Shape(object):
    """
    Shape
    """
    def __init__(self, gene, gCnt):
        self.gene = gene
        self.gCnt = gCnt
        self.fitness = 0                       # 適応度
        self.selectionProbability = 0          # 期待値（ルーレット選択で使用）
        self.sumTotalselectionProbability = 0  # 期待値の累計（ルーレット選択で使用）
        self.children = []
