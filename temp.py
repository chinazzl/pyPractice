# -*- coding: utf-8 -*-

def foreach():
    for i in range(5):
        print(i)

def inceament(num,step,another=1):
    """
    增加数字
    :param num: 数字
    :param step: 步长
    :param another: 另一个参数
    :return: 增加后的数字
    """
    return num + step + another

print(inceament(1,2))
