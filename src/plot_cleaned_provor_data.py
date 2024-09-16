
from pathlib import Path
import pandas as pd

import matplotlib.pyplot as plt
import seaborn as sns

facecolor = '#fef7ea'
textcolor = '#4a0404'

custom_style = {
    'axes.edgecolor'  : textcolor,
    'axes.labelcolor' : textcolor,
    'axes.facecolor'  : facecolor,
    'xtick.color'     : textcolor,
    'ytick.color'     : textcolor,
}
sns.set_style('ticks', rc=custom_style)

imei_numbers = [
    '300125061656740',
    '300125061360970',
]

wmo_numbers = [
    '4902598',
    '4902599',
]

for imei, wmo in zip(imei_numbers, wmo_numbers):

    ctd = pd.read_hdf(Path(f'../data/provor/{imei}') / f'{wmo}_ctd_test.h5')
    oxy = pd.read_hdf(Path(f'../data/provor/{imei}') / f'{wmo}_optode_test.h5')
    eco = pd.read_hdf(Path(f'../data/provor/{imei}') / f'{wmo}_ecopuck_test.h5')

    fig, axes = plt.subplots(2, 2, sharey=True, facecolor=facecolor)
    deg = chr(176)
    ctd = ctd.loc[ctd['Phase number'] != 5]
    oxy = oxy.loc[oxy['Phase number'] != 5]
    eco = eco.loc[eco['Phase number'] != 5]
    ctd[f'Temperature ({deg}C)'] = ctd[ctd.columns[5]]
    sns.scatterplot(x=f'Temperature ({deg}C)', y='Pressure (dbar)', hue='Profile number', data=ctd, ax=axes[0,0], palette='colorblind', marker='.', linewidth=0)
    sns.scatterplot(x='Salinity (PSU)', y='Pressure (dbar)', hue='Profile number', data=ctd, ax=axes[0,1], palette='colorblind', legend=False, marker='.', linewidth=0)
    sns.scatterplot(x=f'C1 phase ({deg})', y='Pressure (dbar)', hue='Profile number', data=oxy, ax=axes[1,0], palette='colorblind', legend=False, marker='.', linewidth=0)
    sns.scatterplot(x='Channel 1 a (Count)', y='Pressure (dbar)', hue='Profile number', data=eco, ax=axes[1,1], palette='colorblind', legend=False, marker='.', linewidth=0)
    axc2 = axes[1,1].twiny()
    sns.scatterplot(x='Channel 2 (Count)', y='Pressure (dbar)', hue='Profile number', data=eco, ax=axc2, palette='colorblind', legend=False, marker='.', linewidth=0)

    axes[0,0].legend(fontsize=8, title='Profile #', title_fontsize=10)
    axes[0,0].set_title(wmo, fontweight='bold', loc='left')

    axes[0,0].set_ylim((35.5, -0.5))
    axes[0,1].set_xlim((26, 33))
    axes[1,1].set_xlim((0, 3500))
    axes[1,1].set_xticks([0, 500, 1000, 1500])
    axc2.set_xlim((-2000, 2500))
    axc2.set_xticks([0, 1000, 2000])
    axes[0,0].set_xlabel(f'Temperature ({deg}C)')
    axes[0,1].set_xlabel('Salinity')
    axes[1,0].set_xlabel(f'Optode Phase ({deg})')
    axes[0,0].set_ylabel('Pressure (dbar)')
    axes[1,0].set_ylabel('Pressure (dbar)')
    axes[1,1].set_xlabel('Channel 1 (counts)', loc='left')
    axc2.set_xlabel('Channel 2 (counts)', loc='right')
    fig.set_size_inches(fig.get_figwidth(), 1.5*fig.get_figheight())
    fig.tight_layout()

    fig.savefig(Path(f'../figures/provor/{wmo}_barge_profiles.png'), bbox_inches='tight', dpi=350)
    plt.close(fig)
