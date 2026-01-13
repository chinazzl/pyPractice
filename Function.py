# -*- coding: utf-8 -*-

'''
 传递可变化参数
'''
def multipleArgs(*args):
    """
    接受可变数量的参数
    :param args: 可变参数
    :return: 参数列表
    """
    return args

args = multipleArgs(1,'a')
print(args)

message = "a"

def pythonScope():
    """
    演示Python作用域
    :return: None
    """
    # global message
    message = "b"
    print("message in function:", message)

pythonScope()
print("message in global:", message)

def listTest():
    chars = list('Hello world')
    print(chars)
    for c in chars:
        print(type(c) == chr);

if __name__ == '__main__':
    listTest()
    # 直接运行时才会执行
    print("This is a test for function.py")