# coding:utf-8

class Shape(object):
    """
    Shape
    """
    def __init__(self, no, gene, gCnt):
        self.no = no
        self.gene = gene
        self.gCnt = gCnt
        self.fitness = -1                       # 適応度
        self.selectionProbability = -1          # 期待値（ルーレット選択で使用）
        self.sumTotalselectionProbability = -1  # 期待値の累計（ルーレット選択で使用）
