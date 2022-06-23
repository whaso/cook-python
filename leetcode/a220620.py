"""
荷兰国旗问题
"""

class Solution(object):
    def sortColors(self, nums):
        """
        :type nums: List[int]
        :rtype: None Do not return anything, modify nums in-place instead.
        """
        # all in [0, zero) is 0
        # all in [zero, i) is 1
        # all in [two, len] is 2
        l = len(nums)
        two = l
        zero = 0
        if l < 2:
            return
        i = 0

        while i < two:
            if i != zero and nums[i] == 0:
                nums[i], nums[zero] = nums[zero], nums[i]
                zero += 1
                i += 1
            elif nums[i] == 1:
                i += 1
            else:
                two -= 1
                nums[i], nums[two] = nums[two], nums[i]
