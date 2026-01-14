"""
模拟卡方检验
"""

import pandas as pd
import numpy as np
from scipy import stats

# 1. 简历四格表
"""
      阳性  阴性
医院1  40    10
医院2  35    15
"""
data_table = np.array([[40,10],[35,15]])
n = np.sum(data_table)
print(f"总样本量{n}")
# 2. 卡方检验
"""

请记住这个**“IVD 行业黄金法则”**：
总样本数 $N >= 40$ 且所有格子的期待值 $ > 5$：用 普通卡方 (Pearson Chi-square)。这是最常见的情况。
总样本数 $N >= 40$ 但有格子期待值在 $1 ~ 5$ 之间：用 校正卡方 (Yates' Correction for Continuity)。也就是书上那个复杂的公式，但代码里就是一个参数的事。
总样本数 $N < 40$ 或有格子期待值 T $ < 1$：
    放弃卡方，直接用 Fisher 精确检验 (Fisher's Exact Test)。
    面试必杀技：如果样本很小，别纠结校正不校正了，直接告诉面试官“这时候应该用 Fisher 精确检验”，这显着你特别专业.
# --- 方法 1：卡方检验 (含校正) ---
# correction=True (默认就是True)，Python会自动帮你应用那个复杂的校正公式
chi2, p, dof, expected = stats.chi2_contingency(data, correction=True)
print(f"校正卡方 P值: {p:.4f}")

# correction=False，就是书上最简单的公式
chi2_uncorrected, p_uncorrected, _, _ = stats.chi2_contingency(data, correction=False)
print(f"普通卡方 P值: {p_uncorrected:.4f}")

# --- 方法 2：Fisher 精确检验 (IVD行业小样本首选) ---
# 当你会用这个时，校正公式就不重要了，因为这个是“精确”的，不是“近似”的
oddsratio, p_fisher = stats.fisher_exact(data)
print(f"Fisher精确检验 P值: {p_fisher:.4f}")
"""

"""
注意 $E$ 是分母！如果 $E$ 很大（比如 50）：分母很稳，算出来的结果很靠谱。如果 $E$ 很小（比如 1）：
哪怕观察值 $O$ 只变了一点点（比如从 1 变成 2），分子 $(2-1)^2 = 1$。但因为分母是 1，结果直接就是 1。
分母太小，会导致算出来的卡方值“虚高”（不稳定），让你误以为有显著差异，实际上可能只是运气导致的误差。
这就是为什么统计学规定：当 $E < 5$ 时，卡方检验会“发飘”，必须用校正公式或者 Fisher 精确检验。
"""
# 检验是否有任意一个期待值 < 5
chi2, p_val, dof, expected = stats.chi2_contingency(data_table, correction=False)
min_T = np.min(expected)
if n>=40 and min_T >= 5:
    print("判定所有期待值均大于 5 样本量充足")
    chi2, p, dof, expected = stats.chi2_contingency(data_table,correction=False)
    print(f"卡方值：{chi2:.4f},P值：{p:.4f}，期待值矩阵：\n{expected}")
    print(f"卡方检验 P值: {p:.4f}")
    final_P = p

elif n>=40 and min_T >= 1:
    print("判定 n>=40 且 1<= T < 5")
    chi2, p, dof, expected = stats.chi2_contingency(data_table,correction=True)
    print(">> 采用 卡方校正")
    print(f"校正卡方检验 P值: {p:.4f}")
    final_P = p
else:
    print("\n判定检测到有期待值小于5 或 n < 40，卡方检验结果可能不准确。")
    print(">>> 自动切换为：Fisher精确检验")
    # 调用Fisher精确检验
    oddsr, p_fisher = stats.fisher_exact(data_table)
    print(f"Fisher精确检验 P值：: {p_fisher:.4f}")
    final_P = p_fisher

print("-"*50)
"""
“在处理分类数据时，我不会盲目使用卡方检验。 我的代码流程是：先计算理论期待值（Expected Values）。
如果发现任何一个格子的期待值小于 5（说明样本太小），我的程序会自动降级使用 Fisher 精确检验。 
这样可以避免因为样本不足导致的第一类错误（假阳性），确保我们给出的医学结论是经得起推敲的。”
"""
if final_P > 0.05:
    print("结论：两家医院的阳性率没有显著差异")
else:
    print("结论：有差异")