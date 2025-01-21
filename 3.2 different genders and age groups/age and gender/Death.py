# -*- coding: utf-8 -*-
"""
Created on Tue Jul  2 16:29:34 2024

@author: 61967
"""

import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# 加载数据
file_path = 'C:\\Users\\61967\\Desktop\\GBD\\China\\年龄段\\中国\\Death china.csv'
data = pd.read_csv(file_path)

# 过滤数据，仅保留 "Low physical activity" 和 2021年的数据
filtered_activity_data = data[(data['rei'] == 'Low physical activity') & (data['year'] == 2021)]

# 创建透视表，索引为年龄组，列为性别，值为DALYs率
pivot_activity_data = filtered_activity_data.pivot_table(index='age', columns='sex', values='val')

# 设置风格为自然风格
sns.set(style="whitegrid")

# 修改配色
colors = {'Male': '#3498db', 'Female': '#e74c3c', 'Both': '#FF8C00'}  # 蓝色、红色和橙色

# 设置字体大小
plt.rcParams.update({'font.size': 30})  # 更新全局字体大小

# 绘制并排柱状图和折线图
fig, ax1 = plt.subplots(figsize=(24, 18))

# 绘制柱状图
bars = pivot_activity_data[['Male', 'Female']].plot(kind='bar', color=[colors['Male'], colors['Female']], ax=ax1, width=0.8)

# 绘制折线图
ax1.plot(pivot_activity_data.index, pivot_activity_data['Both'], color=colors['Both'], marker='o', markersize=10, linewidth=6, label='Both')

# 设置标题和标签
ax1.set_title('', fontsize=30)
ax1.set_xlabel('Age Group', fontsize=30)
ax1.set_ylabel('Death Rate (per 100,000)', fontsize=30)

# 设置x轴和y轴刻度
ax1.set_xticklabels(pivot_activity_data.index, rotation=45, fontsize=28)
ax1.tick_params(axis='y', labelsize=28)

# 设置图例，将 "Both" 合并到左上角的图例中
lines, labels = ax1.get_legend_handles_labels()
ax1.legend(lines, labels, fontsize=28, title='Sex', title_fontsize=30, loc='upper left')

# 去除网格线
ax1.grid(False)

# 显示和保存图表
plt.tight_layout()
plt.show()

