# *-* coding:utf-8 *-*

class Text(str):
    def duplicate(self):
        print(self)
        return self + self

text = Text("Python")
print(text.duplicate())

class TrackableList(list):
    def append(self,object):
        print("append called")
        super().append(object)

track = TrackableList()
track.append(1)

for i in track:
    print(i)