# -*- coding: utf-8 -*-

class Point:

    def __init__(self,x,y):
        self.x = x
        self.y = y

    def __str__(self):
        return f"Point={self.x},{self.y}"

    def __eq__(self,other):
        return self.x == other.x and self.y == other.y

    def __lt__(self,other):
        return self.x < other.x and self.y < other.y

    def __gt__(self,other):
        return self.x > other.x and self.y > other.y


point = Point(1,2)
print(point)
point1 = Point(1,2)
print(point == point1)
point2 = Point(3,5)
print(point < point2)
