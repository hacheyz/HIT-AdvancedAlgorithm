import numpy as np
import string

"""
用 minHash 进行集合相似性连接
--------------------------
输入：集族 R = {r1, r2, ..., rn}, c ∈ (0, 1]
输出：{<r, s> ∈ R×R | sim(r, s) ≥ c} 
     sim(r, s) = |r ∩ s| / |r ∪ s|
--------------------------
要求：
1. 实现 Naive 算法
2. 实现 minHash 算法
3. 比较两种算法的运行结果是否一致
4. 设置不同的 Hash 函数个数，查看运行效率差别
5. 设置不同的 Hash 函数个数，比较返回结果差别
6. 总结得出确保最佳效果的 Hash 函数个数
7. 更换数据集，重复上述结果，得出一致的结论
8. 撰写实验报告
"""

# Naive 算法
def naive_sim_pairs(R, c):
    result = []
    for i in range(len(R)):
        for j in range(i+1, len(R)):
            r = R[i]
            s = R[j]
            sim = len(set(r) & set(s)) / len(set(r) | set(s))
            if sim >= c:
                result.append((r, s))
    return result

# minHash 算法
def minHash_sim_pairs(R, c, n):
    result = []
    for i in range(len(R)):
        for j in range(i+1, len(R)):
            r = R[i]
            s = R[j]
            sim = min_hash_sim(r, s, n)
            if sim >= c:
                result.append((r, s))
    return result

# 计算 minHash
def min_hash_sim(r, s, n):
    """
    输入：集合 r, s, Hash 函数个数 n
    输出：minHash 相似性
    """
    eql_cnt = 0  # 相等计数
    for i in range(n):
        h = np.random.permutation(set(r) | set(s))
        if min_hash(r, h) == min_hash(s, h):
            eql_cnt += 1
    return eql_cnt / n


def min_hash(r, h):
    """
    输入：集合 r, 排列 h
    输出：minHash 值
    """


    

# 测试
if __name__ == "__main__":
    np.random.seed(0)
    U = np.array(list(string.ascii_lowercase))  # 全集 U 为小写字母
    R = [np.random.choice(U, 5, replace=False) for _ in range(1000)]  # 随机生成 10 个集合
    c = 0.6
    h = 10
    print(naive_sim_pairs(R, c))
    # print(minHash_sim_pairs(R, c, h))
