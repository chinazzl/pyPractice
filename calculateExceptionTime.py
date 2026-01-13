# -*- coding: utf-8 -*-
# 比较两种处理异常的性能，直接使用raise进行抛异常的性能要小，可以直接返回一个错误的变量然后在外侧进行判断有更好的性能
from timeit import timeit

code1 = """

def calculate_xfactor(age):
    if age <= 0:
        raise ValueError("You should not enter 0 or less.")
    return 10 /age

try:
    calculate_xfactor(-1)
except Exception as e:
    pass
"""

code2 = """

def calculate_xfactor(age):
    if age <= 0:
        return None
    return 10 /age

xfactor = calculate_xfactor(-1)
if xfactor == None:
    pass
"""
print("code1 is first=",timeit(code1,number=10000))
print("code2 is second=",timeit(code2,number=10000))
