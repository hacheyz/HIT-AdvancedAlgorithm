import numpy as np
import time
from utils import load_data
from utils import get_sets, get_sub_sets
from utils import print_ret_size, print_ret_sim
from naive import naive_sim_pairs, jaccard_similarity
from min_hash import min_hash_sim_pairs
from draw import draw_time
from draw import draw_sim

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

# 测试
if __name__ == "__main__":
    np.random.seed(0)
    AOL_file_name = "./data/E1_AOL-out.txt"
    Booking_file_name = "./data/E1_Booking-out.txt"
    kosarak_file_name = "./data/E1_kosarak_100k.txt"
    data = load_data(kosarak_file_name)
    full_sets = get_sets(data)
    sets = get_sub_sets(full_sets, 1000)

    c = 0.8
    ret_naive = naive_sim_pairs(sets, c)
    ret_min_hash = min_hash_sim_pairs(sets, c, 30)

    print_ret_size(ret_naive, ret_min_hash)  # 输出结果大小
    print_ret_sim(ret_naive, ret_min_hash)  # 输出结果相似度

    # 更改 hash 个数进行分析
    h_num = np.arange(2, 100, 2)
    sets = get_sub_sets(full_sets, 100)
    ret_naive = naive_sim_pairs(sets, c)
    time.sleep(1)

    # 绘制不同 Hash 函数个数下的运行效率差别
    print("\nRunning time test")
    times = []
    for n in h_num:
        start = time.time()
        min_hash_sim_pairs(sets, c, n)
        times.append(time.time() - start)
    draw_time(times, h_num)
    time.sleep(1)

    # 绘制不同 Hash 函数个数下的返回结果差别
    print("\nCorrectness test:")
    simlaritys = []
    for n in h_num:
        ret_min_hash = min_hash_sim_pairs(sets, c, n)
        simlaritys.append(jaccard_similarity(set(ret_naive), set(ret_min_hash)))
    draw_sim(simlaritys, h_num)
