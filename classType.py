# -*- coding: utf-8 -*-

class Point :
    # 所有类属性进行共享
    default_color = "red"
# 构造函数，self- 对象本身，x、y传入的参数
    def __init__(self,x,y):
        self.x = x
        self.y = y

    def draw(self):
        print("draw=",self)

    def setName(self,name):
        print("setName=",name)

Point.default_color = "yellow"
point = Point(1,2)
print(point.default_color)
print(Point.default_color)
point.draw();

point = Point(3,4)
print(point.default_color)
print(Point.default_color)
point.draw();
