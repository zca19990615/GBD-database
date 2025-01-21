# -*- coding: utf-8 -*-
"""
Created on Tue Jul  2 12:32:06 2024

@author: 61967
"""

import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import itertools

# Load the data
file_path = 'C:\\Users\\61967\\Desktop\\GBD\\China\\总体趋势\\GLOBAL\\DALY.csv'
data = pd.read_csv(file_path)

# Filter data for all causes and the specified risk factor, considering all diseases up to 2021
data_filtered_all_updated = data[(data['rei'] == 'Low physical activity') & 
                                 (data['age'] == 'Age-standardized') & 
                                 (data['metric'] == 'Rate') & 
                                 (data['year'] <= 2021)]

# Pivot the data to have locations as columns
pivot_data_updated = data_filtered_all_updated.pivot_table(index='year', columns='location', values='val')

# Define the correct order for the legend with "Global" and "China" on top
correct_order = ["Global", "China"]

# Filter and reorder the pivot data to match the correct order
pivot_data_updated = pivot_data_updated[correct_order]

# Define unique markers and colors
markers = ['o', 's']
unique_markers = itertools.cycle(markers)
unique_colors = ['#1f77b4', '#d62728']  # Nature style blue and red

# Set the plotting style
sns.set(style="ticks")

# Create the plot
plt.figure(figsize=(14, 8))

# Plot each location with unique markers and colors ensuring no initial overlap
for idx, (location, color) in enumerate(zip(pivot_data_updated.columns, unique_colors)):
    plt.plot(pivot_data_updated.index, pivot_data_updated[location],
             marker=next(unique_markers), linestyle='-', color=color, label=location)

# Set the title and labels
plt.title('', fontsize=18, weight='bold')  # Increase title font size
plt.xlabel('Year', fontsize=16)  # Increase x-axis label font size
plt.ylabel('DALY Rate (per 100,000)', fontsize=16)  # Increase y-axis label font size

# Ensure that 2021 is labeled on the x-axis
plt.xticks(range(1990, 2022, 5), fontsize=14)  # Increase x-axis ticks font size
plt.yticks(fontsize=14)  # Increase y-axis ticks font size

# Remove grid lines
plt.grid(False)

# Customize spines
sns.despine()

# Set the legend at the upper right corner with larger font size
plt.legend(loc='upper right', frameon=False, fontsize=14)

# Show the plot
plt.tight_layout()
plt.show()
