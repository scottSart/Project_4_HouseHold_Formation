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
sec_attempt = os.path.join(BASE_DIR,"2nd Attempt", "Consolidated Dataset_v2.xlsx")

# Loading the dataset
puma_df = pd.read_excel(sec_attempt, sheet_name = "Aggr Values from_Tr 2022 Data", header = 5)

## Clearing all NAN Values
puma_vals =puma_df[19:]

puma_vals.head()

# Restricting the dataset to the necessary columns
puma_vals_wide = puma_vals[['State abbr.',  'PUMA12 name',           2012,
                 2013,           2014,           2015,           2016,
                 2017,           2018,           2019,           2021,
                 2022,           2023]]

# Rounding the values to the nearest integer
puma_vals_wide[2022]=puma_vals_wide[2022].round(0)
puma_vals_wide[2023]=puma_vals_wide[2023].round(0)

# Identifying 2023 v 2022 changes
puma_vals_wide['Abs_2023v2012'] = puma_vals_wide[2023] - puma_vals_wide[2012]
puma_vals_wide['Pct_2023v2012'] = (puma_vals_wide[2023] - puma_vals_wide[2012])*100/puma_vals_wide[2012]

# Identifying 2023 v 2019 changes
puma_vals_wide['Abs_2023v2019'] = puma_vals_wide[2023] - puma_vals_wide[2019]
puma_vals_wide['Pct_2023v2019'] = (puma_vals_wide[2023] - puma_vals_wide[2019])*100/puma_vals_wide[2019]

puma_vals_wide.head()

# Identifying the top 20 PUMA with the highest percentage change in household count from 2019 to 2023
top_20_change_23v19 = puma_vals_wide.sort_values(by = 'Pct_2023v2019', ascending = False).head(20)

# Plotting the top 20 PUMA with the highest percentage change in household count from 2019 to 2023
plt.figure(figsize=(15, 10))    
plt.bar(top_20_change_23v19['PUMA12 name'], top_20_change_23v19['Pct_2023v2019'])
plt.ylabel('Percentage Change in Household Count')
plt.xlabel('PUMA')
plt.xticks(rotation=90)
plt.title('Top 20 PUMA with the Highest Percentage Change in Household Count from 2019 to 2023')
plt.tight_layout()
# plt.savefig(os.path.join(BASE_DIR, "Output", "Top 20 PUMA with the Highest Percentage Change in Household Count from 2019 to 2023.png"))
plt.show()

# Identifying the top 20 PUMA with the highest percentage change in household count from 2012 to 2023
top_20_change_23v12 = puma_vals_wide.sort_values(by = 'Pct_2023v2012', ascending = False).head(20)

# Plotting the top 20 PUMA with the highest percentage change in household count from 2012 to 2023
plt.figure(figsize=(15, 10))
plt.bar(top_20_change_23v12['PUMA12 name'], top_20_change_23v12['Pct_2023v2012'])
plt.ylabel('Percentage Change in Household Count')
plt.xlabel('PUMA')
plt.xticks(rotation=90)
plt.tight_layout()
plt.show()