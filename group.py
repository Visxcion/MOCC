import numpy as np
from arguments import *


class IndividualSeruFormation:
    def __init__(self):
        self.code_length = W * 2 - 1
        self.code = np.random.choice(range(1, self.code_length + 1), self.code_length, replace=False)
        self.seru = list()

    def exchange(self):
        self.code = exchange(self.code, self.code_length)

    # 根据code解码出seru
    def decode(self):
        self.seru.clear()
        former = False
        for element in self.code:
            if element <= W:
                if former:
                    self.seru[len(self.seru) - 1].append(element)
                else:
                    self.seru.append([element])
                former = True
            else:
                former = False


class IndividualSeruLoading:
    def __init__(self):
        self.code_length = W * M
        self.code = np.random.choice(range(1, self.code_length + 1), self.code_length, replace=False)

    def exchange(self):
        self.code = exchange(self.code, self.code_length)


def exchange(code, code_length):
    pos1, pos2 = np.random.choice(range(code_length), 2, replace=False)
    code[pos1], code[pos2] = code[pos2], code[pos1]
    return code


class GroupSeruFormation:
    def __init__(self, group_size):
        self.size = group_size
        self.individuals = list()
        self.represent = np.random.choice(range(self.size), 1)[0]
        for i in range(self.size):
            self.individuals.append(IndividualSeruFormation())

    # 计算index的适应度并更新
    def update(self, index):
        pass


class GroupSeruLoading:
    def __init__(self, group_size):
        self.size = group_size
        self.individuals = list()
        self.represent = np.random.choice(range(self.size), 1)[0]
        for i in range(self.size):
            self.individuals.append(IndividualSeruLoading())

    # 计算index的适应度并更新
    def update(self, index):
        pass
