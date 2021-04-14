#!/usr/bin/python

from pathlib import Path

import numpy as np
import pandas as pd

import matplotlib.pyplot as plt
import seaborn as sns

sns.set(style='ticks')
pal = sns.color_palette('colorblind')

df = pd.read_csv(Path('../data/nke-npts-npacket.csv'))
df['nsbd'] = np.ceil(df.npacket/3)
df['nsbd_bgc'] = np.ceil(df.npacket_bgc/3)
df['data_kb'] = df.nsbd*300/1000
df['data_bgc_kb'] = df.nsbd_bgc*300/1000

meds_core_pts  = np.array([129, 105, 104, 105, 104])
meds_core_data = np.array([6400, 1800, 1757, 1743, 1785])/1000

coriolis_core_pts  = np.array([994])
coriolis_core_data = np.array([10800])/1000

meds_bgc_pts  = np.array([105,128,100,85,34])
meds_bgc_data = np.array([3090,5200,3221,4967,5167])/1000

fig, ax = plt.subplots()
ax.plot(df.npts, df.data_kb, 'ko', label='NKE Core')
ax.plot(df.npts, df.data_bgc_kb, '^', color='grey', label='NKE BGC')
ax.plot(meds_core_pts, meds_core_data, 'o', color=pal[0], label='MEDS Core')
ax.plot(coriolis_core_pts, coriolis_core_data, 'o', color=pal[1], label='Coriolis Core')
ax.plot(meds_bgc_pts, meds_bgc_data, '^', color=pal[0], label='MEDS BGC')


cf = np.poly1d(np.polyfit(df.data_kb, df.npts, 1))
bf = np.poly1d(np.polyfit(df.data_bgc_kb, df.npts, 1))

dplans = [12, 17, 30]
pnames = ['2', '3', '4']
for i,d in enumerate(dplans):
    ax.axhline(d/3, color=pal[2+i], label=None)
    ax.axvline(cf(d/3), color=pal[2+i], linestyle='--', label=None)
    ax.axvline(bf(d/3), color=pal[2+i], linestyle='-.', label=None)
    print(cf(d/3), bf(d/3))
    ax.text(800, d/3+0.1, 'Plan {}/3'.format(pnames[i]), color=pal[2+i])

ax.plot([448], [3.9], '*', color='k', markersize=10, label='New High-res MEDS Float')

ax.set_xlabel('Average Number of Points per Profile')
ax.set_ylabel('SBD File Size per Profile (kB)')
ax.legend(loc=2)
ax.set_xlim((-5, 1050))
ax.set_ylim((0,20))
ax.minorticks_on()
ax.grid()
fig.savefig(Path('../figures/approximate_data_usage_20210325.png'), bbox_inches='tight', dpi=350)
plt.close(fig)