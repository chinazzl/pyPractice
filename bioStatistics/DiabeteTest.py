import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import seaborn as sns
from scipy import stats
from sklearn.metrics import auc, confusion_matrix, roc_curve
from sklearn.preprocessing import StandardScaler


class DiabetesMedicalAnalysis:

    def __init__(self,data_path):
        """
        初始化分析对象
        :param data_path:
        """
        self.data_path = data_path
        # self.df = None
        self.X_train = None
        self.y_train = None
        self.X_test = None
        self.y_test = None
        self.model = None
        self.df = None
        #  将数据转换为标准正态分布
        self.scaler = StandardScaler()

    def loadData(self):
        """1. 数据加载和初步检验"""
        print("="*50)
        print("步骤一、数据加载")
        self.df = pd.read_csv(self.data_path)
        print(f"\n数据集大小：{self.df.shape}")
        print(f"\n样本数量{self.df.shape[0]}")
        print(f"\n特征数量{self.df.shape[1]}")
        print(f"\n数据类型:")
        print(self.df.dtypes)
        print("\n前五行数据")
        print(self.df.head())
        print("\n基本统计信息")
        print(self.df.describe())
        return self.df

    def data_quality_check(self):
        """数据质量检查"""
        print("="*50)
        # 缺失值检查
        print("\n缺失值统计")
        missing = self.df.isnull().sum()
        print(missing)
        print(missing[missing > 0] if missing.sum() >0 else "无缺失值")
        # 零值检查（某些指标为0可能是缺失值）
        print("\n可能异常的零值统计：")
        zero_features = ['Glucose', 'BloodPressure', 'SkinThickness',
                        'Insulin', 'BMI']
        for zfeature in zero_features:
            zero_count = (self.df[zfeature]==0).sum()
            percemtage = zero_count / len(self.df) * 100
            print(f"{zfeature}: {zero_count} => {percemtage:.2f}%")
        # 目标变量分布
        print("\n目标变量(Outcom)分布：")
        outcome_counts = self.df['Outcome'].value_counts()
        print(outcome_counts)
        print(f"阳性率{outcome_counts[1]/len(self.df)*100}%")
        return self.df

    def clean_data(self):
        print("执行数据清理")
        print("="*50)
        features_to_clean = ['Glucose', 'BloodPressure', 'SkinThickness', 'Insulin', 'BMI']
        for feature in features_to_clean:
            # 1. 算出中位数，只算出非0的数据
            median_value = self.df[self.df[feature]>0][feature].median()
            # 统计多少个0被替换了
            zero_count = (self.df[feature]==0).sum()
            # 执行替换中位数
            self.df[feature] = self.df[feature].replace(0,median_value)
            # 4. 打印处理结果
            print(f"{feature}: 填充了 {zero_count} 个零值，使用中位数 {median_value:.2f}")
        return self.df

    def statistical_tests(self):
        print("统计假设检验")
        print("="*50)
        results = []
        features = self.df.columns[:-1]
        for feature in features:
            # 分组数据
            group_0 = self.df[self.df['Outcome'] == 0][feature]
            group_1 = self.df[self.df['Outcome'] == 1][feature]
            # 正态性检验
            stat_0, p_0 = stats.shapiro(group_0.sample(min(5000, len(group_0))))
            stat_1, p_1 = stats.shapiro(group_1.sample(min(5000, len(group_1))))
            # 根据正态选择检验方法
            if p_0 > 0.05 and p_1 > 0.05:
                # t检验
                t_stat,p_value = stats.ttest_ind(group_0,group_1)
                test_type = 't-test'
            else :
                u_stat,p_value = stats.mannwhitneyu(group_0,group_1)
                test_type = 'Mann-Whitney U'
            # 计算效应量
            """
            想象你在开发一种降血压药（或者试剂盒），你有两组数据：吃药组 vs. 不吃药组。
            P 值 (P-value)：回答 “有没有区别？”
            它像一个开关（Boolean）。
            P < 0.05：有区别！
            但是：如果你的样本量超级大（比如 10 万人），哪怕血压只降了 0.01 mmHg，P 值也会小于 0.05。
            结论：统计学上显著，但在医学上毫无意义（降 0.01 等于没降）。
            效应量 (Effect Size/Cohen's d)：回答 “区别有多大？”
            它是一个程度值（Float）。
            它不看样本量，只看两组数据的真实差距。
            结论：如果效应量很小（比如 0.01），说明虽然 P 值显著，但这个药其实是个“废柴”。
            
            # 场景对比：
            场景A: 小样本研究
            - 健康人组（n=20）：血糖平均值 100 mg/dL
            - 糖尿病组（n=20）：血糖平均值 120 mg/dL
            - 差值：20 mg/dL
            - P值：0.08（不显著）
            
            场景B: 大样本研究
            - 健康人组（n=10000）：血糖平均值 100 mg/dL
            - 糖尿病组（n=10000）：血糖平均值 102 mg/dL
            - 差值：2 mg/dL
            - P值：<0.001（高度显著）
            
            # 问题：
            # 场景A：差值20 mg/dL，但P值不显著 → 结论"没区别"？
            # 场景B：差值2 mg/dL，但P值显著 → 结论"有区别"？
            
            # 答案：
            # P值只告诉你"是否统计显著"，不告诉你"临床意义多大"
            # Cohen's d 告诉你"实际差异有多大
            
            # 记忆口诀：
            # 0.2 - 稍微有点区别
            # 0.5 - 有明显区别
            # 0.8 - 区别很大
            # 1.0 - 区别非常大
            关键理解：

            •	P值 < 0.05 ≠ 临床有意义
            •	Cohen’s d >= 0.5 ≠ 统计显著
            •	理想情况：P < 0.05 且 d >= 0.5（既有统计意义又有临床意义）
            •	最糟情况：P < 0.05 但 d < 0.2（统计显著但临床无意义）
            
            """
            conhens_d = ((group_1.mean()-group_0.mean())/
                         np.sqrt((group_1.std() ** 2 + group_0.std() ** 2))/2)
            results.append({
                'Feature': feature,
                'Test': test_type,
                'Mean(Healthy)': group_0.mean(),
                'Mean(Diabetic)': group_1.mean(),
                'Statistic': t_stat if test_type == 't-test' else u_stat,
                'P_value': p_value,
                "Conhen's d": conhens_d,
                'Significant': '***' if p_value < 0.001 else '**' if p_value < 0.01 else '*' if p_value < 0.05 else 'ns'
            })
        results_df = pd.DataFrame(results)
        print("\n统计检验结果：")
        print(results_df.to_string(index=False))
        # 保存结果
        results_df.to_csv('resources/statistical_test_results.csv',index=False)
        print("\n统计检验结果已保存：statistical_test_results.csv")
        return results_df

    """
    在计算参考区间之前（CLSI C28-A3 标准建议），我们必须剔除离群值。
    
    比如：虽然你选的是“健康人”，但有个人可能那天喝醉了，血糖飙到 300。
    
    如果不剔除这个 300，你算出来的上限就会被拉高，导致试剂盒“不灵敏”。
    """
    def remove_outliers_iqr(self,data):
        """
            辅助函数 使用IQR（四分位距法）提出离群值
        :return:
        """
        Q1 = np.percentile(data,25)
        Q3 = np.percentile(data,75)
        IQR = Q3 - Q1
        # 定义篱笆
        lower_fence = Q1 - 1.5*IQR
        upper_fence = Q3 + 1.5*IQR
        # 只保留篱笆内的数据
        clean_data = [x for x in data  if lower_fence <= x <= upper_fence]
        return clean_data

    def calculate_reference_interval(self,originalData_df,confidence=0.95):
        """
            计算参考区间
            data: 必须是【健康人】的数据列表
            confidence: 默认95%双侧区间
        :param data:
        :param confidence:
        :return:
        """
        data = originalData_df[originalData_df['Outcome'] == 0]['Glucose']
        data = data[data > 0]
        # 使用IQR进行过滤
        clean_data_list = self.remove_outliers_iqr(data)
        data = pd.Series(clean_data_list)
        n = len(data)
        if n < 120:
            print(f"警告：样本量n={n} 不足120，计算的参考区间可能不稳定(CLSI C28-A3 标准推荐 n>=120)）")
        # 1， 正态性检验
        stat,p_value = stats.shapiro(data.sample(min(5000,len(data))))
        print(f"---参考区间计算（N={n}）---")
        print(f"正态性检验 P值：{p_value:.4f}")
        lower_limit,upper_limit = 0,0
        if p_value > 0.05:
            # A 正态分布 参数法
            method = "参数法（Mean +- 1.96SD）"
            mean_val = np.mean(data)
            # ddof = 1 样本标准差
            std_val = np.std(data,ddof=1)
            # 计算双侧界限
            z_score = stats.norm.ppf((1+ confidence)/2) # 通常是1.96
            print(f"z_score={z_score:.4f}")
            lower_limit = mean_val - std_val * z_score
            upper_limit = mean_val + std_val * z_score
        else:
            # B. 偏态分布 （非参数法/百分位数法）
            method = "非参数法（2.5% - 97.5% 分位数）"
            # 计算分位点
            q_low = (1-confidence)/2
            q_high = 1 - (1-confidence)/2
            lower_limit = np.percentile(data,q_low * 100)
            upper_limit = np.percentile(data,q_high * 100)
            print(f"2.5% 分位数：{lower_limit:.2f}")
            print(f"97.5% 分位数：{upper_limit:.2f}")
        print(f"采用方法：{method}")
        print(f"计算结果：[{lower_limit:.2f},{upper_limit:.2f}]")
        print("-"*30)
        print(f"最终结论：该试剂盒的血糖正常参考范围是 {lower_limit:.1f} - {upper_limit:.1f}")
        # Q-Q图
        """
            关键观察：
            左尾（低值区）：点在红线下方，说明实际数据比正态分布更"聚集"
            右尾（高值区）：点在红线上方，说明存在比正态分布预期更多的高值
            这是典型的 "重尾"（Heavy-tailed）分布，也就是说：
            
            数据的尾部比标准正态分布更"厚"
            极端值（特别是高值）比正态分布预期的要多
            这会导致 正峰度（尖峰厚尾）
            为什么会这样？
            在健康人群的血糖数据中，可能的原因：
            混入了亚临床高血糖者：虽然标记为健康（Outcome=0），但可能有些人处于糖尿病前期
            测量误差：极端高值可能是检测异常
            生理特征：血糖本身就不是完美正态的，特别是在包含餐后血糖的情况下
        """
        stats.probplot(data, dist="norm", plot=plt)
        plt.title("Q-Q Plot for Glucose (Healthy)")
        plt.show()
        # 直方图 + 正态分布
        plt.hist(data, bins=30, density=True, alpha=0.7)
        # 叠加正态分布曲线
        mu, sigma = data.mean(), data.std()
        x = np.linspace(data.min(), data.max(), 100)
        plt.plot(x, stats.norm.pdf(x, mu, sigma), 'r-', label='Normal')
        plt.legend()
        plt.show()
        self.plot_refernce_distribution(data,lower_limit,upper_limit,"Glucose")
        return lower_limit,upper_limit

    def plot_refernce_distribution(self,data,low,high,feature_name):
        """
            画图函数：绘制直方图并标记参考区间界限
        :return:
        """
        plt.figure(figsize=(10,6))
        # 1. 绘制直方图和密度曲线
        sns.histplot(data,kde=True,color='blue',label="Healthy Distribution")
        #2. 画出参考下限和上限
        plt.axvline(low,color='red',linestyle='--',linewidth=2,label=f"Low Limit ({low:.2f})")
        plt.axvline(high,color='red',linestyle='--',linewidth=2,label=f"High Limit ({high:.2f})")
        # 3.添加图例和标题
        plt.title(f'Reference Interval Distribution: {feature_name}', fontsize=14)
        plt.xlabel(feature_name)
        plt.ylabel('Count / Frequency')
        plt.legend()
        plt.grid(True, alpha=0.3)
        plt.show()

    def generate_report(self,result_df= None):
        """步骤7: 生成分析报告"""
        print("\n" + "=" * 60)
        print("步骤7: 生成分析报告")
        print("=" * 60)
        if result_df is None:
            try:
                result_df = pd.read_csv('resources/statistical_test_results.csv')
            except FileNotFoundError:
                print("警告：未找到统计检验结果文件，使用默认模板")
                result_df = None
        if result_df is not None:
            # 筛选显著特征
            significant_features = result_df[result_df['P_value'] < 0.05].copy()
            significant_features = significant_features.sort_values('P_value')
            # 按效应量分类
            high_effect = significant_features[abs(significant_features["Conhen's d"]) >= 0.8]
            medium_effect = significant_features[
                (abs(significant_features["Conhen's d"]) >= 0.5) &
                (abs(significant_features["Conhen's d"]) < 0.8)
            ]
            small_effect = significant_features[
                (abs(significant_features["Conhen's d"]) >= 0.2) &
                (abs(significant_features["Conhen's d"]) < 0.5)
            ]
            # 生成风险因素描述
            risk_factors = []
            for idx,row in high_effect.iterrows():
                feature = row['Feature']
                cohens_d = row['Cohens d']
                mean_healthy= row['Mean(Healthy)']
                mean_diabetic = row['Mean(Diabetic)']
                direction = "高于" if mean_diabetic > mean_healthy else "低于 "
                risk_factors.append(
                    f" -{feature}({'效应量：' + f'{cohens_d:.2f}'}：糖尿病患者{direction}健康人，"
                    f"p<0.001,大效应)"
                )
            for idx,row in medium_effect.iterrows():
                feature = row['Feature']
                cohens_d = row["Conhen's d"]
                mean_healthy = row['Mean(Healthy)']
                mean_diabetic = row['Mean(Diabetic)']
                direction = "高于" if mean_diabetic > mean_healthy else "低于"
                risk_factors.append(
                    f"   - {feature}（效应量：{cohens_d:.2f}，中等效应）"
                )
            risk_factors_text = "\n".join(risk_factors) if risk_factors else "   （无显著风险因素）"
        else:
            risk_factors_text = "   （数据未加载）"

        report = f"""
            ================================================================================
                                糖尿病数据医学统计分析报告
            ================================================================================
            
            一、数据概况
            --------------------------------------------------------------------------------
            数据集大小: {self.df.shape[0]} 个样本
            特征数量: {self.df.shape[1] - 1} 个医学指标
            目标变量: Outcome (0=非糖尿病, 1=糖尿病)
            
            二、主要发现
            --------------------------------------------------------------------------------
            1. 数据质量
               - 总体数据完整性良好
               - 部分生理指标存在零值，可能是缺失值或测量误差
            
            2. 关键风险因素（基于统计检验）
               {risk_factors_text}
            
            3. 非显著因素
            3. 非显著因素
                - 以下因素在两组间差异无统计学意义（P >= 0.05）：
                {chr(10).join([f'     - {row["Feature"]}' for idx, row in result_df[result_df['P_value'] >= 0.05].iterrows()]) if result_df is not None else '     （数据未加载）'}
                
            4. 预测模型性能
               - 模型类型: 逻辑回归
               - 测试集准确率: 待评估
               - AUC: 待评估
               - 交叉验证平均准确率: 待评估
            
            
            三、临床建议
            --------------------------------------------------------------------------------
           1. 诊断指标优先级
            {chr(10).join([f'   - {row["Feature"]}：应作为主要诊断依据（大效应量）' for idx, row in high_effect.iterrows()]) if result_df is not None and not high_effect.empty else '   - 建议结合多项指标进行综合评估'}

            2. 风险因素管理
            {chr(10).join([f'   - 关注{row["Feature"]}的干预（中等效应量）' for idx, row in medium_effect.iterrows()]) if result_df is not None and not medium_effect.empty else '   - 建议结合多项指标进行综合评估'}
            
            3. 弱相关因素
               - 以下因素对糖尿病预测贡献有限（小效应量或无显著性）：
                {chr(10).join([f'     - {row["Feature"]}' for idx, row in result_df[(result_df['P_value'] >= 0.05) | (abs(result_df["Conhen's d"]) < 0.2)].iterrows()]) if result_df is not None else '     （需进一步分析）'}
            
            四、方法学说明
            --------------------------------------------------------------------------------
            - 统计检验: t检验/Mann-Whitney U检验
            - 参考区间计算: 参数法/非参数法（根据正态性检验选择）
            - 显著性水平: α = 0.05
            - 效应量评估: Cohen's d（0.2小/0.5中/0.8大）
            
            五、局限性
            --------------------------------------------------------------------------------
            1. 样本量有限（{self.df.shape[0]}例），可能影响统计效能
            2. 横断面研究设计，无法确定因果关系
            3. 部分指标存在缺失值，已用中位数填充
            4. 需要在独立人群中验证参考区间
            
            ================================================================================
            报告生成时间: {pd.Timestamp.now().strftime('%Y-%m-%d %H:%M:%S')}
            ================================================================================
        """

        print(report)

        # 保存报告
        with open('resources/diabetes_analysis_report.txt', 'w', encoding='utf-8') as f:
            f.write(report)

        print("\n完整报告已保存: diabetes_analysis_report.txt")

        return report

    def method_comparison(self):
        """
            如何证明你的新机器和金标准是一致的
            实现回归分析：算斜率、截距、R2
            实现Bland-Altman分析：算偏差Bias和一致性界限LoA
        """
        print("方法学比对")
        print("\n" + "=="*50)
        # 假设Glucose是新机器测的，我们造一个金标准 Glucose_Gold
        # 金标准 = 新机器 /1.05（有5%的偏差） + 随机噪音
        np.random.seed(42)
        y_new = self.df['Glucose']
        x_gold = y_new / 1.05 + np.random.normal(0,2,len(y_new))
        # 2. 线性回归分析
        slope,intercept, r_value,p_value,std_err = stats.linregress(x_gold, y_new)
        print(f"回归方程：Y= {slope:.3f}X + {intercept:.3f}")
        print(f"相关系数(R^2): {r_value ** 2:.4f}")
        # 3. Bland -ALtman分析
        diff = y_new - x_gold
        mean_diff = np.mean(diff)
        sd_diff = np.std(diff)
        # 上界限
        upper_loa = mean_diff + 1.96 * sd_diff
        # 下界限
        lower_loa = mean_diff - 1.96 * sd_diff
        print(f"平均偏差（Bias）：{mean_diff:.2f}")
        print(f"95%一致性界限(LoA):[{lower_loa:.2f},{upper_loa:.2f}]")

        # 4. 绘图（回归图 + BA图）
        plt.subplot(1,2,1)
        plt.plot(x_gold, slope * x_gold + intercept,color='red',linewidth=2,label = f'R^2={r_value**2:.4f}')
        plt.title('Regressioin Analysis')
        plt.xlabel('Gold Standard')
        plt.ylabel('New Method')
        plt.legend()

        # BA图
        plt.subplot(1,2,2)
        plt.scatter((x_gold + y_new)/2,diff,alpha=0.3)
        plt.axhline(mean_diff,color='red',linestyle='-',label='Bias')
        plt.axhline(upper_loa,color='red',linestyle='--',label='Upper LoA')
        plt.axhline(lower_loa,color='red',linestyle='--',label='Lower LoA')
        plt.title('Bland-Altman Analysis')
        plt.xlabel('Mean of Methods')
        plt.ylabel('Difference (New - Gold)')
        plt.legend()
        plt.show()

    def evaluate_diagnostic_performance(self, feature='Glucose', threshold=None):
        """
        任务二：诊断效能评估
        计算 ROC, AUC, 灵敏度, 特异度
        """
        print("\n" + "=" * 50)
        print(f"步骤：诊断效能评估 ({feature})")
        print("=" * 50)

        y_true = self.df['Outcome']
        y_scores = self.df[feature]

        # 1. 计算 ROC 和 AUC
        fpr, tpr, thresholds = roc_curve(y_true, y_scores)
        roc_auc = auc(fpr, tpr)
        print(f"AUC 值: {roc_auc:.4f}")

        # 2. 确定 Cut-off 值
        # 如果没传阈值，就用 Youden 指数最大点 (TPR - FPR 最大)
        if threshold is None:
            youden_index = tpr - fpr
            best_idx = np.argmax(youden_index)
            threshold = thresholds[best_idx]
            print(f"自动计算最佳 Cut-off 值: {threshold:.2f}")

        # 3. 计算灵敏度和特异度
        y_pred = (y_scores >= threshold).astype(int)
        tn, fp, fn, tp = confusion_matrix(y_true, y_pred).ravel()

        sensitivity = tp / (tp + fn)
        specificity = tn / (tn + fp)

        print(f"灵敏度 (Sensitivity): {sensitivity:.2%}")
        print(f"特异度 (Specificity): {specificity:.2%}")

        # 4. 绘制 ROC 曲线
        plt.figure()
        plt.plot(fpr, tpr, color='darkorange', lw=2, label=f'ROC curve (area = {roc_auc:.2f})')
        plt.plot([0, 1], [0, 1], color='navy', lw=2, linestyle='--')
        plt.xlabel('False Positive Rate')
        plt.ylabel('True Positive Rate')
        plt.title(f'ROC Curve: {feature}')
        plt.legend(loc="lower right")
        plt.show()

"""
在 IVD 数据分析中，工具的出场顺序是有严格逻辑的：
第一关（T检验 / Mann-Whitney）：输入：连续数值（血糖）。问：病人和健康人平均值一样吗？答：P < 0.05，不一样。 $\rightarrow$ 通过，进入下一关。
第二关（ROC / AUC）：输入：连续数值（血糖）。问：这个指标能把两类人分得多开？答：AUC = 0.85，分得挺开。 $\rightarrow$ 通过，找最佳阈值。
第三关（混淆矩阵 / 卡方 / Kappa）：输入：定性类别（阴/阳，基于阈值切割后）。问：在当前阈值下，误诊率和漏诊率是多少？
    答：灵敏度 80%，特异度 90%。 $\rightarrow$ 写入说明书。
"""
def main():
    try:
        data_path = 'resources/diabetes.csv'
        dma = DiabetesMedicalAnalysis(data_path)
        dma.loadData()
        dma.data_quality_check()
        dma.clean_data()
        dma.statistical_tests()
        # ⭐ 关键修改：重新读取原始数据，而不是使用 self.df
        original_df = pd.read_csv(data_path)
        dma.calculate_reference_interval(original_df)
        # 5. 【新增】方法学比对 (证明机器准) -> 对应任务一
        # 注意：这是模拟数据，演示你的回归分析能力
        dma.method_comparison()

        # 6. 【新增】诊断效能评估 (证明能看病) -> 对应任务二
        # 计算 Glucose 的 ROC 和 AUC
        dma.evaluate_diagnostic_performance(feature='Glucose')
        dma.generate_report()
    except Exception as e:
        print(f"\n分析过程出现异常：{str(e)}")
        import traceback
        traceback.print_exc()

if __name__=="__main__":
    main()

