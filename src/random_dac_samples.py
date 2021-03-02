#!/usr/bin/python

from pathlib import Path

import numpy as np
import pandas as pd

import matplotlib.pyplot as plt
import seaborn as sns
sns.set(style='ticks', palette='colorblind')

import bgcArgoDMQC as bgc
from argopy import DataFetcher as ArgoDataFetcher
argo_loader = ArgoDataFetcher()

# some indexing to choose floats
# get core and bgc profiles for meds dac
gx = bgc.get_index(index='global')
bx = bgc.get_index()
gx = gx[gx.dac != 'meds']
bx = bx[bx.dac != 'meds']

# get core files only
gx = gx[~gx.wmo.isin(bx.wmo)]
# only profiles from the last 5 years
gx = gx[gx.date > 2.020e13]

dac_list = []
res_list = []

for w in gx.wmo.unique():
    # int so that it can be used as index
    sub_gx = gx[gx.wmo == w]
    r = int(sub_gx.shape[0]*np.random.rand())
    # get the profile info
    profile = sub_gx.iloc[r]
    dac = profile.dac
    wmo = profile.wmo
    cyc = profile.cycle

    # load using argo data fetcher
    try:
        ds = argo_loader.profile([int(wmo)], [cyc]).to_xarray()
    except:
        print('e')
        continue

    gx = gx[gx.wmo != wmo]
    res = ds.dims['N_POINTS']

    dac_list.append(dac)
    res_list.append(res)

    print(wmo, cyc, dac, res)


cf = pd.DataFrame(dict(dac=dac_list, pts=res_list))
fig, ax = plt.subplots()
g = sns.barplot(x='dac', y='pts', data=cf, ax=ax)
ax.grid()
fig.savefig(Path('../figures/other_dac_res.png'), bbox_inches='tight', dpi=350)