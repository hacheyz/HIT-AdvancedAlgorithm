from utils import universal_set
import numpy as np
from tqdm import tqdm


def pick_random_min_hash_functions(n: int, U_size: int) -> list:
    """
    随机生成 n 个哈希函数
    """
    hash_functions = []
    for _ in range(n):
        a = np.random.randint(1, U_size)
        b = np.random.randint(0, U_size)
        hash_functions.append(lambda x, _a=a, _b=b: (_a * x + _b) % U_size)
    return hash_functions


def min_hash_signature(s: int, min_hash_mat: np.array) -> np.array(int):
    """
    计算集合 s 的 min-hash 签名
    """
    signature = np.zeros(len(min_hash_mat), dtype=int)
    for i, h in enumerate(min_hash_mat):
        signature[i] = min_hash_mat[i, s]

    return signature


def min_hash_similarity(s1: int, s2: int, min_hash_mat: np.array) -> float:
    """
    用 min hash 签名估计两个集合的 Jaccard 相似度，n 为哈希函数数量
    """
    signature1 = min_hash_mat[:, s1]
    signature2 = min_hash_mat[:, s2]
    return np.mean(signature1 == signature2)


def min_hash_sim_pairs(R: dict, c: float, n: int) -> list:
    """
    返回集族 R 中满足相似度大于 c 的所有集合对
    """
    pairs = []
    set_index = list(R.keys())
    U = universal_set(R)  # 全集
    hash_functions = pick_random_min_hash_functions(n, len(U))

    # 提前计算元素的 hash 值
    hashes = []
    for h in hash_functions:
        hash_val = {}
        for i in universal_set(R):
            hash_val[i] = h(i)
        hashes.append(hash_val)

    # 提前计算集合的 min hash 值
    min_hash_mat = np.zeros((n, len(set_index)), dtype=int)
    for i, h in enumerate(hashes):
        for j, r in enumerate(set_index):
            min_hash_mat[i, j] = min((h[x] for x in R[r]))

    progress_bar = tqdm(total=len(set_index) * (len(set_index) - 1) // 2, desc='MinHash')
    for i in range(len(set_index)):
        signature_i = min_hash_mat[:, i]
        for j in range(i + 1, len(set_index)):
            signature_j = min_hash_mat[:, j]
            if np.mean(signature_i == signature_j) >= c:
                pairs.append((set_index[i], set_index[j]))
            progress_bar.update(1)
    progress_bar.close()
    return pairs
