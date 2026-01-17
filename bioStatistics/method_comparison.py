import numpy as np
import matplotlib.pyplot as plt
from scipy import stats

"""
定量分析闭环（攻克“一致性”难题）
证明我们的新机器和医院的金标准机器结果一样。
对应书本知识：第十一章 线性回归、第七章 T检验。
工业界术语：方法学比对、回归拟合 ($R^2$)、Bland-Altman 图。

问： 如何做方法学比对？
答： “首先做线性回归，检查 $R^2$ 是否大于 0.98 以及斜率是否接近 1。
    其次，为了更严谨地观察系统误差，我会画 Bland-Altman 图，
    查看平均偏差（Bias）和一致性界限（LoA），确保差异在临床可接受范围内。”

    mehod_x: 老机器/金标准的测值
    method_y: 新机器/待测 的测值
"""
def compare_methods(method_x, method_y):
    print(f"method_x={method_x} method_y={method_y}")
    # 1. 线性回归（看趋势是否一致）
    slope, intercpt, r_value, p_value, std_err = stats.linregress(method_x, method_y)
    print("====线性回归分析：计算新机器和老机器是否趋势相同 ====")
    print(f"回归方程 Y={slope:.3f}X + {intercpt:.3f}")
    print(f"R平方= {r_value:.3f} （越接近1越好）")
    # 2. 绘制回归图
    '''
    •	figsize = (宽度, 高度)，单位是英寸
	•   figsize=(10,5) → 画布宽10英寸，高5英寸
	•	换算成像素：默认 dpi=100，所以是 1000×500 像素
    '''
    plt.figure(figsize=(10,5))
    # 1 → 整个图形分成1行
    # 2 → 每行2列（共2个子图，左右排列）
    # 1 → 当前选中第1个子图（左边）
    plt.subplot(1,2,1)
    plt.scatter(method_x, method_y,alpha=0.5)
    plt.plot(method_x, slope*method_x + intercpt,'r',label='Fit')
    plt.xlabel('Method X (Gold Standard)')
    plt.ylabel('Method Y (New test)')
    plt.title(f'Regression (R^2={r_value**2:.3f})')
    plt.legend()

    # 3. Bland-Altaman分析 （看差值分析）T检验进阶
    diff = method_y - method_x
    mean_diff = np.mean(diff)
    std_diff = np.std(diff)
    print(f"mean_diff={mean_diff:.3f} std_diff={std_diff:.3f}")
    plt.subplot(1,2,2)
    '''
    # 常用参数：
    a      # 要计算平均值的数组
    axis   # 沿哪个轴计算（0=列，1=行）
    dtype  # 返回值的数据类型
    '''
    plt.scatter(np.mean([method_x, method_y],axis=0),diff,alpha=0.5)
    plt.axhline(mean_diff,color='gray',linestyle='--')
    # 上界
    plt.axhline(mean_diff + 1.96*std_diff,color='red',linestyle=':')
    # 下界限
    plt.axhline(mean_diff - 1.96*std_diff,color='red',linestyle=':')
    plt.title(f"Bland-Altman Plot (Mean Diff = {mean_diff:.2f})")
    plt.xlabel('Mean Value')
    plt.ylabel('Difference (Y-X)')
    plt.tight_layout()
    plt.show()

if __name__ == "__main__":
    x_data = np.linspace(0, 100, 50)
    y_data= 1.05 * x_data+ 2 + np.random.normal(0, 3, 50)
    compare_methods(x_data, y_data)
