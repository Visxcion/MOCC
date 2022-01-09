import numpy as np
from arguments import *


class IndividualSeruFormation:
    def __init__(self):
        self.code_length = W * 2 - 1
        self.code = np.random.choice(range(1, self.code_length + 1), self.code_length, replace=False)
        self.serus = list()
        self.X = None

    def exchange(self):
        self.code = exchange(self.code, self.code_length)

    # get serus, X
    def decode(self):
        # set seru
        self.serus.clear()
        former = False
        for element in self.code:
            if element <= W:
                if former:
                    self.serus[len(self.serus) - 1].append(element)
                else:
                    self.serus.append([element])
                former = True
            else:
                former = False
        # set X
        self.X = np.zeros((W + 1, len(self.serus) + 1), dtype=int)
        for i in range(len(self.serus)):
            for j in range(len(self.serus[i])):
                self.X[self.serus[i][j]][i + 1] = 1


class IndividualSeruLoading:
    def __init__(self, code=None):
        if code:
            self.code_length = len(code)
            self.code = code
        else:
            self.code_length = W * M
            self.code = np.random.choice(range(1, self.code_length + 1), self.code_length, replace=False)
        self.order = None
        self.Z = None

    def exchange(self):
        self.code = exchange(self.code, self.code_length)

    # get order, Z
    def decode(self, seru_count):
        # set order
        self.order = [list() for i in range(seru_count)]
        for i in range(len(self.code)):
            if self.code[i] <= W:
                self.order[(i + 1) % seru_count].append(self.code[i])
        # set Z
        K = 0  # 订单数量上界
        for element in self.order:
            K = max(K, len(element))
        self.Z = np.zeros((M + 1, seru_count + 1, K + 1), dtype=int)
        for i in range(len(self.order)):
            for j in range(len(self.order[i])):
                self.Z[self.order[i][j]][i + 1][j + 1] = 1


def exchange(code, code_length):
    pos1, pos2 = np.random.choice(range(code_length), 2, replace=False)
    code[pos1], code[pos2] = code[pos2], code[pos1]
    return code


class GroupSeruFormation:
    def __init__(self, group_size):
        self.size = group_size
        self.individuals = list()
        # 初始化时随机选代表
        self.represent = np.random.choice(range(self.size), 1)[0]
        for i in range(self.size):
            self.individuals.append(IndividualSeruFormation())

    # 计算index的适应度并更新
    def update(self, index, cooperator):
        individual = self.individuals[index]

        TC = np.zeros(M + 1, dtype=float)
        for m in range(1, M + 1):
            t1 = .0
            for n in range(1, N + 1):
                for i in range(1, W + 1):
                    for j in range(1, len(individual.serus) + 1):
                        for k in range(1, M + 1):
                            t1 += V[m][n] * T_n * beta[n][i] * CW[i] * individual.X[i][j] * cooperator.Z[m][j][k]
            t2 = .0
            for i in range(1, W + 1):
                for j in range(1, len(individual.serus) + 1):
                    for k in range(1, M + 1):
                        t2 += individual.X[i][j] * cooperator.Z[m][j][k]
            TC[m] = t1 / t2

        # TODO: SCm
        SC = np.zeros(M + 1, dtype=float)
        for m in range(1, M + 1):
            pass

        FC = np.zeros(M + 1, dtype=float)
        for m in range(1, M + 1):
            for i in range(1, W + 1):
                for j in range(1, len(individual.serus) + 1):
                    for k in range(1, M + 1):
                        FC[m] += individual.X[i][j] * cooperator.Z[m][j][k]
            FC[m] = B[m] * TC[m] * W / FC[m]

        FCB = np.zeros(M + 1, dtype=float)
        for m in range(1, M + 1):
            for s in range(1, m):
                for j in range(1, len(individual.serus) + 1):
                    for k in range(1, m + 1):
                        FCB[m] += (FC[s] + SC[s]) * cooperator.Z[m][j][k] * cooperator.Z[s][j][k - 1]

        TTPT = 0
        for m in range(1, M + 1):
            TTPT = max(TTPT, FCB[m] + FC[m] + SC[m])
        TLH = 0
        for m in range(1, M + 1):
            for i in range(1, W + 1):
                for j in range(1, len(individual.serus)):
                    for k in range(1, M + 1):
                        TLH += FC[m] * individual.X[i][j] * cooperator.Z[m][j][k]


class GroupSeruLoading:
    def __init__(self, group_size):
        self.size = group_size
        self.individuals = list()
        # 初始化时随机选代表
        self.represent = np.random.choice(range(self.size), 1)[0]
        for i in range(self.size):
            self.individuals.append(IndividualSeruLoading())

    # 计算index的适应度并更新
    def update(self, index):
        pass
