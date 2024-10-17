"""
实现一种随机图，在随机图上实现对最小生成树的抽样过程，
由抽样过程实现蒙特卡罗方法计算最小生成树权值的数学期望估计，
比较估计结果的准确性

步骤：
1. 实现算法产生 n 顶点随机图的生成
    输入：n
    输出：一个 n 顶点随机图，任意两个顶点之间边的权值均匀分布于 (0, 1)
2. 调用第 1 步实现的算法，实现对 n 顶点图的均匀抽样
3. 在抽样样本上计算最小生成树并计算其权值的数学期望
4. 在第 2 步和第 3 步的基础上，建立 n 与最小生成树权值数学期望之间的关系
5. 对 n = 16, 32, 64, 128, 256, 512, 1024,... 展开实验，考察算法运行时间的变化，
    并检验所建立的关系的一般性
6. 尝试用理论分析解释实验结果
7. 撰写实验报告
"""

from graph import *
import time
import matplotlib.pyplot as plt
from mpmath import zeta

def main():
    n_list = np.arange(16, 1040, 16)
    iter_num = 10
    runtimes = []
    mst_weights = []

    for n in n_list:
        graph = RandomGraph(n)
        mst_weight = 0

        start_time = time.time()
        for _ in range(iter_num):
            graph.randomize()
            mst_weight += graph.prim()
        end_time = time.time()

        runtimes.append((end_time - start_time)/iter_num)
        mst_weights.append(mst_weight/iter_num)

    fig = plt.figure(dpi=400)
    ax = fig.add_subplot(111)
    ax.plot(n_list, runtimes, label='runtime')
    ax.set_ylabel('Runtime (s)')
    ax.set_xlabel('Vertex num n')
    ax.set_title('Runtime of Prim Algorithm')
    plt.show()

    fig = plt.figure(dpi=400)
    ax = fig.add_subplot(111)
    ax.plot(n_list, mst_weights, label='mst_weights')
    Apery_const = zeta(3)  # Apery's constant
    ax.plot([0, n_list[-1]], [Apery_const, Apery_const], linestyle='--', c='gray')
    ax.set_ylabel('Mean weight of MST')
    ax.set_xlabel('Vertex num n')
    ax.set_title('Relation between n and mean weight of MST')
    ax.set_ylim(1.0, 1.4)
    plt.show()


if __name__ == '__main__':
    main()
