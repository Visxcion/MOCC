"""
1. 初始种群，随机产生个体编码，形成两个子种群
2. 使用个体编码内部交换操作对其中个体进行进化
3. 每个子种群在其他子种群代表的协助下评估群内部适应度并更新代表
4. 每代种群进化后采用精英策略生成下一代种群
5. 若未达到迭代次数，返回步骤2；若达到最终迭代次数，停止
"""

from arguments import *
from group import *


def init():
    for i in range(len(TYPE)):
        V[i + 1][TYPE[i]] = 1
    for i in range(1, W + 1):
        if W > eta_i:
            CW[i] = 1. + epsilon * (W - eta_i)
    return GroupSeruFormation(GROUP_SIZE_F), GroupSeruLoading(GROUP_SIZE_L)


def exchange():
    for i in range(group_f.size):
        if np.random.random() < P_c:
            group_f.individuals[i].exchange()
    for i in range(group_l.size):
        if np.random.random() < P_c:
            group_l.individuals[i].exchange()


def cooperate():
    for i in range(group_f.size):
        group_f.update(i)
    for i in range(group_l.size):
        group_l.update(i)


def elite():
    pass


if __name__ == '__main__':
    group_f, group_l = init()
    for iteration in range(MAX_ITERATION):
        exchange()
        cooperate()
        elite()
