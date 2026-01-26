"""
模拟真实生产环境数据清洗
我为你设计了一个 “工业级数据清洗模块”。它不仅是简单的填补空值，而是模拟了真实 IVD 场景中会遇到的 三大类脏数据：
格式污染：比如 "< 0.5" (低于检测限)、"> 1000" (爆量程)、"5.6 mmol/L" (带单位)。
逻辑错误：比如 "-0.02" (浓度不可能是负的，通常是底物耗尽或定标偏差)。
离群噪音：比如 "Error"、"NaN" 或完全不合理的数值。
"""
import pandas as pd
import numpy as np
import re
from sklearn.preprocessing import StandardScaler


class CleanData:

    def __init__(self,data_path):
        """
        初始化分析对象
        :param data_path:
        """
        self.data_path = data_path
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

    def inject_dirty_data(self):
        print("\n" + "!"*50)
        print("模拟真实世界的脏数据")
        # 1. 模拟低于检测下限LOD的情况 "< 0.1"
        mask_low = self.df['Glucose'] < 80
        self.df.loc[mask_low, 'Glucose'] = "< 2.0"
        # 2. 模拟带单位的情况: "105.5 mg/dL"
        # 随机选 10 个样本加上单位
        random_idx = self.df.sample(10).index
        self.df.loc[random_idx, 'BMI'] = self.df.loc[random_idx, 'BMI'].astype(str) + " kg/m2"

        # 3. 模拟负值噪音 (定标偏差): "-0.5"
        # 胰岛素有些算出来是负的
        self.df.loc[0:5, 'Insulin'] = -5.0

        # 4. 模拟仪器报错: "Error"
        self.df.loc[10:15, 'BloodPressure'] = "Error"

        print("模拟完成！现在你的数据变得乱七八糟了。")
        print(self.df[['Glucose', 'BMI', 'Insulin', 'BloodPressure']].head(15))
        print("!" * 50 + "\n")

    def _parse_value(self,val,lod_value=None):
        """
            内部工具 只能解析单个数值
        :param val:
        :param lod_value:
        :return:
        """
        if pd.isna(val):
            return np.nan
        val_str = str(val).strip()
        # A 已经是数字
        try:
            return float(val)
        except ValueError:
            pass
        # B. 处理 "<2.0"，行业惯例：通常取检测线的一半（Lod/2）或者直接去LoD
        if val_str.startswith("<"):
            num = float(re.findall(r"[-+]?\d*\.\d+|\d+",val_str)[0])
            #策略：如果发现小于号，返回数值/2
            return num/2
        # C 处理“>1000"高于检测值
        if val_str.startswith(">"):
            num = float(re.findall(r"[-+]?\d*\.\d+|\d+",val_str)[0])
            return num # 或者 num *1.1

        #D. 处理单位 “25.5 kg/m2
        maches = re.findall(r"[-+]?\d*\.\d+|\d+",val_str)
        if maches:
            return float(maches[0])
        #E. 完全无法解析
        return np.nan

    def clean_real_world_data(self, strategy='strict'):
        """

        :param strategy:
            - strict:严格模式（遇到坏数据直接整行删除，适用于注册临床试验）
            - impute：填补模式（坏数据设为NaN，后续用中位数/均值填补，适用于探索性挖掘）
        :return:
        """
        print(f"=== 开始执行工业级数据清洗 (策略: {strategy}) ===")
        features = ['Glucose', 'BloodPressure', 'SkinThickness', 'Insulin', 'BMI']
        for col in features:
            print(f">>正在清洗指标：{col}")
            #1. 清洗格式（String -> Float)
            self.df[col] = self.df[col].apply(self._parse_value)
            # 2. 逻辑清洗
            # 在IVD中，浓度 <0通常是由于本底扣除过大，物理上归零
            neg_count = (self.df[col] < 0).sum()
            if neg_count > 0:
                print(f" 发现{neg_count}个负值，修正为0.0")
                self.df.loc[self.df[col] <0,col] = 0.0
        # 2. 缺失值处理策略
        initial_len = len(self.df)
        if strategy == 'strict':
            # 临床试验标准 (CLSI): 只要有一个指标坏了，这行数据就废了，不能瞎猜。
            self.df.dropna(subset=features, inplace=True)
            print(f"\n【清洗报告】严格模式：剔除了{initial_len - len(self.df)}行包含无效数据的样本。")
        elif strategy == 'impute':
            # 数据挖掘标准：只要不是太多，我就猜它是多少
            for col in features:
                median_val = self.df[col].median()
                self.df[col] = self.df[col].replace(np.nan, median_val)
            print(f"\n【清洗报告】填补模式，所有的NaN已经用中位数进行填补")
        print(f"清洗后剩余样本量：{len(self.df)}")
        print("="*50)
        return self.df


if __name__ == '__main__':
    data_path = "resources/diabetes.csv"
    dma = CleanData(data_path)
    dma.loadData()
    dma.inject_dirty_data()
    dma.clean_real_world_data()





