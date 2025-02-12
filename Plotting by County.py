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

# Loading County Specific Dataset
county_df = pd.read_excel(puma_df, sheet_name = "Household Count on County", header = 5)

county_df.columns

# Limiting the dataset to the continental USA
household_count_cols = ['County','County_12',
       'County_13', 'County_14', 'County_15', 'County_16', 'County_17',
       'County_18', 'County_19', 'County_21', 'County_22', 'County_23']

data_cols = ['County_12',
       'County_13', 'County_14', 'County_15', 'County_16', 'County_17',
       'County_18', 'County_19', 'County_21', 'County_22', 'County_23']

county_df_vals = county_df[household_count_cols]

# dropping all counties with less than 1 household and converting to whole numbers

for cols in data_cols:
    county_df_vals = county_df_vals[county_df_vals[cols] > 1]
    county_df_vals[cols] = county_df_vals[cols].astype(int)



# Load US counties shapefile
counties = gpd.read_file('https://www2.census.gov/geo/tiger/TIGER2019/COUNTY/tl_2019_us_county.zip')

# Split county name and state from the County column
county_df_vals[['County_Name', 'State']] = county_df_vals['County'].str.rsplit(' ', n=1, expand=True)

# Convert county names to uppercase for matching
counties['NAME'] = counties['NAME'].str.upper()
county_df_vals['County_Name'] = county_df_vals['County_Name'].str.upper()

# Create a state FIPS to state abbreviation mapping
state_fips = {
    '01':'AL', '02':'AK', '04':'AZ', '05':'AR', '06':'CA', '08':'CO', '09':'CT',
    '10':'DE', '11':'DC', '12':'FL', '13':'GA', '15':'HI', '16':'ID', '17':'IL',
    '18':'IN', '19':'IA', '20':'KS', '21':'KY', '22':'LA', '23':'ME', '24':'MD',
    '25':'MA', '26':'MI', '27':'MN', '28':'MS', '29':'MO', '30':'MT', '31':'NE',
    '32':'NV', '33':'NH', '34':'NJ', '35':'NM', '36':'NY', '37':'NC', '38':'ND',
    '39':'OH', '40':'OK', '41':'OR', '42':'PA', '44':'RI', '45':'SC', '46':'SD',
    '47':'TN', '48':'TX', '49':'UT', '50':'VT', '51':'VA', '53':'WA', '54':'WV',
    '55':'WI', '56':'WY'
}

# Convert FIPS to state abbreviations in counties dataframe
counties['STATE_ABBR'] = counties['STATEFP'].map(state_fips)

# Create state-county pairs for matching using state abbreviations
counties['state_county'] = counties['NAME'] + '_' + counties['STATE_ABBR']
county_df_vals['state_county'] = county_df_vals['County_Name'] + '_' + county_df_vals['State']

# Merge the dataframes
merged_df = counties.merge(county_df_vals, how='right', left_on='state_county', right_on='state_county')

# Create figure and axis with projection
fig, ax = plt.subplots(figsize=(15, 10), subplot_kw={'projection': ccrs.PlateCarree()})

# Set map extent to continental US
ax.set_extent([-125, -66, 24.5, 49.5], crs=ccrs.PlateCarree())

# Add state boundaries and coastlines
ax.add_feature(cfeature.STATES, edgecolor='gray', linewidth=0.5)
ax.add_feature(cfeature.COASTLINE)

# Calculate 10th and 90th percentiles for color normalization
vmin = np.percentile(county_df_vals['County_13'], 5) # Keep 2013 as the base year
vmax = np.percentile(county_df_vals['County_13'], 95)

# Create color normalization
norm = Normalize(vmin=vmin, vmax=vmax)

# Plot counties
merged_df.plot(column='County_23',  # Changing Column Name to 2012 , 2013, 2014, 2015, 2016, 2017, 2018, 2019, 2021, 2022, 2023
              ax=ax,
              transform=ccrs.PlateCarree(),
              cmap='viridis',
              norm=norm,
              legend=True,
              legend_kwds={'label': 'Household Count 2023'}) # Change label based on the year used

plt.title('US County Household Counts (2023)')
plt.savefig(os.path.join(save_path_vals, 'US County Household Counts (2023).png')) # Change file name based on the year used
plt.savefig(os.path.join(save_path_vals, 'US County Household Counts (2023).svg'))
plt.show()



### Calculating the percentage change in household count from 2019 to 2023 (year over year)

county_df_vals['pct_change_23v19'] = (((county_df_vals['County_23'] - county_df_vals['County_19']) / county_df_vals['County_19']) * 100)/4 # Dividing by 4 to get the average annual percentage change
county_df_vals['pct_change_23v22'] = ((county_df_vals['County_23'] - county_df_vals['County_22']) / county_df_vals['County_22']) * 100
county_df_vals['pct_change_22v21'] = ((county_df_vals['County_22'] - county_df_vals['County_21']) / county_df_vals['County_21']) * 100
county_df_vals['pct_change_21v19'] = (((county_df_vals['County_21'] - county_df_vals['County_19']) / county_df_vals['County_19']) * 100)/2 # Dividing by 2 to get the average annual percentage change


top_10_change_23v19 = county_df_vals.sort_values(by='pct_change_23v19', ascending=False).head(20)
top_10_change_23v22 = county_df_vals.sort_values(by='pct_change_23v22', ascending=False).head(20)
top_10_change_22v21 = county_df_vals.sort_values(by='pct_change_22v21', ascending=False).head(20)
top_10_change_21v19 = county_df_vals.sort_values(by='pct_change_21v19', ascending=False).head(20)

# Plotting the top 10 counties with the highest percentage change in household count from 2019 to 2023
plt.figure(figsize=(15, 10))
plt.bar(top_10_change_23v19['County'], top_10_change_23v19['pct_change_23v19'])
plt.ylabel('Percentage Change in Household Count')
plt.xlabel('County')
plt.xticks(rotation=90)
plt.title('Top 20 Counties with the Highest\nPercentage Change in Household Count from 2019 to 2023')
plt.tight_layout()
plt.savefig(os.path.join(save_path_pct, 'Top 20 Counties with the Highest Percentage Change in Household Count from 2019 to 2023.png'))
plt.savefig(os.path.join(save_path_pct, 'Top 20 Counties with the Highest Percentage Change in Household Count from 2019 to 2023.svg'))
plt.show()

# Plotting the top 10 counties with the highest percentage change in household count from 2019 to 2021
plt.figure(figsize=(15, 10))
plt.bar(top_10_change_21v19['County'], top_10_change_21v19['pct_change_21v19'])
plt.ylabel('Percentage Change in Household Count')
plt.xlabel('County')
plt.xticks(rotation=90)
plt.title('Top 20 Counties with the Highest\nPercentage Change in Household Count from 2019 to 2021')
plt.tight_layout()
plt.savefig(os.path.join(save_path_pct, 'Top 20 Counties with the Highest Percentage Change in Household Count from 2019 to 2021.png'))
plt.savefig(os.path.join(save_path_pct, 'Top 20 Counties with the Highest Percentage Change in Household Count from 2019 to 2021.svg'))
plt.show()

# Plotting the top 10 counties with the highest percentage change in household count from 2022 to 2023
plt.figure(figsize=(15, 10))
plt.bar(top_10_change_23v22['County'], top_10_change_23v22['pct_change_23v22'])
plt.ylabel('Percentage Change in Household Count')
plt.xlabel('County')
plt.xticks(rotation=90)
plt.title('Top 20 Counties with the Highest\nPercentage Change in Household Count from 2022 to 2023')
plt.tight_layout()
plt.savefig(os.path.join(save_path_pct, 'Top 20 Counties with the Highest Percentage Change in Household Count from 2022 to 2023.png'))
plt.savefig(os.path.join(save_path_pct, 'Top 20 Counties with the Highest Percentage Change in Household Count from 2022 to 2023.svg'))
plt.show()

# plotting the top 10 counties with the highest percentage change in household count from 2021 to 2022
plt.figure(figsize=(15, 10))
plt.bar(top_10_change_22v21['County'], top_10_change_22v21['pct_change_22v21'])
plt.ylabel('Percentage Change in Household Count')
plt.xlabel('County')
plt.xticks(rotation=90)
plt.title('Top 20 Counties with the Highest\nPercentage Change in Household Count from 2021 to 2022')
plt.tight_layout()
plt.savefig(os.path.join(save_path_pct, 'Top 20 Counties with the Highest Percentage Change in Household Count from 2021 to 2022.png'))
plt.savefig(os.path.join(save_path_pct, 'Top 20 Counties with the Highest Percentage Change in Household Count from 2021 to 2022.svg'))
plt.show()



county_df_vals.head()








