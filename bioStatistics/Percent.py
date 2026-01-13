# -*- coding: utf-8 -*-
'''
bioStatistics.Percent 的 Docstring
甘油三酯    频数 
0.1         27
0.4         169
0.7         167
1.0         94
1.3         81
1.6         42
1.9         28
2.2         14
2.5         4
2.8         3
3.1         1
合计        630
'''

distribution = [
    # {'L': 1.9,'Total':630,'Accumulated':580,'i':0.3,'Freq':28}
    {'group':0.1,'frequency':27},
    {'group':0.4,'frequency':169},
    {'group':0.7,'frequency':167},
    {'group':1.0,'frequency':94},
    {'group':1.3,'frequency':81},
    {'group':1.6,'frequency':42},
    {'group':1.9,'frequency':28},
    {'group':2.2,'frequency':14},
    {'group':2.5,'frequency':4},
    {'group':2.8,'frequency':3},
    {'group':3.1,'frequency':1}
]
# 累积频数
current_accumulated = 0
# 累积频率
current_freq_percent = 0.0
# 组距
group_instance = 0.3
# 总频数
total = sum([date['frequency'] for date in distribution])
target_rank = total * 0.95
for data in distribution:
    feq_p = data['frequency'] / 630.0
    current_accumulated += data['frequency']
    # 如果频数 >= 医学参考95%的频数
    if current_accumulated >= target_rank:
        L = data['group']
        i =  group_instance
        Fm = data['frequency']
        n = total
        fL = current_accumulated - data['frequency']
        print(f"组距下限值L：{L},组距：{i}，当前频数：{Fm}，总频数：{n}，累积频数:{fL}")
        median = L + i * ((n * 0.95 - fL) / Fm)
        print(f"95百分位数中位数为: {median}")
        break
    current_freq_percent += feq_p


