import argopy

from pathlib import Path
from netCDF4 import Dataset
import pandas as pd
import numpy as np

import matplotlib.pyplot as plt
import matplotlib.path as mpath
import cmocean.cm as cmo

import seaborn as sns
sns.set(style="ticks", palette="colorblind")

import cartopy.crs as ccrs
import cartopy.feature as cfeature

# define some useful mapping functions
def polarCentral_set_latlim(lat_lims, ax):
  ax.set_extent([-180, 180, lat_lims[0], lat_lims[1]], ccrs.PlateCarree())
  # Compute a circle in axes coordinates, which we can use as a boundary
  # for the map. We can pan/zoom as much as we like - the boundary will be
  # permanently circular.
  theta = np.linspace(0, 2*np.pi, 100)
  center, radius = [0.5, 0.5], 0.5
  verts = np.vstack([np.sin(theta), np.cos(theta)]).T
  circle = mpath.Path(verts * radius + center)
  
  ax.set_boundary(circle, transform=ax.transAxes)

def add_map_features(ax):
  ax.coastlines()
  gl = ax.gridlines()
  ax.add_feature(cfeature.BORDERS)
  ax.add_feature(cfeature.LAND)
  gl = ax.gridlines(draw_labels=True)

# wmo numbers of the floats
north_wmos = [4902558]
south_wmos = [4902638, 4902639, 4902698, 4902704]

north_plan = [4902672, 4902673]
south_plan = [4902711, 4902718]

north_failed = [4902565]
south_failed = []

# grab Argo index for each group
index = argopy.ArgoIndex().load()
north_ix = index.search_wmo(north_wmos).to_dataframe()
north_ix = north_ix.loc[north_ix.cyc == 1]
south_ix = index.search_wmo(south_wmos).to_dataframe()
south_ix = south_ix.loc[south_ix.cyc == 1]

# active floats
south_ix['Status'] = south_ix.shape[0]*['Operational']
north_ix['Status'] = north_ix.shape[0]*['Operational']

# load info on planned, failed floats
df = pd.read_csv('../../blog/deployment/canada_deployments.csv')
dfn = df.loc[df.REF.isin(north_plan)]
north_plans_df = pd.DataFrame({
  'wmo':dfn.REF.astype(int),
  'latitude':dfn['DEPLOYMENT LAT'],
  'longitude':dfn['DEPLOYMENT LON'],
  'Status':dfn.shape[0]*['Planned']
})
dfn = df.loc[df.REF.isin(north_failed)]
north_failed_df = pd.DataFrame({
  'wmo':dfn.REF.astype(int),
  'latitude':dfn['DEPLOYMENT LAT'],
  'longitude':dfn['DEPLOYMENT LON'],
  'Status':dfn.shape[0]*['Failed']
})

dfs = df.loc[df.REF.isin(south_plan)]
south_plans_df = pd.DataFrame({
  'wmo':dfs.REF.astype(int),
  'latitude':dfs['DEPLOYMENT LAT'],
  'longitude':dfs['DEPLOYMENT LON'],
  'Status':dfs.shape[0]*['Planned']
})
dfs = df.loc[df.REF.isin(south_failed)]
south_failed_df = pd.DataFrame({
  'wmo':dfs.REF.astype(int),
  'latitude':dfs['DEPLOYMENT LAT'],
  'longitude':dfs['DEPLOYMENT LON'],
  'Status':dfs.shape[0]*['Failed']
})

north_ix = pd.concat((north_ix, north_plans_df, north_failed_df))
south_ix = pd.concat((south_ix, south_plans_df, south_failed_df))

# geo axis figures
fig = plt.figure(constrained_layout=True)
axes = [
  fig.add_subplot(1, 2, 1, projection=ccrs.NorthPolarStereo()),
  fig.add_subplot(1, 2, 2, projection=ccrs.SouthPolarStereo())
]

# bathymetry for plot
bath_file = Path('/Users/GordonC/Documents/data/GEBCO/GEBCO_2020.nc')
bath = Dataset(bath_file)
blat = bath['lat'][:]
blon = bath['lon'][:]
elev = bath['elevation'][:]

# subset/decimate bathymetry - really big array
iy = np.logical_or(blat > 60, blat < -55)

blat = blat[iy]
elev = elev[iy,:]
elev = -np.ma.masked_array(elev.data, elev > 0)

N = 20
blat = blat[::N]
blon = blon[::N]
elev = elev[::N,:]
elev = elev[:,::N]

for ix, ax in zip([north_ix, south_ix], axes):
  # add bathymetry
  im = ax.contourf(
    blon, blat, elev, list(range(0, 3800, 200)),
    transform=ccrs.PlateCarree(),
    cmap=cmo.deep,
    vmin=0, extend='max'
  )
  
  leg = True if ix.latitude.mean() > 0 else False
  # plot profiles so far
  sns.scatterplot(
    data=ix, x='longitude', y='latitude', 
    hue='Status', hue_order=['Operational', 'Failed', 'Planned'], palette=['blue', 'red', 'orange'],
    ax=ax, transform=ccrs.PlateCarree(), legend=leg
  )
  add_map_features(ax)

# move legend so somewhere more friendly
axes[0].legend(loc=3, bbox_to_anchor=(-0.25, 0.0))

# set limits
polarCentral_set_latlim([60, 90], axes[0])
polarCentral_set_latlim([-60, -90], axes[1])

axes[0].set_title('Arctic Ocean', loc='left', fontweight='bold')
axes[1].set_title('Southern Ocean\n', loc='left', fontweight='bold')

fig.savefig('../figures/ast2025_polar_deployments.png', bbox_inches='tight', dpi=350)
plt.close(fig)