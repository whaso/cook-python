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


def p_nums(m, n):
    l = 0
    for i in range(m, n + 1):
        if is_prime(i):
            l += 1
            print(i)
    return l

def is_prime(n):
    if n < 2:
        return False
    for i in range(2, int(n/2) + 1):
        if n % i == 0:
            return False
    return True


class Solution(object):
    def lengthOfLongestSubstring(self, s):
        """
        :type s: str
        :rtype: int
        "pwwkew"
        """
        left = -1
        right = 0
        max_len = 0
        slength = len(s)
        temp = set()
        while right < slength:
            if s[right] not in temp:
                temp.add(s[right])
                max_len = max(len(temp), max_len)
                right += 1
            else:
                left += 1
                temp.remove(s[left])
        return max_len


if __name__ == "__main__":
    Solution().lengthOfLongestSubstring("pwwkew")


