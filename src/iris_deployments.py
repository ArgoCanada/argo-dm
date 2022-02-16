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

# define rectangle around atlantic ocean
atl = [-85, 10, -20, 40]
# choose projection/transform
projection = ccrs.PlateCarree()
transform = ccrs.PlateCarree()

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
# subset to make smaller
M, N = elev.shape
sx = range(0, N, 10)
sy = range(0, M, 10)
blon = blon[sx]
blat = blat[sy]
elev = elev[sy, :]
elev = elev[:, sx]
elev = -np.ma.masked_array(elev.data, elev > 0)

# add bathymetry
im = ax.contourf(
    blon, blat, elev, list(range(0, 5000, 250)),
    transform=transform,
    cmap=cmo.deep,
    vmin=0, extend='max'
)
cb = plt.colorbar(im, ax=ax, orientation='vertical', label='Depth (m)')
cb.ax.set_facecolor(fig.get_facecolor())

# get iris deployment file
fn = Path('/Users/GordonC/Documents/argo/meds/ocean-ops/IRIS-ArgoCanada-deployment-update.csv')
iris = pd.read_csv(fn)

ax.plot(np.nan, np.nan, 'o')
ax.plot(iris.Longitude, iris.Latitude, 'o', label='CTD', markersize=6, transform=transform)

# format map
lon_formatter = LongitudeFormatter(zero_direction_label=True)
lat_formatter = LatitudeFormatter()
gl = ax.gridlines(crs=transform, draw_labels=True)
gl.right_labels = False
gl.xformatter = lon_formatter
gl.yformatter = lat_formatter

fig.savefig(
    Path('../figures/iris_deployments.png'), 
    dpi=350, bbox_inches='tight', facecolor=fig.get_facecolor(),
    edgecolor=None
)
plt.show()