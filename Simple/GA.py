import individual
import math
import random


class GA:
    def __init__(self, crossrate, variationrate):
        """
        :param crossrate: 基因交叉发生的概率
        :param variationrate: 基因变异发生的概率
        1 crossrate：单点交叉概率
        2 variationrate：突变概率
        4 size：需要计算的种群大小
        5 generation：迭代次数
        7 best：种群最好的个体
        8 list：种群中所有的个体
        """
        self.crossrate = crossrate
        self.variationrate = variationrate
        self.size = 101
        self.generation = 200
        self.gene_num = 2
        self.best = None
        self.list = []
        pass

    def initpopulation(self):
        # 初始化一个种群大小的函数
        for i in range(self.size):
            n1 = random.uniform(-32, 32)
            n2 = random.uniform(-32, 32)
            life = individual.Individual(n1, n2)
            self.list.append(life)
            pass
        pass

    # 个体数值计算公式
    def ackleyFitnessFunc(self, x, y):
        ackleyComponentA = -0.2 * math.sqrt(0.5 * (x * x + y * y))
        ackleyComponentB = 0.5 * (math.cos(2 * math.pi * x) + math.cos(2 * math.pi * y))
        fitness = (-20 * math.exp(ackleyComponentA)) - math.exp(ackleyComponentB) + math.exp(1) + 20
        return fitness

    def function(self, individual):
        score = self.ackleyFitnessFunc(individual.gene[0], individual.gene[1])
        return score

    def caculate(self):
        self.best = self.list[0]
        for i in range(self.size):
            self.list[i].score = self.function(self.list[i])
            if self.best.score > self.list[i].score:
                self.best = self.list[i]
        pass

    def roulette_wheel(self):
        """
        轮盘赌普通方法得到被选中的基因型
        :param individuals: 种群中各个基因类型的数量
        :return: 返回被选中的基因型的代号
        """
        all_individual = 0
        for i in range(len(self.list)):
            all_individual += 1 / self.list[i].score
        probabilities = []
        for i in range(len(self.list)):
            probabilities.append((1 / self.list[i].score) / all_individual)
        selected_individual = random.uniform(0, 1)
        now_individual = 0.0
        for ind, val in enumerate(probabilities):
            now_individual += val
            if now_individual > selected_individual:
                return self.list[ind]

    def crossgene(self, parent1, parent2, index1, index2):
        child = [0, 0]
        child[0] = parent1.gene[0] * index1 + parent2.gene[0] * index2
        child[1] = parent1.gene[1] * index1 + parent2.gene[1] * index2
        return child

    def crossover(self, father, mother):
        """
        :param father: 需要进行遗传的父类个体
        :param mother: 需要进行遗传的母类个体
        :return:
        """
        x = random.randint(0, 9999)
        # 变异有概率，大于某个值就不发生，小于某个值就发生变异
        k = 10000 * self.variationrate
        if x < k:
            # 进行单点交换
            index1 = random.uniform(0, 1)
            index2 = 1 - index1
            child1 = self.crossgene(father, mother, index1, index2)
            child2 = self.crossgene(mother, father, index1, index2)
        else:
            child1 = father.gene
            child2 = mother.gene
        return child1, child2

    def variation(self, individual):
        """
        :param individual: 需要判断是否进行变异的个体的基因
        :return: 变异或者没有变异以后的个体
        """
        x = random.randint(0, 9999)
        # 变异有概率，大于某个值就不发生，小于某个值就发生变异
        k = 10000 * self.variationrate
        if x < k:
            index = random.randint(0, 1)
            individual[index] = random.uniform(-32, 32)
        return individual

    # 进行繁衍，得到孩子
    def get_children(self):
        father = self.roulette_wheel()
        mother = self.roulette_wheel()
        child1, child2 = self.crossover(father, mother)
        self.variation(child1)
        self.variation(child2)
        return individual.Individual(child1[0], child1[1]), \
               individual.Individual(child2[0], child2[1])

    # 得到新一代种群
    def next_generation(self):
        new_list = []
        self.caculate()
        new_list.append(self.best)  # 最好的个体一定要,虽说回交有点不太好......
        while len(new_list) < len(self.list):
            individual1, individual2 = self.get_children()
            new_list.append(individual1)
            new_list.append(individual2)
        self.list = new_list
        self.generation += 1
        pass

    def get_what_we_need(self):
        return self.generation, self.best.gene, self.best.score
    pass
