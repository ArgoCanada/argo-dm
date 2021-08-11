#!/usr/bin/python

from pathlib import Path
import numpy as np
import pandas as pd

import cmocean.cm as cmo

from netCDF4 import Dataset

import matplotlib.pyplot as plt
import matplotlib.dates as mdates
import cartopy.crs as ccrs
import cartopy.feature as cfeature

pr_east = -68
pr_west = -73
pr_north = 23
pr_south = 20

df = pd.read_csv(Path('../data/rbr/4902533_failed_locations.csv'), index_col=0, sep=';').T

projection = ccrs.PlateCarree()

# bath = Dataset(Path('/Users/gordonc/Documents/data/GEBCO/GEBCO_2020.nc'))

# lons = bath['lon'][:]
# lats = bath['lat'][:]
# elev = bath['elevation'][:]

# delta = 10
# ix = np.logical_and(lons > pr_west-delta, lons < pr_east+delta)
# iy = np.logical_and(lats > pr_south-delta, lats < pr_north+delta)

# lons = lons[ix]
# lats = lats[iy]
# elev = elev[iy,:]
# elev = elev[:,ix]

# dx = np.arange(0,lons.shape[0],40)
# dy = np.arange(0,lats.shape[0],40)

# lons = lons[dx]
# lats = lats[dy]
# elev = elev[dy,:]
# elev = elev[:,dx]
# elev = -np.ma.masked_array(elev.data, elev > 0)

fig = plt.figure()
ax = fig.add_subplot(1, 1, 1, projection=projection)

lat = df['GPS latitude'].values + (df['GPS latitude (minutes)'].values + df['GPS latitude (minutes fractions (4th))'].values/10000)/60
lon = -df['GPS longitude'].values - (df['GPS longitude (minutes)'].values + df['GPS longitude (minutes fractions (4th))'].values/10000)/60

dates = np.array([mdates.datetime.datetime(y+2000, m, d, h, mn, s) for y,m,d,h,mn,s in zip(df.Year, df.Month, df.Day, df.Hour, df.Minute, df.Second)])
ix = dates > mdates.datetime.datetime.today() - mdates.datetime.timedelta(days=8)

last_week = dates[ix]
last_lats = lat[ix]
last_lons = lon[ix]

delta_t = last_week[-1] - last_week[0]
delta_t = delta_t.total_seconds()/60/60/24
delta_lat = last_lats[-1] - last_lats[0]
delta_lon = last_lons[-1] - last_lons[0]

lat_per_day = delta_lat/delta_t
lon_per_day = delta_lon/delta_t

two_weeks = mdates.datetime.datetime.today() + mdates.datetime.timedelta(days=14)
curr_delta = two_weeks - last_week[-1]
curr_delta = curr_delta.total_seconds()/60/60/24
two_weeks_lat = curr_delta*lat_per_day
two_weeks_lon = curr_delta*lon_per_day

aug_4 = mdates.datetime.datetime(year=2021, month=8, day=4)
curr_delta = aug_4 - last_week[-1]
curr_delta = curr_delta.total_seconds()/60/60/24
aug_4_lat = curr_delta*lat_per_day
aug_4_lon = curr_delta*lon_per_day


ax.plot(lon, lat, 'o', markerfacecolor='yellow', markersize=4, markeredgecolor='black', transform=ccrs.Geodetic())
# ax.plot(lon[-1] + two_weeks_lon, lat[-1] + two_weeks_lat, '*', markerfacecolor='yellow', markersize=8, markeredgecolor='black', transform=ccrs.Geodetic())
# ax.plot(lon[-1] + aug_4_lon, lat[-1] + aug_4_lat, '*', markerfacecolor='yellow', markersize=8, markeredgecolor='black', transform=ccrs.Geodetic())
# ax.text(lon[-1] + two_weeks_lon + 0.75, lat[-1] + two_weeks_lat, '2 weeks', transform=ccrs.Geodetic(), bbox=dict(facecolor='white', edgecolor='black'), fontsize=8)
# ax.text(lon[-1] + aug_4_lon, lat[-1] + aug_4_lat + 0.75, 'Aug 4', transform=ccrs.Geodetic(), bbox=dict(facecolor='white', edgecolor='black'), fontsize=8)

ax.set_extent([pr_west, pr_east, pr_south, pr_north])
ax.coastlines(resolution='10m')
ax.gridlines(draw_labels=True)
# im = ax.contourf(lons, lats, elev,
#                 transform=ccrs.PlateCarree(),
#                 cmap=cmo.deep,
#                 vmin=0, extend='max')
# plt.colorbar(im, ax=ax, orientation='horizontal', label='Depth (m)')
ax.add_feature(cfeature.LAND.with_scale('10m'))

fig.savefig(Path('../figures/rbr_locations.png'), bbox_inches='tight', dpi=350)