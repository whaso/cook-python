import io, sys, inspect
import timeit
import bisect
import random
from enum import Enum
from urllib import parse
from textwrap import dedent
# from contextlib import contextmanager
from typing import Iterable, TextIO, List, Optional, NamedTuple, Dict
from abc import ABC, abstractmethod, ABCMeta
from collections import Counter

import requests
from lxml import etree
from jinja2 import Template
# from requests.exceptions import RequestException
from pydantic import BaseModel, conint, ValidationError
from flask_sqlalchemy import Model



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


"""
SOLID设计原则
    S: single responsibility principle(SRP, 单一职责原则) 一个类只应该有一种被修改的原因
    O: open-closed principle (OCP, 开放关闭原则) 类应该对扩展开放，对修改封闭
    L: Liskov substitution principle (LSP, 里式替换原则)
    I: interface segregation principle (ISP, 接口隔离原则)
    D: dependency inversion principle (DIP, 依赖倒置原则)
"""


class Post:
    """Hacker News 上的条目

    :param title: 标题
    :param link: 链接
    :param points: 当前得分
    :param comments_cnt: 评论数
    """

    def __init__(self, title: str, link: str, points: str, comments_cnt: str):
        self.title = title
        self.link = link
        self.points = int(points)
        self.comments_cnt = int(comments_cnt)



class PostFilter(ABC):
    """抽象类：定义如何过滤帖子结果"""

    @abstractmethod
    def validate(self, post: Post) -> bool:
        """判断帖子是否应该保存"""


class DefaultPostFilter(PostFilter):
    """保留所有帖子"""

    def validate(self, post: Post) -> bool:
        return True


class GithubPostFilter(PostFilter):
    def validate(self, post: Post) -> bool:
        parsed_link = parse.urlparse(post.link)
        return parsed_link.netloc == "github.com"


class HNTopPostsSpider:
    """抓取 Hacker News Top 内容条目

    :param fp: 存储抓取结果的目标文件对象
    :param limit: 限制条目数，默认为 5
    """

    items_url = "https://news.ycombinator.com/"
    file_title = "Top news on HN"

    def __init__(self, limit: int = 5, filter_by_hosts: Optional[List[str]] = None):
        # self.fp = fp
        self.limit = limit
        # self.post_filter = post_filter or DefaultPostFilter()
        self.filter_by_hosts = filter_by_hosts

    # def write_to_file(self):
    #     """以纯文本格式将 Hacker News Top 内容写入文件"""
    #     self.fp.write(f"#{self.file_title}\n\n")
    #     for i, post in enumerate(self.fetch(), 1):  # enumerate()接收第二个参数，表示从这个数开始计数，默认i是0
    #         self.fp.write(f"> TOP {i}: {post.title}\n")
    #         self.fp.write(f"> 分数：{post.points} 评论数：{post.comments_cnt}\n")
    #         self.fp.write(f"> 地址：{post.link}\n")

    def fetch(self) -> Iterable[Post]:
        """从Hacker News 抓取Top内容

        Returns:
            []: 可迭代Post对象
        """
        proxies = {
            "http": "http://127.0.0.1:7890",
            "https": "http://127.0.0.1:7890",
        }
        proxy_rules = [
            "news.ycombinator.com",
        ]
        use_proxy = False
        for i in proxy_rules:
            if i in self.items_url:
                use_proxy = True
        resp = requests.get(self.items_url, proxies=proxies if use_proxy else {})
        # 使用XPath解析页面内容
        html = etree.HTML(resp.text)
        items = html.xpath("//table/tr[@class='athing']")
        counter = 0
        for item in items:
            if counter >= self.limit:
                break
            node_title = item.xpath("./td[@class='title'][last()]/span/a")[0]
            node_detail = item.getnext()
            points_text = node_detail.xpath("./td[last()]/span/span[@class='score']/text()")[0]
            comments_text = node_detail.xpath("./td[last()]/span/a[last()]/text()")[0]
            post = Post(title=node_title.text,
                        link=node_title.get("href"),
                        points=points_text[0].split()[0] if points_text else "0",
                        comments_cnt=comments_text.split()[0])
            # if self.post_filter.validate(post):
            if self._check_link_from_hosts(post.link):
                counter += 1
                yield post

    def _check_link_from_hosts(self, link: str) -> bool:
        """检查某链接是否属于所定义的站点"""
        if self.filter_by_hosts is None:
            return True

        parsed_link = parse.urlparse(link)
        return parsed_link.netloc in self.filter_by_hosts


def t9():
    crawler = HNTopPostsSpider(sys.stdout)
    crawler.write_to_file()


class PostsWriter:
    """负责将帖子列表写入文件"""

    def __init__(self, fp: io.TextIOBase, title: str) -> None:
        self.fp = fp
        self.title = title

    def write(self, posts: List[Post]):
        self.fp.write(f"#{self.title}\n\n")
        for i, post in enumerate(posts, 1):
            self.fp.write(f"> TOP {i}: {post.title}\n")
            self.fp.write(f"> 分数：{post.points} 评论数：{post.comments_cnt}\n")
            self.fp.write(f"> 地址：{post.link}\n")
            self.fp.write("---------\n")


def t10(fp: Optional[TextIO] = None):
    """获取 Hacker News Top 内容，并将其写入文件中

    :param fp: 需要写入的文件，如未提供，将向标准输出打印
    """
    dest_fp = fp or sys.stdout
    crawler = HNTopPostsSpider()
    writer = PostsWriter(dest_fp, title="Top news on HN")
    writer.write(list(crawler.fetch()))


"""
SOLID设计原则
    L: Liskov substitution principle (LSP, 里式替换原则)
        - 所有子类（派生类）对象应该可以任意替代父类（基类）对象使用，且不会破坏程序原本的功能。
"""


class DeactivationNotSupported(Exception):
    """当用户不支持停用时抛出"""


class User(Model):
    """用户类，包含普通用户的相关操作"""
    def deactivate(self):
        """停用当前用户
        :raises: 当用户不支持停用时，抛出异常
        """
        self.is_active = False
        self.save()


class Admin(User):
    def deactivate(self):
        raise DeactivationNotSupported("admin can not be deactivated")


"""
SOLID设计原则
    I: interface segregation principle (ISP, 接口隔离原则)
    D: dependency inversion principle (DIP, 依赖倒置原则)
    - 高层模块不应该依赖低层模块，二者都应该依赖抽象
"""


class SiteSourceGrouper:
    """对Hacker News 新闻来源站点进行分组统计

    :param url: Hacker News 首页地址
    """

    def __init__(self, url: str):
        self.url = url

    def get_groups(self) -> Dict[str, int]:
        """获取（域名，个数）分组"""
        groups = Counter()
        for i in range(1, 5):
            resp = requests.get(self.url + f"?p={i}", proxies={
                "http": "http://127.0.0.1:7890",
                "https": "http://127.0.0.1:7890",
            })
            html = etree.HTML(resp.text)
            # 通过xpath语法筛选新闻域名标签
            # elems = html.xpath("//table/tr[@class='athing']/td[@class='title'][last()]/span[@class='titleline']/span/a/span/text()")
            elems = html.xpath("//span[@class='sitebit comhead']/a/span")
            for elem in elems:
                groups.update([elem.text])
        return groups


def t11():
    groups = SiteSourceGrouper("https://news.ycombinator.com/").get_groups()
    # 打印最常见的 3 个域名
    for key, value in groups.most_common(3):
        print(f"Site: {key} | Count: {value}")


def t12():
    def f1():
        f2(1, 2, 3, 4, e=5)

    def f2(a, b, c, d, *, e, **kw):
        f = 6
        g = 7
        f3()

    def f3():
        # 栈帧
        frame = inspect.currentframe().f_back
        f_locals = frame.f_locals  # 名字空间 包含 f g f3
        code = frame.f_code  # 代码对象
        arg_count = code.co_argcount + code.co_kwonlyargcount  # 参数个数
        if code.co_flags & 0x04:  # *args
            arg_count += 1
        if code.co_flags & 0x08:  # **kwargs
            arg_count += 1
        params = code.co_varnames[: arg_count]
        print(
            {p: f_locals[p] for p in params}
        )
    f1()  # {'a': 1, 'b': 2, 'c': 3, 'd': 4, 'e': 5, 'kw': {}}


# def test_grouper_returning_valid_type():
#     """测试 get_groups 是否返回了正确类型"""
#     grouper = SiteSourceGrouper("https://news.ycombinator.com/")
#     result = grouper.get_groups()
#     assert isinstance(result, Counter), "groups should be Counter instance"

from unittest import mock


@mock.patch("requests.get")
def test_grouper_returning_valid_type(mocked_get):
    """测试 get_groups 是否返回了正确类型"""
    with open("./zen/hn.html", "r") as fp:
        mocked_get.return_value.text = fp.read()

    grouper = SiteSourceGrouper("https://news.ycombinator.com/")
    result = grouper.get_groups()
    assert isinstance(result, Counter), "groups should be Counter instance"
    for key, value in result.most_common(3):
        print(f"Site: {key} | Count: {value}")


class HNWebPage(metaclass=ABCMeta):
    """抽象类：Hacker News 站点页面"""

    @abstractmethod
    def get_text(self) -> str:
        raise NotImplementedError


class RemoteHNWebPage(HNWebPage):
    """远程页面，通过请示 HN 站点返回内容"""

    def __init__(self, url: str) -> None:
        self.url = url

    def get_text(self) -> str:
        resp = requests.get(self.url)
        return resp.text


class SiteSourceGrouper:
    """对HN页面新闻来源站点进行分组统计"""

    def __init__(self, page: HNWebPage) -> None:
        self.page = page

    def get_groups(self) -> Dict[str, int]:
        """获取（域名，个数）分组"""
        html = etree.HTML(self.page.get_text())
        # 通过 xpath 语法筛选新闻域名标签
        elems = html.xpath("//table[@class='itemlist']//span[@class='sitestr']")

        groups = Counter()
        for e in elems:
            groups.update([e.text])
        return groups


class LocalHNWebPage(HNWebPage):
    """本地页面"""

    def __init__(self, path: str) -> None:
        self.path = path

    def get_text(self) -> str:
        with open(self.path, "r") as fp:
            return fp.read()


def test_grouper_from_local():
    page = LocalHNWebPage(path="./static_hn.html")
    grouper = SiteSourceGrouper(page)
    result = grouper.get_groups()
    assert isinstance(result, Counter), "groups should be Counter instance"


class A:
    def __init__(self, a) -> None:
        self.a = a
        print(f"A: {a}")


if __name__ == "__main__":
    print("................ZEN STARTING...................")
    # test_grouper_returning_valid_type()
    print("...................THE END.....................")
