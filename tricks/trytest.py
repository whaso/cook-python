

def tryTest():
    try:
        a = 10
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


if __name__ == "__main__":
    # x = 0
    # while (x := x + 1) < 10:
    #     print(x)
    # readXML()
    # import re
    # r = re.compile("^(?:(?=.*[A-Z])(?=.*[a-z])(?=.*[0-9])).{8,}$")
    # hashTest()
    # a = tryTest()
    # print(a)
    

    pass
