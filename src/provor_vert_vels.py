
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

    oxy_test = pd.read_hdf(Path(f'../data/provor/{imei}') / f'{wmo}_optode.h5')
    eco_test = pd.read_hdf(Path(f'../data/provor/{imei}') / f'{wmo}_ecopuck.h5')

    oxy_full = pd.read_hdf(Path(f'../data/provor/{imei}') / f'{wmo}_optode_full.h5')
    eco_full = pd.read_hdf(Path(f'../data/provor/{imei}') / f'{wmo}_ecopuck_full.h5')
    
    for df, ax, ix in zip([eco_test, eco_full], axes_row, ['Profile number', 'Cycle number']):
        td = np.array([t.total_seconds() for t in df['1st sample date'].diff()])
        tt = df.loc[td != 0]
        tt = tt.loc[tt['Pressure (dbar)'] < 50]
        for p in tt[ix].unique():
            sub = tt.loc[tt[ix] == p]
            speed = np.array([z/t.total_seconds() for z, t in zip(sub['Pressure (dbar)'].diff(), sub['1st sample date'].diff())])
            ax.plot(speed*100, sub['Pressure (dbar)'], '.')
        ax.set_ylim((36, -1))
        ax.set_xlim((-46, 2))
    axes_row[0].set_ylabel('Pressure (dbar)')
    axes_row[0].set_title(f'{wmo}', loc='left')
[ax.set_xlabel('Vertical Velocity (cm s$^{-1}$)') for ax in axes[1,:]]
axes[0,0].set_title('Barge Test', loc='right')
axes[0,1].set_title('Open Ocean Deployment', loc='right')
fig.set_size_inches(fig.get_figwidth(), 1.5*fig.get_figheight())
fig.tight_layout()
fig.savefig('../figures/provor/vert_vel_eco_final.png', bbox_inches='tight', dpi=300)