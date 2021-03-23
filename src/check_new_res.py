#!/usr/bin/python

from pathlib import Path

import numpy as np

import matplotlib.pyplot as plt
import seaborn as sns
sns.set(style='ticks', palette='colorblind')

import bgcArgoDMQC as bgc
import argopy

# bgc.io.update_index()
# bgc.io.get_argo(4902540)

fetcher = argopy.DataFetcher()
ds = fetcher.profile([4902540], [5]).to_xarray()

fig, axes = plt.subplots(2, 3)

axes[0,0].plot(ds.TEMP, ds.PRES, 'o', color=sns.color_palette('cmo.thermal')[3], markersize=2)
axes[0,1].plot(ds.PSAL, ds.PRES, '^', color=sns.color_palette('cmo.haline')[3], markersize=2)
axes[0,2].plot(np.diff(ds.PRES), ds.PRES[:-1], '.', markersize=2)

ds = ds.where(ds.PRES < 300)

axes[1,0].plot(ds.TEMP, ds.PRES, 'o', color=sns.color_palette('cmo.thermal')[3], markersize=2)
axes[1,1].plot(ds.PSAL, ds.PRES, '^', color=sns.color_palette('cmo.haline')[3], markersize=2)
axes[1,2].plot(np.diff(ds.PRES), ds.PRES[:-1], '.', markersize=2)

for ax in axes[:,0]:
    ax.set_xlabel('Temperature ({}C)'.format(chr(176)))
    ax.set_ylabel('Pressure (dbar)')

for ax in axes[:,1]:
    ax.set_xlabel('Practical Salinity')
    ax.set_yticklabels([])

for ax in axes[:,2]:
    ax.set_xlabel('Resolution [$\Delta P$] (dbar)')
    ax.set_xlim(left=0)
    ax.set_yticklabels([])

for ax in axes[0,:]:
    ax.set_ylim((2000,0))
    ax.set_xlabel('')
for ax in axes[1,:]:
    ax.set_ylim((300,0))

fig.savefig(Path('../figures/meds_high_res_results.png'), bbox_inches='tight', dpi=350)
plt.close(fig)