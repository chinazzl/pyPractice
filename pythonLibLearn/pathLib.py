# -*- coding:utf-8 -*-

from pathlib import Path
# Path()指当前目录的路径
path = Path("../economy")
print(path)
print(path.is_dir())
print(path.exists())
print(path.suffix)
print(path.parent)

# ======文件夹操作=====
# path.mkdir()
# path.rmdir()
# path.rename("../ecnomy")
# path.rename("../economy/aa.txt")

paths = [p for p in path.iterdir() if p.is_dir()]
print(paths)

# rglob属于递归搜索，glob属于查询当前文件夹下的文件，如果想要递归搜索需要glob("**/*.pyc")
pyc_files = [p for p in path.rglob("*.pyc")]
print(pyc_files)
