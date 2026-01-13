# -*- coding: utf-8 -*-

class TagCloud:

    def __init__(self):
        self.tags = {}
        # 私有变量
        self.__private = {}

    def add(self,tag):
        self.tags[tag] = self.tags.get(tag,0) + 1

    def __getItem__(self,tag):
        return self.tags.get(tag.lower(),0)

    def __setItem__(self,tag,count):
        self.tags[tag.lower()] = count

cloud = TagCloud()
cloud.add("python")
cloud.add("python")
print(cloud.tags)

item = cloud.__getItem__("Python")
print(item)

print(cloud.__dict__) # {'tags': {'python': 2}, '_TagCloud__private': {}}

 # print(cloud.__private)  Error AttributeError: 'TagCloud' object has no attribute '__private'

print(cloud._TagCloud__private) #  {}