import numpy as np
from collections import defaultdict
from naive import jaccard_similarity


def load_data(file_name):
    return np.loadtxt(file_name, delimiter='\t', dtype='int')


def get_sets(data):
    sets = defaultdict(set)
    for row in data:
        sets[row[0]].add(row[1])  # 向 row[0] 号集合添加元素 row[1]
    return sets


def universal_set(sets: dict) -> set:
    return set().union(*sets.values())


def check_key_continuity(sets):
    return list(sets.keys()) == list(range(1, len(sets) + 1))  # 集合索引是否连续


def get_sub_sets(R: dict, n: int) -> dict:
    """
    从集族 R 中返回随机 n 个集合构成的子集族
    """
    sub_sets = {}
    for i in np.random.choice(list(R.keys()), n, replace=False):
        sub_sets[i] = R[i]
    return sub_sets


def print_ret_size(naive_sim_pairs, min_hash_sim_pairs):
    print(f'Naive result size: {len(naive_sim_pairs)}')
    print(f'MinHash result size: {len(min_hash_sim_pairs)}')


def print_ret_sim(naive_sim_pairs, min_hash_sim_pairs):
    print(f'Jaccard similarity of two results: {jaccard_similarity(set(naive_sim_pairs), set(min_hash_sim_pairs)):.4%}')
