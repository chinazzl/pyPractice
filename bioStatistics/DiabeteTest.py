import pandas as pd
import numpy as np
from sklearn.preprocessing import StandardScaler

class DiabetesMedicalAnalysis:

    def __init__(self,data_path):
        """
        初始化分析对象
        :param data_path:
        """
        self.data_path = data_path
        self.df = None
        self.X_train = None
        self.y_train = None
        self.X_test = None
        self.y_test = None
        self.model = None
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




if __name__=="__main__":
    dma = DiabetesMedicalAnalysis("resources/diabetes.csv")
    dma.loadData()
    dma.data_quality_check()
    dma.clean_data()

