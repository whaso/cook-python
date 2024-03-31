import random


def gen_unordered_list(length):
    # 生成一个指定长度的无序列表
    unordered_list = random.sample(range(1, length * 10), length)
    return unordered_list


# 冒泡排序
"""
冒一个泡，比较相邻两元素，最后比较出最大的
- 最优时间复杂度: O(n)
- 最坏时间复杂度: O(n^2)
- 稳定性：稳定
"""

def bubble_sort(l):
    n = len(l)
    if n <= 1:
        return
    for j in range(0, n-1):  # 0 ~ len - 1
        count = 0
        for i in range(0, n-1-j):  # 0 ~ len-1-j
            count += 1
            if l[i] > l[i+1]:
                l[i], l[i+1] = l[i+1], l[i]


# 选择排序
"""
认为左边有序，右边无序，右边找到最小的放左边，和左边交换位置
- 最优: O(n^2)
- 最坏: O(n^2)
- 稳定性：不稳定(升序每次选择最大)
"""

def select_sort(l):
    n = len(l)
    for j in range(0, n-1):
        min_index = j
        for i in range(j+1, n):
            if l[min_index] > l[i]:
                min_index = i
        l[min_index], l[j] = l[j], l[min_index]  # 遍历一遍找一个最小的出来换位置


# 插入排序
"""
通过构建有序序列，对未排序数据，对已排序序列从后向前扫描，找到相应位置并插入
在从后向前扫描过程中，需要反复把已排序元素逐步向后挪位，为最新元素提供插入空间
认为左边(开始为第一个)有序，右边无序，从右边取数，到左边有序区域从后往前挨个与前面的数字比较后按大小交换位置(类似冒泡)
- 最优: O(n)
- 最坏: O(n^2)
- 稳定性: 稳定
"""

def insertion_sort(l):
    n = len(l)
    for j in range(1, n):
        while j > 0:
            if l[j] < l[j-1]:
                l[j], l[j-1] = l[j-1], l[j]
                j -= 1
            else:
                break
        
# 快速排序
"""
又称划分交换排序，通过一遍排序将要排序的数据分割成独立的两部分，其中一部分的数据比另一部分小，如此递归下去
1. 从数列取一元素为基准
2. 重新排序数列，以基准分割，基准位于中间
3. 递归
递归出口是数列长度 <= 1
- 最优: O(nlogn) 二分
- 最坏: O(n^2) 一次只分出一个
- 稳定性: 不稳定
"""

def quick_sort(l, first, last):
    if first >= last:
        return
    
    mid_value = l[first]
    low = first
    high = last

    while high > low:
        while high > low and l[high] >= mid_value:
            high -= 1
        l[low] = l[high]
        while high > low and l[low] < mid_value:
            low += 1
        l[high] = l[low]
    
    l[low] = mid_value

    quick_sort(l, first, low-1)
    quick_sort(l, low+1, last)
        


if __name__ == "__main__":
    l = gen_unordered_list(10)
    print(l)
    quick_sort(l, 0, len(l)-1)
    print(l)
