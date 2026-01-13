# -*- coding: utf-8 -*-

import math
import random
"""
练习：
1. 寻找水仙花数。

说明：水仙花数也被称为超完全数字不变数、自恋数、自幂数、阿姆斯特朗数，它是一个3位数，
该数字每个位上数字的立方之和正好等于它本身，例如：$1^3 + 5^3+ 3^3=153$
"""
def find_armstrong_numbers(num):
    # 135 
    low = num % 10;
    mid = (num % 100) //10;
    high = num // 100;
    # 计算每位数字的立方和
    sum_of_cubes = low ** 3 + mid ** 3 + high ** 3
    # 检查立方和是否等于原数
    if sum_of_cubes == num:
        print(f"三位数为 {num} 是水仙花数")


def is_armstrong_number(num):
    # 将数字转换为字符串以便逐位处理
    str_num = str(num)
    # 计算每位数字的立方和
    sum_of_cubes = sum(int(digit) ** 3 for digit in str_num)
    # 检查立方和是否等于原数
    return sum_of_cubes == num


"""
公鸡5元一只，母鸡3元一只，小鸡1元三只，用100块钱买一百只鸡，问公鸡、母鸡、小鸡各有多少只？
公鸡的范围 0-20
母鸡的范围 0-33
"""

def find_chickens():
    # 公鸡的范围
    for rooster in range(0, 21):
        # 母鸡的范围
        for hen in range(0,34):
            # 小鸡的数量
            chicken = 100 -rooster - hen
            money = rooster * 5 + hen * 3 + chicken //3
            if money == 100 and chicken % 3 ==0:
                print(f"公鸡：{rooster}只，母鸡：{hen}只，小鸡：{chicken}只")

"""
找出10000以内的完美数。

说明：完美数又称为完全数或完备数，它的所有的真因子（即除了自身以外的因子）的和（即因子函数）恰好等于它本身。
例如：6（$6=1+2+3$）和28（$28=1+2+4+7+14$）就是完美数。完美数有很多神奇的特性，有兴趣的可以自行了解。
"""
def find_perfect_numbers():
    for i in range(1, 10001):
        perfect_num = 0
        for j in range(1,i):
            if i % j == 0:
                perfect_num += j;
        if perfect_num == i:
            print(f"{i} 是完美数")

'''
打印九九乘法表
'''
def print_multiplication_table():
    for i in range(1,10):
        for j in range(1, i+1):
            print(f"{i} x {j} ={i * j:2d}", end="\t")
        print("\n")  # 换行        


"""
三角形
    * -- 4 spaces 1 star
   *** -- 3 spaces 3 stars
  ***** -- 2 spaces 5 stars
 ******* -- 1 space 7 stars
********* -- 0 spaces 9 stars
"""
def print_triangle(num):
    for i in range(1, num + 1):
        # print spaces
        print(" " * (num - i))
        # print stars
        print("*" * (2 * i - 1));

def print_triangle2(num):
    for i in range(num):
        for j in range(num -i -1):
            print(" ", end="")
        for k in range(2 * i + 1):
            print("*", end="")
        print()

def play_CRAPS(money):
    while money > 0:
        bet = int(input(f"你有 {money} 元，输入你的赌注："))
        if bet > money:
            print("赌注不能超过你的钱。")
            continue
        point = random.randint(1, 6) + random.randint(1, 6)
        print(f"点数是 {point}")
        if point in (7, 11):
            money += bet
            print(f"你赢了！现在你有 {money} 元。")
        elif point in (2, 3, 12):
            money -= bet
            print(f"你输了！现在你有 {money} 元。")
        else:
            while True:
                new_point = random.randint(1, 6) + random.randint(1, 6)
                print(f"新的点数是 {new_point}")
                if new_point == point:
                    money += bet
                    print(f"你赢了！现在你有 {money} 元。")
                    break
                elif new_point == 7:
                    money -= bet
                    print(f"你输了！现在你有 {money} 元。")
                    break 

if __name__ == "__main__":
    print_triangle2(5)