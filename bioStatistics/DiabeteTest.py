import pandas as pd
import numpy as np

df = pd.read_csv("resources/diabetes.csv")
# 前五条
# print(df.head(0).columns)
columns = df.head(0).columns
for column in columns:
    # 将0替换为NaN
    df[column] = df[column].replace(0,np.nan)
    count = (df[column] == 0).sum()
    print(f"{column},{count} 个")
# 查看数据概况
print(df.isnull().sum())
print("-"*20)
# 使用中位数进行填充
# fillna 相当于Optional.orElse
for col in columns:
    median_val = df[col].median()
    # inplace = True代表直接修改原对象
    df[col] = df[col].fillna(median_val)
print("清洗数据完成")
print(df.isnull().sum())