#!/usr/bin/python

from pathlib import Path
import numpy as np
import pandas as pd

import cmocean.cm as cmo

from netCDF4 import Dataset

import matplotlib.pyplot as plt
import cartopy.crs as ccrs
import cartopy.feature as cfeature

canada_east = -35
canada_west = -151
canada_north = 75
canada_south = 35

projection = ccrs.LambertConformal()

bath = Dataset(Path('/Users/gordonc/Documents/data/GEBCO/GEBCO_2020.nc'))

lons = bath['lon'][:]
lats = bath['lat'][:]
elev = bath['elevation'][:]

ix = np.logical_and(lons > canada_west-20, lons < canada_east+20)
iy = np.logical_and(lats > canada_south-20, lats < canada_north+20)

can_lons = lons[ix]
can_lats = lats[iy]
can_elev = elev[iy,:]
can_elev = can_elev[:,ix]

dx = np.arange(0,can_lons.shape[0],40)
dy = np.arange(0,can_lats.shape[0],40)

can_lons = can_lons[dx]
can_lats = can_lats[dy]
can_elev = can_elev[dy,:]
can_elev = can_elev[:,dx]
can_elev = -np.ma.masked_array(can_elev.data, can_elev > 0)

fig = plt.figure()
ax = fig.add_subplot(1, 1, 1, projection=projection)

df = pd.read_csv(Path('/Users/gordonc/Documents/argo/meds/2021-deployment-plan-ocean-ops.csv'))

ax.plot(df.Longitude, df.Latitude, 'o', markerfacecolor='yellow', markersize=4, markeredgecolor='black', transform=ccrs.Geodetic())
ax.set_extent([canada_west, canada_east, canada_south, canada_north])
ax.coastlines(resolution='50m')
ax.gridlines(draw_labels=True)
im = ax.contourf(can_lons, can_lats, can_elev,
                transform=ccrs.PlateCarree(),
                cmap=cmo.deep,
                vmin=0, extend='max')
plt.colorbar(im, ax=ax, orientation='horizontal', label='Depth (m)')
ax.add_feature(cfeature.LAND.with_scale('50m'))

fig.savefig(Path('../figures/deployment_plan_canada.png'), bbox_inches='tight', dpi=350)

africa_east = 35
africa_west = -20
africa_north = 20
africa_south = -30

ix = np.logical_and(lons > africa_west-5, lons < africa_east+5)
iy = np.logical_and(lats > africa_south-5, lats < africa_north+5)

afr_lons = lons[ix]
afr_lats = lats[iy]
afr_elev = elev[iy,:]
afr_elev = afr_elev[:,ix]

dx = np.arange(0,afr_lons.shape[0],40)
dy = np.arange(0,afr_lats.shape[0],40)

afr_lons = afr_lons[dx]
afr_lats = afr_lats[dy]
afr_elev = afr_elev[dy,:]
afr_elev = afr_elev[:,dx]
afr_elev = -np.ma.masked_array(afr_elev.data, afr_elev > 0)

fig = plt.figure()
ax = fig.add_subplot(1, 1, 1, projection=ccrs.PlateCarree())

df = pd.read_csv(Path('/Users/gordonc/Documents/argo/meds/2021-deployment-plan-ocean-ops.csv'))

ax.plot(df.Longitude, df.Latitude, 'o', markerfacecolor='yellow', markersize=6, markeredgecolor='black', transform=ccrs.PlateCarree())
ax.set_extent([africa_west, africa_east, africa_south, africa_north])
ax.coastlines(resolution='50m')
ax.gridlines(draw_labels=True)
im = ax.contourf(afr_lons, afr_lats, afr_elev,
                transform=ccrs.PlateCarree(),
                cmap=cmo.deep,
                vmin=0, extend='max')
plt.colorbar(im, ax=ax, label='Depth (m)')
ax.add_feature(cfeature.LAND.with_scale('50m'))

fig.savefig(Path('../figures/deployment_plan_africa.png'), bbox_inches='tight', dpi=350)
