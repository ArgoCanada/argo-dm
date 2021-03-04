#!/usr/bin/python

from pathlib import Path

import numpy as np
import pandas as pd

import matplotlib.pyplot as plt
import seaborn as sns
from seaborn.palettes import color_palette
sns.set(style='ticks', palette='colorblind')

import bgcArgoDMQC as bgc
import argopy
argopy.set_options(mode='expert')
argo_loader = argopy.DataFetcher()

# some indexing to choose floats
# get core and bgc profiles for meds dac
gx = bgc.get_index(index='global')
bx = bgc.get_index()

# get core files only
gx = gx[~gx.wmo.isin(bx.wmo)]
# only profiles from the last 5 years
gx = gx[gx.date > 2.020e13]
gx = gx[gx.dac == 'meds']

dac_list = []
res_list = []
wmo_list = []
cyc_list = []

i = 0
N = gx.wmo.unique().shape[0]

hdf_file = Path('../data/pts-flt-meds.h5')

if not hdf_file.exists():
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

        res = ds.dims['N_POINTS']

        dac_list.append(dac)
        res_list.append(res)
        wmo_list.append(wmo)
        cyc_list.append(cyc)

        i += 1
        pct = 100*i/N

        print(wmo, cyc, dac, res, '{:.2f}%'.format(pct))


    cf = pd.DataFrame(dict(wmo=wmo_list, cycle=cyc_list, dac=dac_list, pts=res_list))
    cf.to_hdf(hdf_file, key='cf', mode='w')
else:
    cf = pd.read_hdf(hdf_file, 'cf')

# cf = cf[cf.dac != 'kordi']

# fig, ax = plt.subplots()
# g = sns.barplot(x='dac', y='pts', data=cf, ax=ax, palette=sns.color_palette('gist_gray'))
# ax.grid()
# ax.set_ylabel('Vertical Resolution')
# ax.set_xlabel('DAC')
# fig.savefig(Path('../figures/dac_res.png'), bbox_inches='tight', dpi=350)

# fig, axes = plt.subplots(3, 3, sharex=True)
# axes = axes.flatten()
# for dac, ax in zip(cf.dac.unique(), axes):
#     sns.histplot(cf[cf.dac == dac].pts, ax=ax, binwidth=50, color='grey')
#     ax2 = ax.twinx()
#     sns.kdeplot(cf[cf.dac == dac].pts, ax=ax2, color='grey')
#     ax2.set_yticks([])
#     ax2.set_ylabel('')
#     ax.set_title(dac)
#     ax.set_xlabel('')
#     ax.set_ylabel('')

# for ax in axes[-3:]:
#     ax.set_xlabel('$N_{points}$')
# axes[0].set_xlim((0,1500))

# fig.tight_layout()
# fig.savefig(Path('../figures/dac_res_dist.png'), bbox_inches='tight', dpi=350)

# plt.close('all')