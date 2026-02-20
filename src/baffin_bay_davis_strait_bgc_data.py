
import matplotlib.pyplot as plt
import seaborn as sns

import argopy

# box defining Baffin Bay and Davis Strait
box = [-80, -50, 66, 77]
# dates, entire argo era
dates = ['2025-01-01', '2026-01-01']
# data selections requires depths, select entire water column
depth = [0, 9999]

# select data, depth limits to select all data
data = argopy.DataFetcher(ds='bgc-s', parallel=True).region(box + depth + dates)
ds = data.to_xarray()
ix = data.index
ix['year'] = [d.year for d in ix['date']]

# map profiles, show year
argopy.plot.scatter_map(
    ix,
    hue='year',
    cmap='Spectral_r',
    legend_title='Year of sampling'
)

