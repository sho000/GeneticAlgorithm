# coding:utf-8

class Individual(object):
    """
    Individual 個体
    """
    def __init__(self,gene):
        """
        constructor
        """
        self.gene = gene
        self.fitness = None