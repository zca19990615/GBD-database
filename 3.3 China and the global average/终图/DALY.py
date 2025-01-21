# -*- coding: utf-8 -*-
"""
Created on Fri Jun 28 12:37:48 2024

@author: 61967
"""

import pandas as pd
import matplotlib.pyplot as plt

# Load the CSV file
file_path = 'C:\\Users\\61967\\Desktop\\GBD\\China\\总体趋势\\表\\1.csv'
data = pd.read_csv(file_path)

# Filter data for DALYs (Disability-Adjusted Life Years)
dalys_data = data[data['measure'] == 'DALYs (Disability-Adjusted Life Years)']

# Separate data for Number and Rate
dalys_number = dalys_data[dalys_data['metric'] == 'Number']
dalys_rate = dalys_data[dalys_data['metric'] == 'Rate']

# Ensure all relevant columns are numeric
dalys_number['val'] = pd.to_numeric(dalys_number['val'], errors='coerce')
dalys_number['upper'] = pd.to_numeric(dalys_number['upper'], errors='coerce')
dalys_number['lower'] = pd.to_numeric(dalys_number['lower'], errors='coerce')

dalys_rate['val'] = pd.to_numeric(dalys_rate['val'], errors='coerce')
dalys_rate['upper'] = pd.to_numeric(dalys_rate['upper'], errors='coerce')
dalys_rate['lower'] = pd.to_numeric(dalys_rate['lower'], errors='coerce')

# Remove any remaining non-numeric rows
dalys_number_clean = dalys_number.dropna(subset=['val', 'upper', 'lower'])
dalys_rate_clean = dalys_rate.dropna(subset=['val', 'upper', 'lower'])

# Create the improved plot for DALYs with Lancet-inspired colors and no top spines
fig, ax1 = plt.subplots(figsize=(14, 10))

# Define Lancet-inspired color palette with adjusted blue color for better visibility
colors = {'Male': '#0070C0', 'Female': '#ED0000'}

# Plot Number on the left y-axis
for sex in dalys_number_clean['sex'].unique():
    subset = dalys_number_clean[dalys_number_clean['sex'] == sex]
    ax1.bar(subset['year'], subset['val'], label=f'Number - {sex}', color=colors[sex], alpha=0.7)

ax1.set_xlabel('Year', fontsize=16)
ax1.set_ylabel('Number of DALYs', fontsize=16)
ax1.tick_params(axis='both', which='major', labelsize=14)

# Create a second y-axis for Rate
ax2 = ax1.twinx()
for sex in dalys_rate_clean['sex'].unique():
    subset = dalys_rate_clean[dalys_rate_clean['sex'] == sex]
    ax2.plot(subset['year'], subset['val'], label=f'Rate - {sex}', color=colors[sex], marker='o')

ax2.set_ylabel('DALY Rate per 100,000', fontsize=16)
ax2.spines['right'].set_position(('outward', 0))
ax2.spines['right'].set_visible(True)  # Ensure the right spine is visible
ax2.tick_params(axis='both', which='major', labelsize=14)

# Adjust y-axis limits and ticks to align numbers on both sides
ax1.set_ylim(0, 2000000)
ax2.set_ylim(0, 300)
ax1.set_yticks([0, 400000, 800000, 1200000, 1600000, 2000000])
ax2.set_yticks([0, 60, 120, 180, 240, 300])

# Format the y-tick labels to normal numbers
ax1.get_yaxis().set_major_formatter(plt.FuncFormatter(lambda x, loc: "{:,}".format(int(x))))

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
