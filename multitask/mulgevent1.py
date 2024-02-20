import os, sys
import gevent
from gevent import monkey

monkey.patch_all()


def f(n):
    [print(gevent.getcurrent(), i) for i in range(n)]
    gevent.sleep()


g1 = gevent.spawn(f, 5)
g2 = gevent.spawn(f, 6)
g3 = gevent.spawn(f, 7)

print(g1)
print(g2)
print(g3)

# gevent.joinall([g1, g2, g3])
gevent.joinall([g1])