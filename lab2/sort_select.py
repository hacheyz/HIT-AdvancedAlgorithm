def quick_sort(arr: list) -> list:
    """对 arr 进行快速排序"""
    if len(arr) <= 1:
        return arr
    pivot = arr[len(arr) // 2]
    left = [x for x in arr if x < pivot]
    middle = [x for x in arr if x == pivot]
    right = [x for x in arr if x > pivot]
    return quick_sort(left) + middle + quick_sort(right)


def sort_select(arr: list, k: int) -> int:
    """将 arr 排序后，返回其中第 k 小的元素"""
    arr = quick_sort(arr)
    return arr[k]
