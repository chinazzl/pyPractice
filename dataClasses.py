# *-* coding:utf-8 *-*
from collections import namedtuple

point = namedtuple("point",['x','y'])
p1 = point(x=1,y=2)
p2 = point(x=1,y=2)
print(p1 == p2)