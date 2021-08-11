#!/usr/bin/python

from pathlib import Path

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
sns.set(style='ticks', palette='colorblind')

import gsw

wmo = 4902481
flist = list(Path('../sbd/{}'.format(wmo)).glob('Ascent*.csv'))
print(flist)
fn = flist[0]
df = pd.read_csv(fn, sep=';', encoding='unicode-escape')
pres = df['CTD - Pressure (dbar)'].to_numpy()
temp = df['CTD - Temperature (°C)'].to_numpy()
psal = df['CTD - Salinity (PSU)'].to_numpy()
n = 1
while pres[-n] == 1000:
    pres = pres[:-n]
    temp = temp[:-n]
    psal = psal[:-n]
# corr = df['CTD - Salinity correction (°C)'][:-n]
pden = gsw.pot_rho_t_exact(gsw.SA_from_SP(psal, pres, -49, 42), temp, pres, 0) - 1000

print(pden.shape)

fig, axes = plt.subplots(1, 4, sharey=True)

for ax, v, label in zip(axes, [temp, psal, pden], ['Temperature ({}C)'.format(chr(176)), 'Salinity', 'Potential Density (kg m$^{-3}$)']):
    ax.plot(v, pres, '-', markeredgecolor='k', markeredgewidth=0.2, markersize=10)
    ax.set_xlabel(label)
axes[-1].plot(-np.diff(pres), pres[:-1], '-',  markeredgecolor='k', markeredgewidth=0.2, markersize=10)
axes[-1].set_xlabel('$\Delta$P (dbar)')
axes[-1].set_xlim(left=0)
axes[0].set_ylabel('Pressure (dbar)')
axes[0].set_ylim((2000, 0))
axes[0].set_title(wmo)

w, h = fig.get_figwidth(), fig.get_figheight()
fig.set_size_inches(w*4/3, h)

fig.savefig(Path('../figures/{}_parameter_change.png'.format(wmo)), bbox_inches='tight', dpi=250)
plt.close(fig)