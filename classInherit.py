# *-* coding:utf-8 *-*

from abc import ABC, abstractmethod,abstractstaticmethod
class Animal:
    def eat(self):
        print("eat")

    @abstractmethod
    def age (slef):
        pass

# 继承Animal
class Mammal(Animal):

    def sleep(self):
        print("Mammal sleep")

    def walk(self):
        print("walk")

    def run(self):
        pass

class Fish(Animal):

    def sleep(self):
        print("fish sleep")

    def swim(self):
        print("swim")

mammal = Mammal()
mammal.eat()

print(isinstance(mammal,Animal))
print(isinstance(mammal,Fish))

obj = object()
print(issubclass(Animal,object))

print("------")

class SuperDog(Mammal,Fish):
    pass

dog = SuperDog()
dog.sleep()

print("--------")

class Cat(Animal):

    def age(self):
        print(2)

    def sleep(self):
        print("cat sleep")

cat = Cat()
cat.age()
