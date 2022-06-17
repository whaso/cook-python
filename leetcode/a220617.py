
"""
给定 n 个非负整数表示每个宽度为 1 的柱子的高度图，计算按此排列的柱子，下雨之后能接多少雨水。
1. i的水量为min(i左右最大高度lmax[i], rmax[i]) - i高度
2. 遍历取lrmax

"""


def js(height):
    if not height:
        return 0

    n = len(height)
    lmax = [0] * n
    for i in range(n):
        if i == 0:
            lmax[i] = height[i]
            continue
        lmax[i] = max(lmax[i-1], height[i])
    print(lmax)

    rmax = [0] * n
    for i in range(n-1, -1, -1):
        if i == n - 1:
            rmax[i] = height[i]
            continue
        rmax[i] = max(rmax[i+1], height[i])
    print(rmax)

    
