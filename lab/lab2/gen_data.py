import numpy as np


def gen_data(data_type: str, n: int, iter_num: int) -> (list, list):
    k_list = [np.random.randint(0, n) for _ in range(iter_num)]
    if data_type == "uniform":
        return np.random.uniform(0, 1, n).tolist(), k_list
    elif data_type == "normal":
        return np.random.normal(0, 1, n).tolist(), k_list
    elif data_type == "zipf":
        return np.random.zipf(2, n).tolist(), k_list
