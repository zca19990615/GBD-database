# -*- coding: utf-8 -*-
"""
Created on Fri Jun 28 12:41:56 2024

@author: 61967
"""

# -*- coding: utf-8 -*-
"""
Created on Fri Jun 28 12:21:31 2024

@author: 61967
"""

import pandas as pd
import matplotlib.pyplot as plt
from matplotlib.ticker import FuncFormatter

# Load the CSV file
file_path = 'C:\\Users\\61967\\Desktop\\GBD\\Low physical activity\\作图\\年龄分布\\性别总趋势\\1.csv'
data = pd.read_csv(file_path)

# Filter data for "Deaths"
deaths_data = data[data['measure'] == 'Deaths']

# Separate data for Number and Rate
deaths_number = deaths_data[deaths_data['metric'] == 'Number']
deaths_rate = deaths_data[deaths_data['metric'] == 'Rate']

# Ensure all relevant columns are numeric
deaths_number[['val', 'upper', 'lower']] = deaths_number[['val', 'upper', 'lower']].apply(pd.to_numeric, errors='coerce')
deaths_rate[['val', 'upper', 'lower']] = deaths_rate[['val', 'upper', 'lower']].apply(pd.to_numeric, errors='coerce')

# Remove any remaining non-numeric rows
deaths_number_clean = deaths_number.dropna(subset=['val', 'upper', 'lower'])
deaths_rate_clean = deaths_rate.dropna(subset=['val', 'upper', 'lower'])

# Create the improved plot including data up to 2021 with all legends in the upper left, grid lines removed, right y-axis with vertical line, and aligned y-axis numbers including 100000 and 20
# Increase font sizes for better readability and adjust blue color for better visibility

fig, ax1 = plt.subplots(figsize=(14, 10))

# Define Lancet-inspired color palette with adjusted blue color for better visibility
colors = {'Male': '#0070C0', 'Female': '#ED0000'}

# Plot Number on the left y-axis
for sex in deaths_number_clean['sex'].unique():
    subset = deaths_number_clean[deaths_number_clean['sex'] == sex]
    ax1.bar(subset['year'], subset['val'], label=f'Number - {sex}', color=colors[sex], alpha=0.7)

ax1.set_xlabel('Year', fontsize=16)
ax1.set_ylabel('Number of Deaths', fontsize=16)
ax1.tick_params(axis='both', which='major', labelsize=14)

# Function to format y-axis labels
def y_fmt(x, _):
    return f'{int(x):,}'

# Apply the formatter to the left y-axis
ax1.yaxis.set_major_formatter(FuncFormatter(y_fmt))

# Create a second y-axis for Rate
ax2 = ax1.twinx()
for sex in deaths_rate_clean['sex'].unique():
    subset = deaths_rate_clean[deaths_rate_clean['sex'] == sex]
    ax2.plot(subset['year'], subset['val'], label=f'Rate - {sex}', color=colors[sex], marker='o')

ax2.set_ylabel('Death Rate per 100,000', fontsize=16)
ax2.spines['right'].set_position(('outward', 0))
ax2.spines['right'].set_visible(True)  # Ensure the right spine is visible
ax2.tick_params(axis='both', which='major', labelsize=14)

# Adjust y-axis limits and ticks to align numbers on both sides
ax1.set_ylim(0, 100000)
ax2.set_ylim(0, 17.5)
ax1.set_yticks([0, 100000, 200000, 300000, 400000, 500000])
ax2.set_yticks([0, 3.5, 7, 10.5, 14, 17.5])

# Combine legends and adjust positions
lines, labels = ax1.get_legend_handles_labels()
lines2, labels2 = ax2.get_legend_handles_labels()
ax1.legend(lines + lines2, labels + labels2, loc='upper left', fontsize=14)

# Remove grid lines
ax1.grid(False)
ax2.grid(False)

# Hide the top and right spines
ax1.spines['top'].set_visible(False)
ax2.spines['top'].set_visible(False)

plt.title('', fontsize=18)
plt.show()
