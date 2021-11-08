#!/usr/bin/python

from pathlib import Path

import numpy as np
from netCDF4 import Dataset

import matplotlib.pyplot as plt
import cmocean.cm as cmo
import seaborn as sns
sns.set(style='ticks', context='paper', palette='colorblind')

import cartopy.crs as ccrs
import cartopy.feature as cfeature
from cartopy.mpl.ticker import LongitudeFormatter, LatitudeFormatter

# define rectangle over lab sea
bbay = [-80, -50, 65, 78]
# choose projection/transform
projection = ccrs.LambertConformal(central_latitude=70, central_longitude=-65)
transform = ccrs.PlateCarree()
# get bathymetry
bath_file = Path('/Users/GordonC/Documents/data/GEBCO/GEBCO_2020.nc')
bath = Dataset(bath_file)
blat = bath['lat'][:]
blon = bath['lon'][:]
elev = bath['elevation'][:]

ix = np.logical_and(blon > bbay[0] - 10, blon < bbay[1] + 10)
iy = np.logical_and(blat > bbay[2] - 10, blat < bbay[3] + 10)

blon = blon[ix]
blat = blat[iy]
elev = elev[iy,:]
elev = elev[:,ix]
elev = -np.ma.masked_array(elev.data, elev > 0)

# create figure, add coastlines
fig = plt.figure()
ax = fig.add_subplot(projection=projection)
ax.set_extent(bbay)
ax.add_feature(cfeature.GSHHSFeature('intermediate', edgecolor='black', facecolor='lightgray'))

# add bathymetry
im = ax.contourf(
    blon, blat, elev, list(range(0, 2600, 200)),
    transform=transform,
    cmap=cmo.deep,
    vmin=0, extend='max'
)
plt.colorbar(im, ax=ax, orientation='vertical', label='Depth (m)')

# plot floats
float_lats = [72.7392, 72.7367, 72.7384]
float_lons = [-66.9769, -66.9696, -66.9752]

for x, y in zip(float_lons, float_lats):
    ax.plot(x, y, marker='o', color='yellow', markeredgecolor='white', markersize=4, transform=transform)

# format map
lon_formatter = LongitudeFormatter(zero_direction_label=True)
lat_formatter = LatitudeFormatter()
gl = ax.gridlines(crs=transform, draw_labels=True)
gl.right_labels = False
gl.xformatter = lon_formatter
gl.yformatter = lat_formatter

fig.savefig(Path('../figures/baffin_bay_deployments.png'), dpi=350, bbox_inches='tight')
plt.close(fig)
