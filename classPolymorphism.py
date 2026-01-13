# *-* coding: utf-8 *-*
from abc import ABC,abstractmethod

class UIControl(ABC):
    def __init__(self):
        print("abstract class init")

    @abstractmethod
    def draw(self):
        pass

class TextBox(UIControl):
    def draw(self):
        print("TextBox")

class DropDownList(UIControl):
    def draw(self):
        print("DropDownList")

def draw(controls):
    # control.draw()
    for control in controls:
        control.draw()

ddl = DropDownList()
textBox = TextBox()
draw([ddl,textBox])
