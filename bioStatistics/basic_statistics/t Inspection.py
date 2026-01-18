"""
科美的新试剂盒（Group A）和罗氏的老试剂盒（Group B）检测同一批病人，想证明我们的新产品和老产品结果一致（无显著差异）。
"""
import pandas as pd
import numpy as np
from scipy import stats
import matplotlib.pyplot as plt
import seaborn as sns

# 1. 模拟数据（生成两个均值差不多，但带有随机波动的正态分布数据
np.random.seed(42)
# 新试剂盒 均值 50
group_new = np.random.normal(loc=50, scale=5, size=30)
# 老试剂盒 均值49.5
group_old = np.random.normal(loc=49.5, scale=5, size=30)

# 2. 正态检验
# 先查询能不能用t检验
'''
变量 1：w (The Statistic)全称：Wilk's Statistic (W 统计量)。含义：这是算法算出来的原始分数，
    用来衡量你的数据曲线和标准的“钟形曲线”有多像。数值范围：0 到 1 之间。怎么看：越接近 1，说明越像正态分布。
    程序员视角的理解：这就好比你要判断一张图是不是“圆形”。w 就是“圆度系数”，0.99 说明很圆，0.5 说明是个土豆形状。但在做决策时，我们通常不直接看它，而是看 P 值。
变量 2：p_norm (The P-value)全称：P-value (显著性水平)。
    含义：这才是主角！ 它就是我们刚才聊了半天的那个“概率风险”。
    假设 ($H_0$)：假设这组数据是正态分布的。
'''
w,p_norm = stats.shapiro(group_new)
print(f"正态性检验 P值：{p_norm: .4f}")

# 3. 方差齐性检验
#  检验方差是否对齐
'''
stat (W)：Levene 检验的统计量。和刚才一样，它是给数学家看的，程序员通常只扫一眼。
p_levene (P值)：核心判决依据
'''
stat, p_levene = stats.levene(group_new, group_old)
print(f"方差齐性 P值：{p_levene: .4f}")

# 4. t 检验 （如果方差对齐）
t_stat, p_val = stats.ttest_ind(group_new, group_old)
print(f"t检验 P值：{p_val: .4f}")

# 5. 结论
if p_val > 0.05:
    print("结论：P > 0.05，两组无显著差异（验证通过，和竞品一致）")
else:
    print("结论： 有显著差异（验证失败）")
