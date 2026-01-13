# -*- coding=:utf-8 -*-

class Point:

    default_color = "red"

    def __init__(self,x,y):
        self.x = x
        self.y = y

    def draw(self):
        print("draw")

    @classmethod
    def orignal(cls):
        return cls(0,0)

    @classmethod
    def circle(cls):
        return cls(3.14,3.14)

    def printPoint(self):
        print(f"Point= {self.x},{self.y}")


point1 = Point.orignal()
point1.printPoint()
point2 = Point.circle()
point2.printPoint()
