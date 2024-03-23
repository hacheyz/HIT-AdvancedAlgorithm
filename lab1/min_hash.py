from utils import universal_set
import numpy as np
from tqdm import tqdm


def min_hash_sim_pairs(R: dict, c: float, n: int) -> list:
    """
    返回集族 R 中满足相似度大于 c 的所有集合对
    """
    pairs = []
    set_index = list(R.keys())
    U = universal_set(R)  # 全集

    # 构建 U 的 n 个随机排列，计算每个元素的 hash 值（元素在排列中的下标）
    U_list = list(U)
    hashes = []
    for i in range(n):
        np.random.shuffle(U_list)
        hash_val = {}
        for j, u in enumerate(U_list):
            hash_val[u] = j
        hashes.append(hash_val)

    # 计算集合的 Min Hash
    min_hash_mat = np.zeros((n, len(set_index)), dtype=int)
    for i in range(n):
        for j, r in enumerate(set_index):
            min_hash_mat[i, j] = min((hashes[i][x] for x in R[r]))

    # 计算相似集合对
    progress_bar = tqdm(total=len(set_index) * (len(set_index) - 1) // 2, desc='MinHash')
    for i, r in enumerate(set_index):
        for j, s in enumerate(set_index):
            if i < j:
                if np.mean(min_hash_mat[:, i] == min_hash_mat[:, j]) >= c:
                    pairs.append((r, s))
                progress_bar.update(1)
    progress_bar.close()
    return pairs
