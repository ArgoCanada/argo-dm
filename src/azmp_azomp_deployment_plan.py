#!/usr/bin/python

from pathlib import Path

import numpy as np
import pandas as pd
from netCDF4 import Dataset

import matplotlib.pyplot as plt
import cmocean.cm as cmo
import seaborn as sns
sns.set(style='ticks', context='paper', palette='colorblind')

import cartopy.crs as ccrs
import cartopy.feature as cfeature
from cartopy.mpl.ticker import LongitudeFormatter, LatitudeFormatter

# define rectangle around atlantic canada
atl = [-68, -48, 40, 62]
# choose projection/transform
projection = ccrs.LambertConformal(central_latitude=50, central_longitude=-57.5)
transform = ccrs.PlateCarree()

# load azmp + azomp stations
azmp = pd.read_csv(Path('../data/azmpStationsCore.txt'))
ar7w = pd.read_csv(Path('../data/AZOMP_AR7W_stn.csv'))

# create figure, add coastlines
fig = plt.figure()
ax = fig.add_subplot(projection=projection)
ax.set_extent(atl)
ax.add_feature(cfeature.GSHHSFeature('intermediate', edgecolor='black', facecolor='lightgray'))

# get bathymetry
bath_file = Path('/Users/GordonC/Documents/data/GEBCO/GEBCO_2020.nc')
bath = Dataset(bath_file)
blat = bath['lat'][:]
blon = bath['lon'][:]
elev = bath['elevation'][:]

ix = np.logical_and(blon > atl[0] - 10, blon < atl[1] + 10)
iy = np.logical_and(blat > atl[2] - 10, blat < atl[3] + 10)

blon = blon[ix]
blat = blat[iy]
elev = elev[iy,:]
elev = elev[:,ix]
elev = -np.ma.masked_array(elev.data, elev > 0)

# add bathymetry
im = ax.contourf(
    blon, blat, elev, list(range(0, 3800, 200)),
    transform=transform,
    cmap=cmo.deep,
    vmin=0, extend='max'
)
plt.colorbar(im, ax=ax, orientation='vertical', label='Depth (m)')

# plot stations
ms = 2
ax.plot(azmp.longitude, azmp.latitude, 'o', transform=transform, markersize=ms, label=None)
ax.plot(ar7w.lon_dd, ar7w.lat_dd, 'o', transform=transform, markersize=ms, label=None)

rbr_lats = [41.414172, 57.800000, 58.216667]
rbr_lons = [-60.664633, -51.340000, -50.883333]
core_lats = rbr_lats + [43.783300, 41.776870,  56.956667, 59.066667]
core_lons = rbr_lons + [-57.833300, -60.906963,  -52.236667, -49.950000]
bgc_lats = [42.475000, 42.026080, 43.473300, 57.376667, 58.640000, 56.536667, 59.483333]
bgc_lons = [-61.433300, -61.068143, -57.526700, -51.791667, -50.416667, -52.678333, -49.475000]

ms = 6
ax.plot(core_lons, core_lats, '*', label='CTD', markersize=ms, transform=transform)
ax.plot(rbr_lons, rbr_lats, '*', label='RBR + CTD Buddy', markersize=ms, transform=transform)
ax.plot(bgc_lons, bgc_lats, '*', label='CTD+DO', markersize=ms, transform=transform)
ax.legend()

# format map
lon_formatter = LongitudeFormatter(zero_direction_label=True)
lat_formatter = LatitudeFormatter()
gl = ax.gridlines(crs=transform, draw_labels=True)
gl.right_labels = False
gl.xformatter = lon_formatter
gl.yformatter = lat_formatter

# ns = [-68, -56, 40, 51]
# ax.set_extent(ns)

# lab_sea = [-60, -45, 52, 61]
# ax.set_extent(lab_sea)

# save fig
fig.savefig(Path('../figures/azmp_azomp_deployments_2022.png'), dpi=350, bbox_inches='tight')

plt.show()