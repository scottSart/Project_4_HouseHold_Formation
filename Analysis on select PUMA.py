import os
import pandas as pd
import geopandas as gpd
import matplotlib.pyplot as plt
import cartopy.crs as ccrs
import cartopy.feature as cfeature
from matplotlib.colors import Normalize
import numpy as np

BASE_DIR = os.path.dirname(os.path.abspath(__name__))

# Loading Dataset
puma_df = os.path.join(BASE_DIR, "Raw Data", "Consolidated Dataset.xlsx")
save_path_vals = os.path.join(BASE_DIR, "output_values")
save_path_pct = os.path.join(BASE_DIR, "output_pct")

# Loading the dataset
county_df = pd.read_excel(puma_df, sheet_name = "Converting PUMA - County", header = 1)

# Identifying the year over year changes for the selected PUMA

county_df['pct_change_21v19'] = 100*(county_df['Count_21'] - county_df['Count_19']) / county_df['Count_19']
county_df['pct_change_22v21'] = 100*(county_df['Count_22'] - county_df['Count_21']) / county_df['Count_21']
county_df['pct_change_23v22'] = 100*(county_df['Count_23'] - county_df['Count_22']) / county_df['Count_22']
county_df['pct_change_23v19'] = 100*(county_df['Count_23'] - county_df['Count_19']) / county_df['Count_19']

# Identifying the top 20 counties with the highest percentage change in household count from 2019 to 2021
top_20_change_21v19 = county_df.sort_values(by = 'pct_change_21v19', ascending = False).head(20)

# Identifying the top 20 counties with the highest percentage change in household count from 2022 to 2023
top_20_change_23v22 = county_df.sort_values(by = 'pct_change_23v22', ascending = False).head(20)

# Identifying the top 20 counties with the highest percentage change in household count from 2019 to 2023
top_20_change_23v19 = county_df.sort_values(by = 'pct_change_23v19', ascending = False).head(20)

# Identifying the top 20 counties with the highest percentage change in household count from 2021 to 2022
top_20_change_22v21 = county_df.sort_values(by = 'pct_change_22v21', ascending = False).head(20)

# Plotting the top 20 counties with the highest percentage change in household count from 2019 to 2021
plt.figure(figsize=(15, 10))
plt.bar(top_20_change_21v19['County ID_22'], top_20_change_21v19['pct_change_21v19'])
plt.ylabel('Percentage Change in Household Count')
plt.xlabel('County')
plt.xticks(rotation=90)
plt.title('Top 20 Counties with the Highest Percentage Change in Household Count from 2019 to 2021')
plt.tight_layout()
plt.savefig(os.path.join(save_path_pct, 'Top 20 Counties with the Highest Percentage Change in Household Count from 2019 to 2021_v2.png'))
plt.savefig(os.path.join(save_path_pct, 'Top 20 Counties with the Highest Percentage Change in Household Count from 2019 to 2021_v2.svg'))
plt.show()

# Plotting the top 20 counties with the highest percentage change in household count from 2021 to 2022
plt.figure(figsize=(15, 10))
plt.bar(top_20_change_22v21['County ID_22'], top_20_change_22v21['pct_change_22v21'])
plt.ylabel('Percentage Change in Household Count')
plt.xlabel('County')
plt.xticks(rotation=90)
plt.title('Top 20 Counties with the Highest Percentage Change in Household Count from 2021 to 2022')
plt.tight_layout()
plt.savefig(os.path.join(save_path_pct, 'Top 20 Counties with the Highest Percentage Change in Household Count from 2021 to 2022_v2.png'))
plt.savefig(os.path.join(save_path_pct, 'Top 20 Counties with the Highest Percentage Change in Household Count from 2021 to 2022_v2.svg'))
plt.show()

top_20_change_22v21[['Adj_Count_21','Adj_Count_22']]

top_20_change_22v21.columns

