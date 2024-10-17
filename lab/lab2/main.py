"""
比较 3 种中位数选择算法的性能
 - 算法 1：排序后选择
 - 算法 2： 确定型中位数线性时间选择 (BFPRT)
 - 算法 3： 中位数选择随机算法

实验内容：
 - 实现三种算法
 - 数据集自己寻找或生成
 - 运行时间比较，准确度比较
 - 扩展性比较
 - 以恰当、准确、规范的形式表述实验结果
"""

import time
import numpy as np
import matplotlib.pyplot as plt

from sort_select import sort_select
from bfprt_select import bfprt_select
from lazy_select import lazy_select
from gen_data import gen_data


def run_select(arr: list, k_list: list, func) -> list:
    """测试选择算法, 返回运行结果"""
    result = []
    for k in k_list:
        result.append(func(arr, k))
    return result


def test_all_on_data(arr: list, k_list: list):
    run_time = []

    start_time = time.time()
    sort_select_result = run_select(arr, k_list, sort_select)
    run_time.append(time.time() - start_time)

    start_time = time.time()
    bfprt_select_result = run_select(arr, k_list, bfprt_select)
    run_time.append(time.time() - start_time)

    start_time = time.time()
    lazy_select_result = run_select(arr, k_list, lazy_select)
    run_time.append(time.time() - start_time)

    if (sort_select_result != bfprt_select_result) or (sort_select_result != lazy_select_result):
        print("Results are not equal!")

    return run_time


def test(data_type: str, n_list: list, iter_num: int):
    run_times = [[] for _ in range(3)]  # [[sort_select], [bfprt_select], [lazy_select
    for n in n_list:
        arr, k_list = gen_data(data_type, n, iter_num)
        run_time = test_all_on_data(arr, k_list)
        for i in range(3):
            run_times[i].append(run_time[i] / iter_num)

    fig = plt.figure(dpi=400)
    ax = fig.add_subplot(111)
    ax.plot(n_list, run_times[0], label="sort_select")
    ax.plot(n_list, run_times[1], label="bfprt_select")
    ax.plot(n_list, run_times[2], label="lazy_select")
    ax.set_xlabel("Data Size")
    ax.set_ylabel("Run Time")
    ax.set_title(("Run Time of Three Select Algorithms on " + data_type + " Data").title())
    ax.legend()
    plt.show()


def test_theta(n: int, iter_num: int):
    theta_list = np.linspace(0.5, 1, 100).tolist()
    run_times = []
    for theta in theta_list:
        arr, k_list = gen_data("uniform", n, iter_num)
        start_time = time.time()
        for k in k_list:
            lazy_select(arr, k, theta)
        run_times.append((time.time() - start_time) / iter_num)

    fig = plt.figure(dpi=400)
    ax = fig.add_subplot(111)
    ax.plot(theta_list, run_times)
    ax.set_xlabel("Theta")
    ax.set_ylabel("Run Time")
    ax.set_title("Run Time of Lazy Select Algorithm on Different Theta")
    plt.show()


def main():
    # 测试 3 种算法的性能和扩展性
    iter_num = 3  # 测试次数
    n_list = np.linspace(10000, 100000, 20, dtype=int).tolist()  # 数据规模
    data_type_list = ["uniform", "normal", "zipf"]
    for data_type in data_type_list:
        test(data_type, n_list, iter_num)

    # 测试随机算法中的关键参数 theta 对性能的影响
    n = 10000
    test_theta(n, iter_num)


if __name__ == "__main__":
    main()
