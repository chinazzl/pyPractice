import pandas as pd
import numpy as np

df = pd.read_csv("resources/diabetes.csv")
# 前五条
# print(df.head(0).columns)
columns = df.head(0).columns
for column in columns:
    # 将0替换为NaN
    df[column].replace(0,np.nan)
    count = (df[column] == 0).sum()
    print(f"{column},{count} 个")
# 查看数据概况
print(df.isnull().sum())
print("-"*20)
print(df.info())