def median(arr: list) -> int:
    """返回 arr 的中位数, arr 的长度不超过 5"""
    assert len(arr) <= 5
    arr.sort()
    return arr[len(arr) // 2]


def partition(arr: list, MoM: int) -> tuple:
    """根据 MoM 划分 arr 为三部分：L, E, G"""
    L, E, G = [], [], []  # less, equal, greater
    for num in arr:
        if num < MoM:
            L.append(num)
        elif num == MoM:
            E.append(num)
        else:
            G.append(num)
    return L, E, G


def bfprt(arr: list) -> int:
    """返回 arr 的中位数的中位数"""
    n = len(arr)
    if n <= 5:
        return median(arr)
    m = n // 5
    groups = [arr[i * 5:(i + 1) * 5] for i in range(m)]
    medians = [median(group) for group in groups]
    return bfprt(medians)


def bfprt_select(arr: list, k: int) -> int:
    """返回 arr 中第 k 小的元素"""
    # 1. 将 arr 划分为 n//5 组，每组 5 个元素
    # 2. 对每个组进行排序，找到其中位数
    # 3. 递归地调用 bfprt_select，找到这些中位数的中位数 MoM
    # 4. 以 MoM 为基准，划分 arr 为三部分：L, E, G
    # 5. 根据 k 与 L, E, G 的大小关系，递归地调用 bfprt_select
    # 6. 返回结果

    if len(arr) <= 5:
        return sorted(arr)[k]  # 直接返回第 k 小的元素
    MoM = bfprt(arr)
    L, E, G = partition(arr, MoM)
    if k < len(L):
        return bfprt_select(L, k)
    elif k < len(L) + len(E):
        return E[0]
    else:
        return bfprt_select(G, k - len(L) - len(E))
