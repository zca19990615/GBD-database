# -*- coding: utf-8 -*-
"""
Created on Tue Jun 25 22:22:58 2024

@author: 61967
"""

# -*- coding: utf-8 -*-
"""
Created on Tue Jun 25 22:12:09 2024

@author: 61967
"""

# -*- coding: utf-8 -*-
"""
Created on Sat Jun  8 20:38:35 2024

@author: 61967
"""

import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# 加载数据
file_path = 'C:\\Users\\61967\\Desktop\\GBD\\China\\年龄段\\中国\DALY.csv'
data = pd.read_csv(file_path)

# 过滤数据，仅保留 "Low physical activity" 和 2021年的数据
filtered_activity_data = data[(data['rei'] == 'Low physical activity') & (data['year'] == 2021)]

# 去掉性别为 'Both' 的数据
filtered_activity_data = filtered_activity_data[filtered_activity_data['sex'] != 'Both']

# 创建透视表，索引为年龄组，列为位置，值为DALYs率
pivot_activity_data = filtered_activity_data.pivot_table(index='age', columns='sex', values='val')

# 设置风格为自然风格
sns.set(style="whitegrid", palette="muted")

# 修改配色
colors = {'Male': '#d95f02', 'Female': '#1b9e77'}  # 替换为橙色和绿色

# 设置字体大小
plt.rcParams.update({'font.size': 30})  # 更新全局字体大小

# 绘制并排柱状图
plt.figure(figsize=(24, 18))  # 调整图表大小
pivot_activity_data.plot(kind='bar', color=[colors[col] for col in pivot_activity_data.columns], figsize=(24, 18), width=0.8)
plt.title('', fontsize=30)
plt.xlabel('Age Group', fontsize=30)
plt.ylabel('DALY Rate (per 100,000)', fontsize=30)
plt.xticks(rotation=45, fontsize=28)
plt.yticks(fontsize=28)
plt.legend(title='Sex', fontsize=28, title_fontsize=30, loc='upper left')
plt.grid(False)
plt.tight_layout()

# 保存和显示图表
plt.show()
