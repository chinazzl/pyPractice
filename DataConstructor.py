# -*- coding: utf-8 -*-

from collections import deque

numbers = list(range(0,5))

print(numbers[-1])

print("----------")
numbers = [1,2,3,4,5,5,5,6]
first, second, *rest,last = numbers
print(first, second, rest,last)

print("----------")

letters = ['a', 'b', 'c', 'd', 'e']
for index,letter in enumerate(letters):
    # print(letter[0], letter[1])
    print(index, letter)

print("----------")

# Add
letters.insert(0, 'z')
letters.append('f')
# Remove
popItem = letters.pop(0)
print(popItem)
removeItem = letters.remove('f') # None
print(removeItem)
del letters[0:9]  # 删除第一个元素
print(letters)

print("----------")

# Sort
numbers = [2,1,5,6,3]
# 反转
# numbers = numbers[::-1]
# numbers.sort()  # 升序
# numbers.sort(reverse=True)  # 降序
sortedList = sorted(numbers)
print(numbers)
print(sortedList)
numbers = [
    ("item1", 2),
    ("item2", 1),
    ("item3", 5),
    ("item4", 4),
    ("item5", 3)
]
def sorted_Item(num):
    return num[1]
# numbers.sort(key= sorted_Item)
#  lambda
numbers.sort(key= lambda item:item[1])
print(numbers)

print("--------")

items = [
    ("item1", 2),
    ("item2", 1),
    ("item3", 5),
    ("item4", 4),
    ("item5", 3)
]

prices = map(lambda item:item[1],items)
prices = list(prices)
print(prices)
# filtered = filter(lambda item:item[1] > 2,items)
# filtered = list(filtered)
# print(filtered)
filtered = [item[1] for item in items if item[1] > 2]
print(filtered)

print("--------")
# zip
list1 = [1,2,3,6]
list2 = [4,5,6]
print(zip(list1, list2))  # [(1, 4), (2, 5), (3, 6)]
print(list(zip("abcd",list1, list2))) 
print("--------")

browser_session = [1]
browser_session.pop()
if not browser_session:
    print("browser_session is empty")

print("--------")

queue = deque([])
queue.append(1)
queue.append(2)
queue.append(3)
print(queue)
queue.popleft()
print(queue)

print("--------")
point = (1, 2)
print(type(point))
# 元组不可变，设置后无法进行修改
# point[0] = 10
if 10 in point:
    print("10 in point")
point = point + (3, 4)  # 创建一个新的元组
print(point)
print(point[0:2])

print("--------")
# swap
x = 1
y = 2
x, y = y, x  # 交换
x,y = (y,x)
print(x, y)
a,b=[1,2]
print(type(a), type(b))

print("--------")
# set
numbers = [1,2,1,1,3,4]
first = set(numbers)  # 去重
print(first)
second = {1,2,5}
print(first | second)  # 并集
print(first & second)  # 交集
print(first - second)  # 差集
print(first ^ second)  # 对称差集 属于A但不属于B的元素 + 属于B但不属于A的元素。

print("--------")
# dict
point = {"x":1,"y":2}
print(point)
point = dict(x=1, y=2)  # 创建字典
print(point)
point["z"] = 3  # 添加键值对
print(point)
if "a" in point:
    print("a in point")
del point["x"]  # 删除键值对
print(point)
point.keys()  # 获取所有键
point.values()  # 获取所有值
point.items()  # 获取所有键值对
point.get("x", 0)  # 获取键的值，如果不存在则返回默认值0
point.setdefault("a", 0)  # 如果键不存在则添加键值对
point.clear()  # 清空字典
for key,value in point.items():
    print(key, value)  # 遍历键值对

print("--------")
# 字典推导式
numbers = [1,2,3,4,5]
squares = {number:number**2 for number in numbers}
print(squares)  # {1: 1, 2: 4, 3: 9, 4: 16, 5: 25}  
squares = {number + 1:number**2 for number in numbers}
print(squares)  # {2: 1, 3: 4, 4: 9, 5: 16, 6: 25}
values = (x * 2 for x in range(5))
"""
核心优势：节省内存！
想象一下，如果你的 range 不是 5，而是十亿 (1_000_000_000)。
列表：[x * 2 for x in range(1_000_000_000)]
Python 会尝试在内存中创建包含十亿个整数的列表。这几乎肯定会让你的电脑内存耗尽而崩溃。
生成器：(x * 2 for x in range(1_000_000_000))
它几乎不占用内存，因为它只存储了生成规则。只有当你用 for 循环去请求值时，它才会一个一个地计算，用完就丢，不会把所有值都保存在内存里。

正确的理解：生成器存储的是“状态”，而不是“结果”
让我们把生成器想象成一个微型、懒惰的工厂，而不是一个装满货物的仓库（列表就是仓库）。
当你创建生成器时：
values = (x * 2 for x in range(5))
你并没有生产出任何产品（0, 2, 4, 6, 8）。你只是建造了这座工厂，并给了它一套生产说明书。
这个 values 生成器对象，它在内存中存储的不是最终的数值，而是以下三样东西，也就是它的状态 (State)：
指令 (Instruction): 它知道要执行的操作是 x * 2。
数据源 (Data Source): 它知道要从哪里取原材料，也就是 range(5) 这个可迭代对象。
位置指针 (Position Pointer): 它知道上一次生产到了哪里。刚创建时，它指向数据源的最开始。
"""
print(values)  # <generator object <genexpr> at 0x...>
for value in values:
    print(value)  # 0, 2, 4, 6, 8

print(values) # [] 因为生成器已经用完，用完了就直接丢弃
values = (x * 2 for x in range(5))
# print(len(values)) # TypeError: object of type 'generator' has no len()

print("--------")
# unpacking
"""
* (Iterable Unpacking / 解包)
概念：它不是一个连接操作，而是“把容器打开，将其中的所有元素一个个取出来，放到当前位置”的操作。它可以作用于任何可迭代对象（list, tuple, set, range, generator, string...）。
灵活性：它极其灵活，因为你可以在一个新的列表（或元组、集合）字面量中的任何位置进行解包，并且可以混合普通元素和其他解包。
"""
values = [1, 2, 3, 4, 5]
values2 = [6,7]
v3 = values + values2
print(v3)  # [1, 2, 3, 4,
v4 = [*values, *values2]  # 使用 * 进行解包
print(v4)  # [1, 2, 3, 4,
tuple1 = (5,6,7)
v5 = [*values,*tuple1]
print(v5)  # [1, 2, 3, 4, 5, 6, 7]

"""
总结：* vs ** 对于字典
操作符	名称	                        对字典做什么	    主要用途	         示例
*	| 单星号解包(Iterable Unpacking)|    解包出键 (Keys)|  创建包含字典键的列表、元组、集合	my_set = {*my_dict}
**	双星号解包 (Dictionary Unpacking)|   解包出键值对 (Key-Value Pairs)	| 创建或合并字典	new_dict = {**dict1, **dict2}
"""
first = {"x":1}
second = {"y":2}
combined = {**first,**second}
print(combined) 

print("--------")
# Excercise: 使用解包和生成器
from pprint import pprint
sentence = "Hello, my name is John Doe. I am a software developer."
char_frequency = {}
for char in sentence:
    if char in char_frequency:
        char_frequency[char] += 1
    else:
        char_frequency[char] = 1
# pprint(char_frequency)
char_frequency = sorted(char_frequency.items(),
                        key=lambda kv: kv[1])
pprint(char_frequency)