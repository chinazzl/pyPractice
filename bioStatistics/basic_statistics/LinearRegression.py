
"""
线性回归
"""
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from scipy.stats import linregress

# 1. 拟合数据
concentration = np.array([0,10,20,50,100,200])
# 发光值 Y= 50 * X + 100（噪音）
signal = 50 * concentration + 100 + np.random.normal(0,200,len(concentration))

# 2. 线性回归计算
slope,intercept, r_value,p_value,std_err = linregress(concentration,signal)

print(f"回归方程：Y = {slope:.2f}X + {intercept:.2f}")
# 越接近1越好
print(f"R平方：{r_value ** 2:.4f}")
print(f"P值：{p_value:.4e}")

# 画图
plt.scatter(concentration,signal,label='Data')
plt.plot(concentration, slope*concentration + intercept,'r',label='Fit')
plt.legend()
plt.show()
