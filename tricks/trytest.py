import copy
import random
import logging

def tryTest():
    try:
        a = 10
        # None["1"]
        # a["a"]
    except Exception as e:
        print("in exception")
        return 10
    else:
        print("in else")
        return 20
    finally:
        print("in finally")
        return 30


def outter(func):
    print("11111")
    def inner(*args, **kwargs):
        print(22222)
        res = func(*args, **kwargs)
        return res
    print(33333)
    return inner


class Outter:
    def __init__(self, func) -> None:
        self._func = func
        print("get func")

    def __call__(self, *args, **kwds) -> None:
        print("before func")
        res = self._func(*args, **kwds)
        print("after func")
        return print("called!")


# print("befort t")
# @outter
# def t():
#     print("ttttt")
# print("after t")


# print("befort s")
# @Outter
def s():
    print("sssss")

# s = Outter(s)
# print("after s")

class Singleton(object):
    is_instance = None
    def __new__(cls, *args, **kwargs):
        print(type(cls.is_instance))
        cls.is_instance = object.__new__(cls) if cls.is_instance is None else cls.is_instance
        return cls.is_instance


def testSingleton():
    a = Singleton()
    print(id(a))
    b = Singleton()
    print(id(b))
    c = Singleton()
    print(id(c))


def t1():
    # pcost.py #
    # Reads input lines of the form 'NAME,SHARES,PRICE'. # For example:
    #
    # SYM,123,456.78
    import sys
    if len(sys.argv) != 2:
        raise SystemExit(f'Usage: {sys.argv[0]} filename')
    rows = []
    with open(sys.argv[1], 'rt') as file:
        for line in file: 
            rows.append(line.split(','))
    # rows is a list of this form #[
    # ['SYM', '123', '456.78'] # ...
    #]
    total = sum([int(row[1]) * float(row[2]) for row in rows ]) 
    print(f'Total cost: {total:0.2f}')


def jobTest():
    from joblib import Parallel, delayed
    def sing():
        import time
        time.sleep(1)
        print("sing")
    res = Parallel(n_jobs=3)(delayed(sing)() for i in range(10))
    print(res)

def readXls():
    import os
    from xlrd import open_workbook_xls
    file_path = os.path.abspath(os.path.dirname(__file__)) + "/15位升18位患者清单.xls"
    workbook = open_workbook_xls(file_path)
    sheet = workbook.sheet_by_name("SQL Results")
    rows = sheet.nrows
    cols = sheet.ncols
    os.getcwd()
    count = 0
    for row in range(1, rows):
        old_idno, new_idno = sheet.cell(row, 0), sheet.cell(row, 1)
        print(old_idno.value, new_idno.value, type(old_idno.value))
        count += 1
    print(count)


def readXML():
    import os
    from xml.dom.minidom import parse
    file_path = os.path.abspath(os.getcwd()) + "/tricks/117531696.xml"
    dom = parse(file_path)
    print("xml encoding: ", dom.encoding)

def reTest(password):
    import re
    r = re.compile("^(?:(?=.*[A-Z])(?=.*[a-z])(?=.*[0-9])).{8,}$")

def hashTest():
    import hashlib
    a = "123"


def func_out(num1):
    # 定义一个内部函数
    def func_inner(num2):
        # 这里本意想要修改外部num1的值，实际上是在内部函数定义了一个局部变量num1
        nonlocal num1  # 告诉解释器，此处使用的是 外部变量
        print(num1)  # 此时是外部的num1
        # 修改外部变量num1 1 -> 10
        num1 += 10
        # 内部函数使用了外部函数的变量(num1)
        result = num1 + num2
        print("结果是:", result)

    print(num1)
    func_inner(1)
    print(num1)

    # 外部函数返回了内部函数，这里返回的内部函数就是闭包
    return func_inner


class Outter:
    def __init__(self, f) -> None:
        print("init")
        self.f = f

    def __call__(self, *args, **kwargs) -> None:
        self.f(*args, **kwargs)
        print("f")


@Outter
def class_pp():
    print("class pp")


def bubble(l):
    n = len(l)
    if n <= 1:
        print(l)
        return

    for i in range(n-1):
        for j in range(n-i-1):
            if l[j] > l[j+1]:
                l[j], l[j+1] = l[j+1], l[j]
    print(l)

def select_sort(l):
    n = len(l)
    if n <= 1:
        print(l)
    
    for i in range(n-1):
        min_idx = i
        for j in range(i, n):
            if l[j] < l[min_idx]:
                min_idx = j
            l[min_idx], l[j] = l[j], l[min_idx]
    print(l)

def insert_sort(l):
    n = len(l)
    if n <= 1:
        print(l)
        return
    
    for i in range(1, n):
        while i > 0:
            if l[i] < l[i-1]:
                l[i], l[i-1] = l[i-1], l[i]
                print(l)
                i -= 1
            else:
                break
            
    print(l)


def weakTry():
    import weakref
    a = {1, 2}
    print(a)
    b = weakref.ref(a)
    print(b)
    print(b())
    a = 3
    print("===赋值后===")
    print(b())
    print(b())
    print(b())


def quick_sort(l, first, last):
    print(l)
    if first >= last:
        print(l)
        return

    min_idx = first
    max_idx = last

    mid_value = l[min_idx]

    while min_idx < max_idx:
        while min_idx < max_idx and l[max_idx] >= mid_value:
            max_idx -= 1
        l[min_idx] = l[max_idx]
        print(l)

        while min_idx < max_idx and l[min_idx] < mid_value:
            min_idx += 1
        l[max_idx] = l[min_idx]
        print(l)
    print(min_idx, max_idx)
    l[min_idx] = mid_value
    print(l)

    quick_sort(l, first, min_idx-1)
    quick_sort(l, min_idx+1, last)
    print(l)


def binery_search(l, i):
    if not l:
        return False
    
    n = len(l)
    mid = n // 2
    if l[mid] == i:
        return True
    elif l[mid] > i:
        return binery_search(l[:mid], i)
    else:
        return binery_search(l[mid+1:], i)


if __name__ == "__main__":
    print("main start")


    # insert_sort([1, 3, 5, 2, 9, 23, 23, 32, 12, 2, 0])
    # x = 0
    # while (x := x + 1) < 10:
    #     print(x)
    # readXML()
    # import re
    # r = re.compile("^(?:(?=.*[A-Z])(?=.*[a-z])(?=.*[0-9])).{8,}$")
    # hashTest()
    # a = tryTest()
    # print(a)
    # class_pp()

    tryTest()
    print("main end")
