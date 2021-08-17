#!/usr/bin/python

from pathlib import Path

import numpy as np

import matplotlib.pyplot as plt
from matplotlib.offsetbox import AnchoredText
import seaborn as sns
sns.set(style='ticks', palette='colorblind')

import bgcArgoDMQC as bgc
import argopy

# bgc.io.update_index()
# bgc.io.get_argo(4902540, local_path=bgc.ARGO_PATH)

fetcher = argopy.DataFetcher()
wmo = 4902540
ds = fetcher.profile([wmo], [18]).to_xarray()
dx = fetcher.profile([wmo], [1]).to_xarray().to_dataframe()

fig, axes = plt.subplots(2, 3)

ms = 2
axes[0,0].plot(dx.TEMP, dx.PRES, 'o', color=sns.color_palette('cmo.thermal')[3], markersize=ms)
axes[0,1].plot(dx.PSAL, dx.PRES, '^', color=sns.color_palette('cmo.haline')[3], markersize=ms)
axes[0,2].plot(np.diff(dx.PRES), dx.PRES[:-1], 's', markersize=ms)

axes[1,0].plot(ds.TEMP, ds.PRES, 'o', color=sns.color_palette('cmo.thermal')[3], markersize=ms)
axes[1,1].plot(ds.PSAL, ds.PRES, '^', color=sns.color_palette('cmo.haline')[3], markersize=ms)
axes[1,2].plot(np.diff(ds.PRES), ds.PRES[:-1], 's', markersize=ms)

for ax, lbl in zip(axes.flatten(), ['A', 'B', 'C', 'D', 'E', 'F']):
    if lbl == 'A' or lbl == 'D':
        lb = AnchoredText(lbl, loc=2, prop=dict(fontsize=14, fontweight='bold'), frameon=False)
    else:
        lb = AnchoredText(lbl, loc=1, prop=dict(fontsize=14, fontweight='bold'), frameon=False)
    ax.add_artist(lb)

for ax in axes[:,0]:
    ax.set_xlabel('Temperature ({}C)'.format(chr(176)))
    ax.set_ylabel('Pressure (dbar)')

for ax in axes[:,1]:
    ax.set_xlabel('Practical Salinity')
    ax.set_yticklabels([])

for ax in axes[:,2]:
    ax.set_xlabel('Resolution [$\Delta P$] (dbar)')
    ax.set_xlim(left=0, right=30)
    ax.set_yticklabels([])

for ax in axes.flatten():
    ax.set_ylim((1200,0))

for ax in axes[0,:]:
    ax.set_xlabel('')

axes[0,0].set_title('Before Param. Change', loc='left', fontweight='bold')
axes[1,0].set_title('After Param. Change', loc='left', fontweight='bold')
axes[0,2].set_title('Float {}, Cycle 1'.format(wmo), loc='right', fontweight='bold')
axes[1,2].set_title('Cycle 18'.format(wmo), loc='right', fontweight='bold')

fig.tight_layout()
fig.savefig(Path('../figures/meds_before_after_res_results.png'), bbox_inches='tight', dpi=350)
plt.close(fig)

dx = dx[dx.PRES < 300]
fig, axes = plt.subplots(2, 1, sharex=True, sharey=True)
sc1 = axes[0].scatter(dx.TIME, dx.PRES, c=dx.TEMP, cmap=sns.color_palette('cmo.thermal', as_cmap=True))
sc2 = axes[1].scatter(dx.TIME, dx.PRES, c=dx.PSAL, cmap=sns.color_palette('cmo.haline', as_cmap=True))
axes[0].set_ylim((300,0))

axes[0].set_ylabel('Pressure (dbar)')
axes[1].set_ylabel('Pressure (dbar)')

cb1 = plt.colorbar(sc1, ax=axes[0], label='Temperature ({}C)'.format(chr(176)))
cb2 = plt.colorbar(sc2, ax=axes[1], label='Salinity')

for tick in axes[1].get_xticklabels():
    tick.set_rotation(45)

fig.savefig(Path('../figures/high_res_scatter_col.png'), bbox_inches='tight', dpi=350)
plt.close(fig)
