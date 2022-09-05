import re
import timeit
import bisect
import random
from enum import Enum
from textwrap import dedent
from typing import NamedTuple
from contextlib import contextmanager

from jinja2 import Template
from requests.exceptions import RequestException
from pydantic import BaseModel, conint, ValidationError


def render_movies_j2(username, movies):
    _MOVIES_TMPL = """
    Welcome, {{username}}.
    {% for name, rating in movies %}
    * {{ name }}, Rating: {{ rating|default("NOT RATED", False) }}
    {%- endfor %}
    """

    tmpl = Template(_MOVIES_TMPL)
    return tmpl.render(username=username, movies=movies)


def t0():
    movies = [
        ("The Shawshank Redemption", "9.3"),
        ("The Prestige", "8.5"),
        ("Mulan", "")
    ]
    print(render_movies_j2("Wang", movies))


def t1():
    """必须要用\开头才行 不到为啥"""
    a = """\
        sdf
        sdf"""
    print(dedent(a))


WORDS = ["Hello", "string", "performance", "test"] * 25


def str_cat(WORDS):
    s = ""
    l = []
    for word in WORDS:
        s += word
        l.append(word)
        pass
    return s


def str_join(WORDS):
    l = []
    for word in WORDS:
        l.append(word)
    return "".join(l)


def t2():
    
    # 执行100万次
    cat_spend = timeit.timeit(setup="from __main__ import str_cat", stmt="str_cat(WORDS)", globals=globals())
    print("cat_spend:", cat_spend)

    join_spend = timeit.timeit(setup="from __main__ import str_join", stmt="str_join(WORDS)", globals=globals())
    print("join_spend:", join_spend)


class myEnum(int, Enum):
    # 在定义枚举类型时，如果同时继承一些基础类型，比如str、int
    # 枚举类型就能同时充当该基础类型使用。
    VIP = 3
    BANNED = 13

class myDictEnum(dict, Enum):
    # 在定义枚举类型时，如果同时继承一些基础类型，比如str、int
    # 枚举类型就能同时充当该基础类型使用。
    VIP = {}
    BANNED = {}


class Address(NamedTuple):
    country: str
    province: str
    city: str

addr = Address("道外区", "黑龙江", "哈尔滨")


class UserCollection:
    """用于保存多个用户的集合工具类"""

    def __init__(self, users) -> None:
        self.items = users


users = UserCollection(["A", "B"])


class UserCollectionNew(UserCollection):
    """定义了__len__方法就可以用于真值测试 if users_new 是有意义的 对比users则一直为真，不论items是否为空
    同 __bool__ 方法，如果两个都定义，bool方法优先
    """
    def __init__(self, users) -> None:
        super().__init__(users)
    
    def __len__(self):
        return len(self.items)

users_new = UserCollectionNew(["A", "B"])


class UserCollectionNew2(UserCollection):
    """定义了__len__方法就可以用于真值测试 if users_new 是有意义的 对比users则一直为真，不论items是否为空
    同 __bool__ 方法，如果两个都定义，bool方法优先
    """
    def __init__(self, users) -> None:
        super().__init__(users)
    
    def __len__(self):
        return len(self.items)
    
    def __bool__(self):
        return len(self.items) == 0


users_new1 = UserCollectionNew2(["A", "B"])


class EquealWithAnything:
    """与任何对象相等"""
    def __eq__(self, __o: object) -> bool:
        """== 是用此魔法方法判断值，is是判断id()
        True, False, None是单例，所以判断时需要用is
        其他对象并不是严格单例，即使值一样但内存地址是不同的
        但为了省内存(又叫整型驻留)对 -5～256 这些整数python是一直放内存的
          使用时直接返回其对象（不会创建新的对象），所以对这些整数用is判等仍然会返回True
        """
        return True


movies = [
    {"name": "The Dark Knight", "year": 2008, "rating": "9"},
    {"name": "Kaili Blues", "year": 2015, "rating": "7.3"},
]


class Movie:
    """电影对象数据类"""

    def __init__(self, name, year, rating) -> None:
        self.name = name
        self.year = year
        self.rating = rating
    
    @property
    def rank(self):
        rating_num = float(self.rating)
        if rating_num >= 8.5:
            return "S"
        elif rating_num >= 8:
            return "A"
        elif rating_num >= 7:
            return "B"
        elif rating_num >= 6:
            return "C"
        else:
            return "D"

    @property
    def rank_new(self):
        # bisect 二分查找只可查排序好的
        breakpoints = (6, 7, 8, 8.5)
        grades = ("D", "C", "B", "A", "S")
        index = bisect.bisect(breakpoints, float(self.rating))
        return grades[index]

# 德摩根定律：not A or not B  等价于 not (A and B)

def all_numbers_bt_10(numbers):
    """判断序列所有数字都大于10"""
    return bool(numbers) and all(n > 10 for n in numbers)

# or 短路求值 True or (1 / 0)
context = {}
extra_context = None
if extra_context:
    context.update(extra_context)

# 短路求值 即 a or b or c... 这样的表达式，会返回变量中第一个布尔值为真的对象，直到最后
# 所以以下表达式如果extra_context为None 会变为update({}) 不会报错
context.update(extra_context or {})


class DummyContext:
    def __init__(self, name) -> None:
        self.name = name

    def __enter__(self):
        # __enter__会在进入管理器时被调用，同时可以返回结果
        # 此处返回一个增加了随机后缀的name
        return f"{self.name}-{random.random()}"

    def __exit__(self, exc_type, exc_value, traceback):
        # __exit__会在退出管理器时被调用, 入参固定，当没有任何异常时三个参数都为None
        # exc_type   异常的类型
        # exc_value  异常对象
        # traceback  错误的堆栈对象
        # 异常时程序的行为取决于此方法返回值：
        #   返回True,  异常会被当前with语句压制住，不再继续抛出，达到“忽略异常”的效果；
        #   返回False, 异常会被正常抛出，交由调用方处理
        print("Exiting DummyContext")
        return True

def t3():
    with DummyContext("foo") as name:
        print(f"in dummycontext")
        raise("test Exception!")
        print(f"Name: {name}")


class NumberInput(BaseModel):
    # 使用类型注解 conint 定义 number 属性的取值范围
    number: conint(ge=0, le=100)

def input_a_number_with_pydantic():
    while True:
        number = input("Please input a number(0-100): ")
        # 实例化为pydantic模型，捕获校验错误异常
        try:
            number_input = NumberInput(number=number)
        except ValidationError as e:
            print(e)
            continue

        number = number_input.number
        break
    print(f"Your number is {number}")


# 元类，一种特殊的类
# 类可以控制实例的创建过程
# # 元类可以控制类的创建过程
# _validators = {}

# class ValidatorMeta(type):
#     """元类：统一注册所有校验器类，方便后续使用"""

#     def __new__(cls, name, bases, attrs):
#         ret = super().__new__(cls, name, bases, attrs)
#         print((f"new class\n  name: {name} type: {type(name)}\n"
#                f"  bases: {bases} type: {type(bases)}\n"
#                f"  attrs:{attrs} type: {type(attrs)}\n"))
#         _validators[attrs["name"]] = ret
#         return ret


# class StringValidator(metaclass=ValidatorMeta):
#     name = "string"


# class IntegerValidator(metaclass=ValidatorMeta):
#     name = "int"


# 装饰器模式（与python装饰器不是一个东西！）
#    设计一个统一的接口
#    编写多个符合该接口的装饰器类，每个类只实现一个简单的功能
#    通过组合的方式嵌套使用这些装饰器类
#    通过类之间的层层包装来实现复杂的功能
class Numbers:
    """ 一个包含多个数字的简单类 """
    
    def __init__(self, numbers):
        self.numbers = numbers

    def get(self):
        return self.numbers


class EvenOnlyDecorator:
    """ 装饰器类：过滤所有偶数 """

    def __init__(self, decorated):
        self.decorated = decorated

    def get(self):
        return [num for num in self.decorated.get() if num % 2 == 0]


class GreaterThanDecorator:
    """ 装饰器类：过滤大于某个数的数 """

    def __init__(self, decorated, min_value):
        self.decorated = decorated
        self.min_value = min_value

    def get(self):
        return [num for num in self.decorated.get() if num > self.min_value]


def t5():
    obj = Numbers([42, 12, 3, 25, 22, 82, 73])
    even_obj = EvenOnlyDecorator(obj)
    print(even_obj.get())
    gt_obj = GreaterThanDecorator(even_obj, min_value=30)
    print(gt_obj.get())


class Robot:
    def __init__(self, name, age):
        self.name = name
        self.age = age
    
    def __str__(self) -> str:
        return f"Robot<{self.name}:{self.age}>"
    
    def __setattr__(self, __name: str, __value: int) -> None:
        if __name == "age":
            if __value > 90:
                raise ValueError("Robot Age Must LT 90!")
        super().__setattr__(__name, __value)


def t6():
    a = Robot("A", 30)
    print(a)
    a.__dict__.update(dict(
        age=100,
        name="B"
    ))
    print(a)
    a.age = 100


class InfoDumperMixin:
    """ 输出当前实例信息 """

    def dump_info(self):
        d = self.__dict__
        print(f"Number of members: {len(d)}")
        print("Details:")
        for k, v in d.items():
            print(f" - {k}: {v}")


class Person(InfoDumperMixin):
    def __init__(self, name, age):
        self.name = name
        self.age = age


def t7():
    p = Person("jack", 20)
    p.dump_info()


class Validator:
    """ 校验器基类：统一注册所有校验器类，方便后续使用 """
    _validators = {}

    def __init_subclass__(cls, **kwargs):
        print(f"{cls.__name__} registered, extra kwargs: {kwargs}")
        Validator._validators[cls.__name__] = cls


class StringValidator(Validator, foo="bar"):
    name = "string"


class IntegerValidator(Validator):
    name = "int"


def t8():
    print(Validator._validators)



if __name__ == "__main__":
    print("................ZEN STARTING...................")
    t8()
    print("...................THE END.....................")
