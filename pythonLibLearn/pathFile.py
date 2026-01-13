# -*- coding:utf-8 -*-

from pathlib import Path
from time import ctime
import shutil

# Path()指当前目录的路径
path = Path("../economy/__init__.py")
# 统计当前文件/文件夹的大小、创建时间、修改时间等信息 
# Mon Jul 21 22:34:44 2025
print(ctime(path.stat().st_ctime))
print(path.read_text())

target = Path() / "__init__.py"
# 拷贝文件
shutil.copy(path,target)
