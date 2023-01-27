""" 
1252. 奇数值单元格的数目
"""

class Solution(object):
    def oddCells(self, m, n, indices):
        """
        :type m: int
        :type n: int
        :type indices: List[List[int]]
        :rtype: int
        """
        l = [[0] * n for _ in range(m)]
        for i, j in indices:
            for k in range(n):
                l[i][k] += 1
            for k in range(m):
                l[k][j] += 1
        
        return sum(i % 2 for j in l for i in j)
