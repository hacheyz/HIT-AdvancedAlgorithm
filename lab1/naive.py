from tqdm import tqdm


def jaccard_similarity(s1: set, s2: set) -> float:
    """
    计算两个集合的 Jaccard 相似度
    """
    return len(s1 & s2) / len(s1 | s2)


def naive_sim_pairs(R: dict, c: float) -> list:
    """
    返回集族 R 中满足相似度大于 c 的所有集合对
    """
    pairs = []
    set_index = list(R.keys())

    progress_bar = tqdm(total=len(set_index) * (len(set_index) - 1) // 2, desc='Naive')
    for i, r in enumerate(set_index):
        for s in set_index[i + 1:]:
            if jaccard_similarity(R[r], R[s]) >= c:
                pairs.append((r, s))
            progress_bar.update(1)
    progress_bar.close()
    return pairs
