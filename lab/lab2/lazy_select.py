import random
from math import sqrt, floor


def rank(arr: list, x: int) -> int:
    """返回 arr 中小于 x 的元素个数"""
    return sum(1 for num in arr if num < x)


def min_k(sorted_arr: list, k: int) -> int:
    """返回有序数组 sorted_arr 中第 k 小的元素"""
    return sorted_arr[k]


def lazy_select(arr: list, k: int, theta: float = 3 / 4) -> int:
    """拉斯维加斯算法，返回 arr 中第 k 小的元素"""
    n = len(arr)
    R_len = int(n ** theta)
    R = random.choices(arr, k=R_len)  # 随机选择 n^(3/4) 个元素
    R.sort()  # 此排序的时间复杂度为 O(n)
    x = (k / n) * R_len  # arr 的第 k 小元素可能成为 R 的第 x 小元素
    l, h = max(floor(x - sqrt(n)), 0), min(floor(x + sqrt(n)), R_len - 1)  # 考察区间 [l, h]
    L, H = min_k(R, l), min_k(R, h)
    Lp, Hp = rank(arr, L), rank(arr, H)
    P = [num for num in arr if L <= num <= H]  # 将 arr 中介于 L, H 之间的元素放入 P

    if Lp <= k <= Hp and len(P) <= 4 * n ** theta + 1:
        P.sort()
        return min_k(P, k - Lp)
    else:
        if R_len < n:
            return lazy_select(arr, k, min(theta + 0.05, 1))  # 略微提高 R_len 的大小
        else:
            arr.sort()
            return min_k(arr, k)
