from random import sample

import pandas as pd
import numpy as np
from scipy import stats
from sklearn.model_selection import train_test_split,cross_val_score
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
        results_df.to_csv('resources/statistical_teset_results.csv',index=False)
        print("\n统计检验结果已保存：statistical_teset_results.csv")
        return results_df

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
        n = len(data)
        if n < 120:
            print(f"警告：样本量n={n} 不足120，计算的参考区间可能不稳定(CLSI C28-A3 标准推荐 n>=120)）")
        # 1， 正态性检验
        stat,p_value = stats.shapiro(data)
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
        return lower_limit,upper_limit

if __name__=="__main__":
    data_path = 'resources/diabetes.csv'
    dma = DiabetesMedicalAnalysis(data_path)
    dma.loadData()
    dma.data_quality_check()
    dma.clean_data()
    dma.statistical_tests()
    # ⭐ 关键修改：重新读取原始数据，而不是使用 self.df
    original_df = pd.read_csv(data_path)
    dma.calculate_reference_interval(original_df)

