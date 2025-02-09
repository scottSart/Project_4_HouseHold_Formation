import pandas as pd
import os
import matplotlib.pyplot as plt
import cartopy.crs as ccrs
import cartopy.feature as cfeature
import numpy as np
from matplotlib.colors import Normalize



# File Paths
BASE_DIR = os.path.dirname(os.path.abspath(__name__))

# Deining Datapaths
puma_df = os.path.join(BASE_DIR, "Raw Data", "Consolidated Dataset.xlsx")

# Loading Dataset
consolidated_df = pd.read_excel(puma_df, header = 2)

consolidated_df.head()

# defining the household count dataset

household_cols = ['2012 GEO_ID', '2012 PUMA Names', '2012 PUMA Clean Names',
       '2022 PUMA Names', '2022 PUMA Clean Names', 'House_ct_2010',
       'House_ct_2011', 'House_ct_2012', 'House_ct_2013', 'House_ct_2014',
       'House_ct_2015', 'House_ct_2016', 'House_ct_2017', 'House_ct_2018',
       'House_ct_2019', 'House_ct_2021', 'House_ct_2022', 'House_ct_2023','CENTLAT', 'CENTLON', 'INTPTLAT', 'INTPTLON']

household_counts = consolidated_df[household_cols]

# liming the dataset to the continental USA

##############################################################
###### Visualization for 2011 (TESTING) ######
##############################################################

    # Filter for continental USA

household_counts_US = household_counts[
    (household_counts['CENTLAT'].between(24.5, 49.5)) & 
    (household_counts['CENTLON'].between(-125, -66))
][['CENTLAT', 'CENTLON', 'House_ct_2010','House_ct_2011','House_ct_2012', 'House_ct_2013', 'House_ct_2014',
       'House_ct_2015', 'House_ct_2016', 'House_ct_2017', 'House_ct_2018',
       'House_ct_2019', 'House_ct_2021', 'House_ct_2022', 'House_ct_2023']].dropna()


    # Avoid LogNorm issue with zero values
household_counts_US['House_ct_2011'] = household_counts_US['House_ct_2011'].replace(0, 1e-1)
    # household_counts_US['House_ct_2010'] = household_counts_US['House_ct_2010'].replace(0, 1e-1)

    # Create figure and map projection
fig, ax = plt.subplots(figsize=(15, 10), subplot_kw={'projection': ccrs.PlateCarree()})

    # Set map extent to zoom into the US
ax.set_extent([-125, -66, 24.5, 50], crs=ccrs.PlateCarree())

    # Add coastlines and state borders for better context
ax.add_feature(cfeature.COASTLINE)
ax.add_feature(cfeature.STATES, edgecolor='gray', linewidth=0.5)

    # Use LogNorm to improve contrast with adjusted scale
norm = plt.Normalize(vmin=household_counts_US['House_ct_2010'].min(), 
                    vmax=household_counts_US['House_ct_2023'].max())

    # Scatter plot with larger points and adjusted transparency
scatter = ax.scatter(household_counts_US['CENTLON'], household_counts_US['CENTLAT'], 
                    c=household_counts_US['House_ct_2010'], 
                    cmap='viridis',
                    norm=norm,
                    alpha=0.8, 
                    edgecolor='white',
                    linewidth=0.5,
                    s=100)

    # Add color bar with better formatting
cbar = plt.colorbar(scatter, ax=ax, orientation='vertical', shrink=0.7, pad=0.02)
cbar.set_label('Household Counts (2010)', size=12)
cbar.ax.tick_labels = [f'{x:,.0f}' for x in cbar.get_ticks()]  # Format numbers with commas

    # Labels and title with improved formatting
ax.set_title('Household Counts by Location (2010)', pad=20, size=14)
ax.set_xlabel('Longitude', size=12)
ax.set_ylabel('Latitude', size=12)

    # Add gridlines for better reference
ax.gridlines(draw_labels=True, linewidth=0.5, color='gray', alpha=0.5)

plt.tight_layout()
plt.show()


#############################################################################
###### CODING FOR HOUSEHOLD COUNTS BETWEEN 2010 AND 2023, EXCEPT 2020 #######
#############################################################################


# List out the years you want to plot
years = [2010, 2011, 2012, 2013, 2014, 2015, 
         2016, 2017, 2018, 2019, 2021, 2022, 2023]

# Calculate the global min and max across all selected years for consistent color scaling
vmin = 25367 # based on the min value of 2013
vmax = 120000 # based on the max value of 2023

# Create a Normalize object for all plots
norm = Normalize(vmin=vmin, vmax=vmax)

# Specify the colormap (viridis was used in the original example)
cmap = 'viridis'

# Loop over each year and create a map
for yr in years:
    # Create figure and cartopy projection
    fig, ax = plt.subplots(figsize=(15, 10), subplot_kw={'projection': ccrs.PlateCarree()})
    
    # Set map extent for the continental US
    ax.set_extent([-125, -66, 24.5, 50], crs=ccrs.PlateCarree())
    
    # Add map context
    ax.add_feature(cfeature.COASTLINE)
    ax.add_feature(cfeature.STATES, edgecolor='gray', linewidth=0.5)
    
    # Scatter plot for this year's data
    scatter = ax.scatter(
        household_counts_US['CENTLON'], 
        household_counts_US['CENTLAT'],
        c=household_counts_US[f'House_ct_{yr}'],
        cmap=cmap,
        norm=norm,
        alpha=0.8,
        edgecolor='white',
        linewidth=0.5,
        s=100
    )
    
    # Add colorbar
    cbar = plt.colorbar(scatter, ax=ax, orientation='vertical', shrink=0.7, pad=0.02)
    cbar.set_label(f'Household Counts ({yr})', size=12)
    
    # Optionally format colorbar ticks with commas:
    cbar.ax.set_yticklabels([f'{x:,.0f}' for x in cbar.get_ticks()])

    # Title, axes, and grid
    ax.set_title(f'Household Counts by Location ({yr})', pad=20, size=14)
    ax.set_xlabel('Longitude', size=12)
    ax.set_ylabel('Latitude', size=12)
    
    # Add gridlines
    gl = ax.gridlines(draw_labels=True, linewidth=0.5, color='gray', alpha=0.5)
    gl.top_labels = False
    gl.right_labels = False
    
    # Adjust layout
    plt.tight_layout()
    
    # Save figure as PNG and SVG
    plt.savefig(f'household_counts_{yr}.png', dpi=300)
    plt.savefig(f'household_counts_{yr}.svg', dpi=300)
    
    # Close the figure to free memory
    plt.close(fig)


##############################################################
###### Creating a visualization for the percent changes ######
##############################################################

    # Create a new dataframe with lat/long and calculate year-over-year changes
yoy_changes = household_counts_US[['CENTLAT', 'CENTLON']].copy()


    # Calculate year-over-year percent changes
for year in range(2013, 2024):
    if year == 2020:
        yoy_changes[f'pct_change_{year}'] = 0
    elif year == 2021:
        # For 2021, use 2019 as base year
        base_year = 2019
        yoy_changes[f'pct_change_{year}'] = (
            (household_counts_US[f'House_ct_{2021}'] - household_counts_US[f'House_ct_{base_year}']) / 
            household_counts_US[f'House_ct_{base_year}'] * 100
        )
    else:
        base_year = year - 1
        
        yoy_changes[f'pct_change_{year}'] = (
            (household_counts_US[f'House_ct_{year}'] - household_counts_US[f'House_ct_{base_year}']) / 
            household_counts_US[f'House_ct_{base_year}'] * 100
        )


# Round the percent changes to 2 decimal places
pct_cols = [col for col in yoy_changes.columns if 'pct_change' in col]
yoy_changes[pct_cols] = yoy_changes[pct_cols].round(2)

# Creating output directory for percent change plots
os.makedirs('output_pct', exist_ok=True)

# List out the years for percent change plots (2011-2023, excluding 2020)
years = list(range(2013, 2020)) + list(range(2021, 2024))

# Calculate the global min and max of percent changes for consistent color scaling
vmin = -25
vmax = 25

# Create a Normalize object for all plots
norm = Normalize(vmin=vmin, vmax=vmax)

# Specify the colormap - using RdYlBu_r for better visualization of positive/negative changes
cmap = 'RdYlBu_r'

# Loop over each year and create a map
for yr in years:
    # Create figure and cartopy projection
    fig, ax = plt.subplots(figsize=(15, 10), subplot_kw={'projection': ccrs.PlateCarree()})
    
    # Set map extent for the continental US
    ax.set_extent([-125, -66, 24.5, 50], crs=ccrs.PlateCarree())
    
    # Add map context
    ax.add_feature(cfeature.COASTLINE)
    ax.add_feature(cfeature.STATES, edgecolor='gray', linewidth=0.5)
    
    # Scatter plot for this year's percent change data
    scatter = ax.scatter(
        yoy_changes['CENTLON'],
        yoy_changes['CENTLAT'],
        c=yoy_changes[f'pct_change_{yr}'],
        cmap=cmap,
        norm=norm,
        alpha=0.8,
        edgecolor='white',
        linewidth=0.5,
        s=100
    )
    
    # Add colorbar
    cbar = plt.colorbar(scatter, ax=ax, orientation='vertical', shrink=0.7, pad=0.02)
    cbar.set_label(f'Percent Change in Household Counts ({yr-1} to {yr})', size=12)
    
    # Format colorbar ticks as percentages
    cbar.ax.set_yticklabels([f'{x:,.1f}%' for x in cbar.get_ticks()])

    # Title, axes, and grid
    if yr == 2021:
        title = f'Percent Change in Household Counts (2019 to 2021)'
    else:
        title = f'Percent Change in Household Counts ({yr-1} to {yr})'
    ax.set_title(title, pad=20, size=14)
    ax.set_xlabel('Longitude', size=12)
    ax.set_ylabel('Latitude', size=12)
    
    # Add gridlines
    gl = ax.gridlines(draw_labels=True, linewidth=0.5, color='gray', alpha=0.5)
    gl.top_labels = False
    gl.right_labels = False
    
    # Adjust layout
    plt.tight_layout()
    
    # Save figure as PNG and SVG in the output_pct directory
    plt.savefig(os.path.join('output_pct', f'household_counts_pct_change_{yr}.png'), dpi=300)
    plt.savefig(os.path.join('output_pct', f'household_counts_pct_change_{yr}.svg'), dpi=300)
    
    # Close the figure to free memory
    plt.close(fig)
