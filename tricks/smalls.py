import time
import functools
from typing import Any


def wrapper(func):
    counter = 0
    cache = {}

    @functools.wraps(func)
    def inner(*args: Any, **kwds: Any):
        nonlocal counter

        counter += 1
        print(f"func {func.__name__} runs {counter}")

        cache_key = (args, tuple(kwds.items()))
        if cache_key in cache:
            print("get cached data")
            return cache[cache_key]

        start = time.time()
        res = func(*args, **kwds)
        end = time.time()

        cache[cache_key] = res
        print(f"time cost: {round(end - start, 2)}s")
        return res
    return inner


@wrapper
def test(a):
    time.sleep(1)
    print(a)


if __name__ == "__main__":
    test(1)
    test(1)
