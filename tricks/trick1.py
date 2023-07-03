

def dynamic():
    def d(n):
        if n == 1:
            return 1
        elif n == 2:
            return 2
        return d(n - 1) + d(n - 2)

    for i in range(1, 10):
        print(d(i))


def bs():
    nums = [1, 3, 2, 9, 3, 8, 2]

    def f(low, high, num):
        mid = (high + low) // 2
        if num > nums[mid]:
            low = mid + 1
        elif num < nums[mid]:
            high = mid - 1
        else:
            return mid
        return f(low, high, num)
    print(f(0, len(nums) - 1, 3))


if __name__ == "__main__":
    pass
