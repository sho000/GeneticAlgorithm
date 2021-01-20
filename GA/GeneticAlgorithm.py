# coding:utf-8

class GeneticAlgorithm(object):
    """
    GA遺伝的アルゴリズム
    """
    def __init__(self, population):
        """
        コンストラクタ
        """
        self.population = population    # 世代あたりの個体数
        self.generations = []
        # self.step()

    # def step(self):
    #     """
    #     手順
    #     """
    #     # 01. Generate : 生成
    #     self.generate()
    #     # 02. Evaluate : 評価

    #     # 03. Select : 選択

    #     # 04. Breed : 交配
        
    #     # 05. Mutate : 突然変異

    # def generate(self):
    #     """
    #     generate
    #     """
    #     generation = []
    #     for i in range(self.population):
    #         pass