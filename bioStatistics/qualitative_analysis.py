import numpy as np
import pandas as pd
from sklearn.metrics import confusion_matrix, roc_curve, auc, classification_report
import matplotlib.pyplot as plt

"""
 y_true: 真实病人状态（1=有病；0=健康）
 y_scores: 仪器测出来的数值
 threshold：判定阳性的阈值（比如 > 40 算阳性）
"""


def analyze_diagnostic_test(y_true, y_scores, threshold):
    # 根据阈值生成预测结果（ 1 or 0）
    y_pred = (y_scores > threshold).astype(int)
    #     生成混淆矩阵
    """
    混淆矩阵 (Confusion Matrix)= 第九章的“四格表”你的迷茫： 听起来像是什么高深的线性代数矩阵。
    真相： 这就是你在卡方检验里列的那个 $2 x 2$ 的表格！书上叫：阳性/阴性、A组/B组。
      工作里叫：真阳性 (TP)、假阳性 (FP)、真阴性 (TN)、假阴性 (FN)。
      为什么用它： 统计学课本只教你算 P 值（看两组有没有区别），但企业里更关心**“算得准不准”**。
      于是他们给这个四格表里的四个格子起了名字，拼起来就叫“混淆矩阵”。
    """
    tn, fp, fn, tp = confusion_matrix(y_true, y_pred).ravel()
    print(f"混淆矩阵：TN:{tn}, FP:{fp}, FN:{fn}, TP:{tp}")
    # 灵敏性
    sensitivity = tp / (tp + fn) if tp + fn > 0 else 0
    # 特异性
    specificity = tn / (tn + fp) if tn + fp > 0 else 0
    # 准确率
    accuracy = (tp + tn) / (tp + tn + fp + fn)
    print(f"=== 阈值设为 {threshold} 时的性能 ===")
    print(f"混淆矩阵: [TN:{tn}, FP:{fp}, FN:{fn}, TP:{tp}]")
    print(f"灵敏度 (Sensitivity): {sensitivity:.2%}")
    print(f"特异度 (Specificity): {specificity:.2%}")
    print(f"总准确率 (Accuracy): {accuracy:.2%}")

    # 4. 画ROC曲线，评估整体性能，与阈值无关
    fpr,tpr,_ = roc_curve(y_true, y_scores)
    """
    AUC 含义
        AUC = 0.5：随机猜测，无分类能力
        AUC = 1.0：完美分类器
        AUC 越接近1：模型性能越好
    """
    roc_auc = auc(fpr,tpr)
    plt.plot(fpr,tpr,color='darkorange',lw=2, label=f'AUC={roc_auc:.3f}')
    plt.plot([0,1],[0,1],color='navy',linestyle='--')
    plt.xlabel('1-Specificity(False Positive Rate)')
    plt.ylabel('Sensitivity(True Positive Rate)')
    plt.title('ROC Curve')
    plt.legend(loc='lower right')
    plt.show()


if __name__ == "__main__":
#     真实情况 100健康  100病人
    truth = np.array([0] * 100 + [1] * 100)
    # 测量值：健康人均值30 ， 病人均值50
    measurements = np.concatenate([np.random.normal(30,10,100),np.random.normal(50,10,100)])
    # 运行
    analyze_diagnostic_test(truth, measurements, 12)




