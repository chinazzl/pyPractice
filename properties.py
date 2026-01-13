# *-* coding: utf-8 *-*
"""
Python 中的 Properties 是一种优雅的方式来管理类的属性访问，让你可以像访问普通属性一样调用方法。
基本概念
Properties 允许你：

将方法调用伪装成属性访问
在获取或设置属性时执行额外的逻辑
保持简洁的接口，同时提供灵活的内部实现
"""
class Product:

    def __init__(self,price):
        # self.setPrice(price)
        self.price = price

# 将getPrice设置为装饰器
    @property
    def price(self):
        return self.__price

    @price.setter
    def price(self,value):
        if value < 0:
            raise ValueError("the price can not negative")
        self.__price = value

    # 调用property方法
    # price = property(getPrice,setPrice)

product = Product(10)
print(product.price)
