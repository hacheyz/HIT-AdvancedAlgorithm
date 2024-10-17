import numpy as np

class RandomGraph:
    def __init__(self, n: int):
        """
        :param n: 图的顶点数
        """
        self.n = n
        self.graph = np.zeros((n, n))

    def randomize(self):
        """
        生成一个 n 顶点随机图，任意两个顶点之间边的权值均匀分布于 (0, 1)
        """
        self.graph = np.random.rand(self.n, self.n)
        self.graph = np.tril(self.graph, -1)  # 取下三角矩阵
        self.graph += self.graph.T  # 对称
        np.fill_diagonal(self.graph, np.inf)  # 设置对角线为无穷大

    def prim(self):
        """
        Prim 算法计算最小生成树权值
        :return: 最小生成树权值
        """
        n = self.n
        visited = [False] * n
        visited[0] = True
        dist = self.graph[0].copy()
        mst = 0
        for _ in range(n - 1):
            u = np.argmin(dist)
            mst += dist[u]
            dist[u] = np.inf
            visited[u] = True
            for v in range(n):
                if not visited[v] and self.graph[u, v] < dist[v]:
                    dist[v] = self.graph[u, v]
        return mst
