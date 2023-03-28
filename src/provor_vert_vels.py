
from pathlib import Path
import numpy as np
import pandas as pd

import matplotlib.pyplot as plt
import seaborn as sns
sns.set(style='ticks', palette='colorblind')

imei_numbers = [
    '300125061656740',
    '300125061360970',
]

wmo_numbers = [
    '4902598',
    '4902599',
]

fig, axes = plt.subplots(2, 2, sharex=True, sharey=True)
for imei, wmo, axes_row in zip(imei_numbers, wmo_numbers, axes):

    oxy_test = pd.read_hdf(Path(f'../data/provor/{imei}') / f'{wmo}_optode_test.h5')
    eco_test = pd.read_hdf(Path(f'../data/provor/{imei}') / f'{wmo}_ecopuck_test.h5')

    oxy_full = pd.read_hdf(Path(f'../data/provor/{imei}') / f'{wmo}_optode_full.h5')
    eco_full = pd.read_hdf(Path(f'../data/provor/{imei}') / f'{wmo}_ecopuck_full.h5')
    

    for df, ax, ix in zip([oxy_test, oxy_full], axes_row, ['Profile number', 'Cycle number']):
        tt = df.loc[df['time'].notna()]
        tt = tt.loc[tt['Phase number'] != 5]
        for p in tt[ix].unique():
            sub = tt.loc[tt[ix] == p]
            speed = np.array([z/t.total_seconds() for z, t in zip(sub['Pressure (dbar)'].diff(), sub['1st sample date'].diff())])
            ax.plot(speed*100, sub['Pressure (dbar)'], '.')

            if ix == 'Profile number':
                ifig, iax = plt.subplots()
                iax.plot(speed*100, sub['Pressure (dbar)'], '.')
                iax.set_ylim((36, -1))
                iax.set_xlim((-18, 2))
                iax.set_ylabel('Pressure (dbar)')
                iax.set_xlabel('Vertical Velocity (cm s$^{-1}$)')
                iax.set_title(f'{wmo} profile {p}')
                ifig.set_size_inches(ifig.get_figwidth()/2, ifig.get_figheight())
                ifig.savefig(f'../figures/provor/vel_profiles/oxy_{wmo}_{p:02d}.png', bbox_inches='tight', dpi=300)
                plt.close(ifig)
        ax.set_ylim((36, -1))
        ax.set_xlim((-18, 2))
    axes_row[0].set_ylabel('Pressure (dbar)')
    axes_row[0].set_title(f'{wmo}', loc='left', fontweight='bold')
[ax.set_xlabel('Vertical Velocity (cm s$^{-1}$)') for ax in axes[1,:]]
axes[0,0].set_title('Barge Test', loc='right')
axes[0,1].set_title('Open Ocean Deployment', loc='right')
fig.set_size_inches(fig.get_figwidth(), 1.5*fig.get_figheight())
fig.tight_layout()
fig.savefig('../figures/provor/vert_vel_oxy_final.png', bbox_inches='tight', dpi=300)