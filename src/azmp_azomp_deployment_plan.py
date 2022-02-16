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
atl = [-68, -42, 40, 62]
# choose projection/transform
projection = ccrs.LambertConformal(central_latitude=50, central_longitude=-57.5)
transform = ccrs.PlateCarree()

# load azmp + azomp stations
azmp = pd.read_csv(Path('../data/azmpStationsCore.txt'))
ar7w = pd.read_csv(Path('../data/AZOMP_AR7W_stn.csv'))

# create figure, add coastlines
fig = plt.figure(facecolor='beige')
ax = fig.add_subplot(projection=projection)
ax.set_extent(atl)
ax.add_feature(cfeature.GSHHSFeature('intermediate', edgecolor='black', facecolor='beige'))

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
cb = plt.colorbar(im, ax=ax, orientation='vertical', label='Depth (m)')
cb.ax.set_facecolor(fig.get_facecolor())

# plot stations
ms = 2
ax.plot(azmp.longitude, azmp.latitude, 'o', transform=transform, markersize=ms, label=None)
ax.plot(ar7w.lon_dd, ar7w.lat_dd, 'o', transform=transform, markersize=ms, label=None)

deploy = pd.read_csv(Path('../data/deployment-plan-spring-2022.csv'))
rbr_lats = deploy.Latitude[deploy.Model == 'ARVOR-I-RBR']
rbr_lons = deploy.Longitude[deploy.Model == 'ARVOR-I-RBR']
core_lats = deploy.Latitude[deploy.Model == 'ARVOR-I']
core_lons = deploy.Longitude[deploy.Model == 'ARVOR-I']
bgc_lats = deploy.Latitude[deploy.Model == 'ARVOR-I+O2']
bgc_lons = deploy.Longitude[deploy.Model == 'ARVOR-I+O2']

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

ns = [-68, -56, 40, 51]
ax.set_extent(ns)

# lab_sea = [-60, -45, 52, 61]
# ax.set_extent(lab_sea)

# save fig
fig.savefig(
    Path('../figures/azmp_azomp_deployments_2022_ns.png'), 
    dpi=350, bbox_inches='tight', facecolor=fig.get_facecolor(),
    edgecolor=None
)
plt.show()