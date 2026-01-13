# -*- coding:utf-8 -*-

from pathlib import Path
from zipfile import ZipFile
# 将一个文件进行压缩成zip格式
# with ZipFile("file.zip","w") as zip:
#     for p in Path("../economy").rglob("*.*"):
#         zip.write(p)
# 读取
with ZipFile("file.zip","r") as zip:
   print(zip.namelist())
   info = zip.getinfo("../economy/__init__.py")
   print(info.file_size)
   print(info.compress_size)
   zip.extractall("extract")
 

