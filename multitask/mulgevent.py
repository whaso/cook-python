from collections.abc import Iterable, Iterator


class ClassIterator:

    def __init__(self, obj) -> None:
        self.obj = obj
        self.cur_num = 0

    def __iter__(self):
        pass

    def __next__(self):
        if self.cur_num >= len(self.obj.names):
            raise StopIteration

        res = self.obj.names[self.cur_num]
        self.cur_num += 1
        return res


class Classmate:

    def __init__(self) -> None:
        self.names = list()

    def add(self, name):
        self.names.append(name)

    def __iter__(self):
        """想要一个对象称为一个 可迭代对象, 即可以用for遍历
        必须要有此方法
        """
        return ClassIterator(self)


# iter返回self
class Fibonacci:

    def __init__(self, cnt) -> None:
        self.nums = cnt
        self.cur_num = 0
        self.a = 0
        self.b = 1

    def __iter__(self):
        return self

    def __next__(self):
        if self.cur_num >= self.nums:
            raise StopIteration
        
        res = self.a
        self.a, self.b = self.b, self.a + self.b
        self.cur_num += 1

        return res


classmate = Classmate()

classmate.add("foo")
classmate.add("zoo")
classmate.add("yoo")

# iter方法会自动调用__iter__方法接收返回值, 其返回值就是迭代器也就是ClassIterator类创建的对象就是迭代器
classmate_iterator = iter(classmate)
print(isinstance(classmate_iterator, Iterator))  # 判断是否是迭代器 True

for i in classmate:
    print(i)  # foo zoo yoo

print(isinstance(classmate, Iterable))


def create_num(cnt):
    a, b = 0, 1
    cur_num = 0
    while cur_num < cnt:
        yield a
        a, b = b, a + b
        cur_num += 1

gen_obj = create_num(10)  # 此时创建了一个生成器对象
print(gen_obj)  # <generator object create_num at 0x0000022C5899D510>
print([i for i in gen_obj])  # [0, 1, 1, 2, 3, 5, 8, 13, 21, 34]


import time
from greenlet import greenlet

def t1():
    while True:
        print("----------A----------")
        gr2.switch()
        # time.sleep(1)


def t2():
    while True:
        print("----------B----------")
        gr1.switch()
        # time.sleep(1)

gr1 = greenlet(t1)
gr2 = greenlet(t2)

print(gr1, gr2)
gr2.switch()
"""
<greenlet.greenlet object at 0x00000276263C30F0 (otid=0x00000276263A9EE0) pending> <greenlet.greenlet object at 0x00000276263C31A0 (otid=0x00000276263C7040) pending>
----------B----------
----------A----------
----------B----------
----------A----------
...
"""