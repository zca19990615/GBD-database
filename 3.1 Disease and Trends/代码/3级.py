# -*- coding: utf-8 -*-
"""
Created on Tue Jun 18 16:55:03 2024

@author: 61967
"""

# -*- coding: utf-8 -*-
"""
Created on Tue May 28 16:03:07 2024

@author: 61967
"""

import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import itertools

# Load the data
file_path = 'C:\\Users\\61967\\Desktop\\GBD\\China\\不同疾病趋势\\IHME-GBD_2021_DATA-d777f156-1.csv'
data = pd.read_csv(file_path)

# Filter data for all causes and the specified risk factor, considering all diseases up to 2021
data_filtered_all_updated = data[(data['rei'] == 'Low physical activity') & 
                                 (data['sex'] == 'Both') & 
                                 (data['metric'] == 'Rate') & 
                                 (data['year'] <= 2021)]

# Pivot the data to have diseases as columns
pivot_data_updated = data_filtered_all_updated.pivot_table(index='year', columns='cause', values='val')

# Define the correct order for the legend with "Tuberculosis" on top
correct_order = [
    "Tuberculosis",
    "Colon and rectum cancer",
    "Breast cancer",
    "Ischemic heart disease",
    "Stroke",
    "Lower extremity peripheral\narterial disease",
    "Diabetes mellitus",
    "Chronic kidney disease"
]

# Map original causes to new formatted causes
cause_mapping = {
    "Tuberculosis": "Tuberculosis",
    "Colon and rectum cancer": "Colon and rectum cancer",
    "Breast cancer": "Breast cancer",
    "Ischemic heart disease": "Ischemic heart disease",
    "Stroke": "Stroke",
    "Lower extremity peripheral arterial disease": "Lower extremity peripheral\narterial disease",
    "Diabetes mellitus": "Diabetes mellitus",
    "Chronic kidney disease": "Chronic kidney disease"
}

# Rename columns in pivot_data_updated
pivot_data_updated = pivot_data_updated.rename(columns=cause_mapping)

# Filter and reorder the pivot data to match the correct order
pivot_data_updated = pivot_data_updated[correct_order]

# Define unique markers and colors
markers = ['o', 's', 'D', '^', 'v', '<', '>', 'p', 'P', '*', 'h', 'H', 'x', 'X', '+', 'd', '|', '_', '8', '1']
unique_markers = itertools.cycle(markers)
unique_colors = sns.color_palette("husl", n_colors=len(pivot_data_updated.columns))

# Set the plotting style
sns.set(style="whitegrid")

# Create the plot
plt.figure(figsize=(14, 8))

# Plot each disease with unique markers and colors ensuring no initial overlap
for idx, (disease, color) in enumerate(zip(pivot_data_updated.columns, unique_colors)):
    plt.plot(pivot_data_updated.index, pivot_data_updated[disease],
             marker=next(unique_markers), linestyle='-', color=color, label=disease)

# Set the title and labels
plt.title('', fontsize=16)
plt.xlabel('Year', fontsize=14)
plt.ylabel('Deaths Rate (per 100,000)', fontsize=14)

# Ensure that 2021 is labeled on the x-axis
plt.xticks(range(1990, 2022, 5))

# Set the grid to be dashed lines with larger spacing
plt.grid(True, linestyle='--', linewidth=0.7, dashes=(5, 10))

# Set the legend outside of the plot
plt.legend(loc='center left', bbox_to_anchor=(1, 0.5))

# Show the plot
plt.tight_layout()
# Save the plot with high resolution
plt.savefig('resolution_plot3.png', dpi=1200)


plt.show()
