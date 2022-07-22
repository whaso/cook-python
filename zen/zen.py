import timeit
from enum import Enum
from textwrap import dedent
from typing import NamedTuple

from jinja2 import Template


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


class Address(NamedTuple):
    country: str
    province: str
    city: str

addr = Address("道外区", "黑龙江", "哈尔滨")

if __name__ == "__main__":
    t = t2
    t()
