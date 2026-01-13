# -*- coding: utf-8 -*-

file = None
try:
    # 类似java的try-resource
    with open("计量计费.md") as file:
        print("file is open")
    age = int(input("please enter your age:"))
except (ValueError,ZeroDivisionError) as e:
    print("You enter a wrong age ")
    print(e)
else:
    print("你输入的没有异常")
    print(file.closed)
print("即将执行其他程序es")


def calculate_xfactor(age):
    if age <= 0:
        raise ValueError("Age cannot be 0 or less")
    return 10/age

try:
    calculate_xfactor(-1)
except Exception as e:
    print(e)
