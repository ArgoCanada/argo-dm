#!/usr/bin/python

from pathlib import Path

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
sns.set(style='ticks', palette='colorblind')

fn1 = list(Path('../sbd/4902533').glob('Ascent*.csv'))
fn2 = list(Path('../sbd/4902534').glob('Ascent*.csv'))

fig, axes = plt.subplots(2, 3, sharey=True)

for f1, f2 in zip(fn1, fn2):
    df1 = pd.read_csv(f1, sep=';', encoding='unicode-escape')
    df2 = pd.read_csv(f2, sep=';', encoding='unicode-escape')
    for df, row, n in zip([df1, df2], axes, [9, 10]):
        pres = df['CTD - Pressure (dbar)'][:-n]
        temp = df['CTD - Temperature (°C)'][:-n]
        psal = df['CTD - Salinity (PSU)'][:-n]
        corr = df['CTD - Salinity correction (°C)'][:-n]
        for ax, v, label in zip(row[:2], [temp, psal], ['Temperature ({}C)'.format(chr(176)), 'Salinity']):
            ax.plot(v, pres, '-', markeredgecolor='k', markeredgewidth=0.2, markersize=10)
            if n == 10:
                ax.set_xlabel(label)

        row[-1].plot(-np.diff(pres), pres[:-1], '-',  markeredgecolor='k', markeredgewidth=0.2, markersize=10)
        if n == 10:
            row[-1].set_xlabel('$\Delta$P (dbar)')
        row[-1].set_xlim(left=0)
        row[0].set_ylabel('Pressure (dbar)')
        row[0].set_ylim((2000, 0))

axes[0,1].set_title('RBR Float 4902533')
axes[1,1].set_title('RBR Float 4902534')

w, h = fig.get_figwidth(), fig.get_figheight()
fig.set_size_inches(w*4/3, h*2)

fig.savefig(Path('../figures/rbr_profiles_first5.png'), bbox_inches='tight', dpi=250)

fig, axes = plt.subplots(1, 2)

for f1, f2 in zip(fn1, fn2):
    df1 = pd.read_csv(f1, sep=';', encoding='unicode-escape')
    df2 = pd.read_csv(f2, sep=';', encoding='unicode-escape')
    for ax, df, n in zip(axes, [df1, df2], [9, 10]):
        temp = df['CTD - Temperature (°C)'][:-n]
        psal = df['CTD - Salinity (PSU)'][:-n]
        ax.plot(psal, temp, '-', markeredgecolor='k', markeredgewidth=0.2, markersize=10)
        ax.set_xlabel('Salinity')
axes[0].set_ylabel('Temperature ({}C)'.format(chr(176)))

w, h = fig.get_figwidth(), fig.get_figheight()
fig.set_size_inches(w*1.5, h)
fig.savefig(Path('../figures/rbr_ts_diagram_first5.png'), bbox_inches='tight', dpi=250)

# df3 = pd.read_csv(Path(fn1.as_posix().replace('Ascent', 'Descent')), sep=';', encoding='unicode-escape')
# df4 = pd.read_csv(Path(fn2.as_posix().replace('Ascent', 'Descent')), sep=';', encoding='unicode-escape')

plt.show()
# plt.close('all')