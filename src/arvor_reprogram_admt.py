#!/usr/bin/python

from pathlib import Path

import pandas as pd

import matplotlib.pyplot as plt
import cmocean.cm as cmo
import seaborn as sns
sns.set(style='ticks', palette='colorblind', context='talk')

import argopandas as argo

# get meds floats for core and bgc profiles, populate wmo column
core = argo.prof[:]
bgc  = argo.bio_prof[:]
core = core[core.file.str.contains('meds')]
bgc  = bgc[bgc.file.str.contains('meds')]
core['wmo'] = [f.split('/')[1] for f in core.file]
bgc['wmo']  = [f.split('/')[1] for f in bgc.file]
# get just arvor floats
core = core[core.profiler_type == 844]
bgc  = bgc[bgc.wmo.isin(core.wmo)]

# daily time of each cycle
core['time_of_day'] = [d.hour + d.minute/60 for d in core.date]

fig, ax = plt.subplots()
ms = 4
sns.lineplot(x='date', y='time_of_day', hue='wmo', data=core, legend=False, marker='o', markersize=ms, linestyle='', ax=ax)
ax.set_ylim((0,24))
ax.set_xlim(left=pd.Timestamp('2020-10'))
ax.set_xticks(ax.get_xticks()[::2])
ax.set_yticks(list(range(0,28,6)))
ax.set_yticklabels([f'{h:02d}:00' for h in ax.get_yticks()])
ax.set_xlabel('')
ax.set_ylabel('')

fig.savefig(Path('../figures/arvor_profile_times.png'), dpi=350, bbox_inches='tight')
plt.close(fig)

# remove bgc floats from core, or will double count/plot
core = core[~core.wmo.isin(bgc.wmo)]

# number of levels at each cycle
cf = core.levels[['PRES', 'TEMP', 'PSAL']].reset_index()
bf = bgc.levels[['PRES', 'DOXY']].reset_index()

core['n_levels'] = [cf[cf.file == f].N_LEVELS.max() for f in core.file]
bgc['n_levels']  = [bf[bf.file == f].N_LEVELS.max() for f in bgc.file]

fig, ax = plt.subplots()
sns.lineplot(x='date', y='n_levels', hue='wmo', data=core, legend=False, marker='o', markersize=ms, linestyle='', ax=ax)
sns.lineplot(x='date', y='n_levels', hue='wmo', data=bgc, legend=False, marker='s', markersize=ms, linestyle='', ax=ax)
ax.set_xlim(left=pd.Timestamp('2020-10'))
ax.set_xticks(ax.get_xticks()[::2])
ax.set_xlabel('')
ax.set_ylabel('Vertical Levels')

fig.savefig(Path('../figures/arvor_vertical_levels.png'), dpi=350, bbox_inches='tight')
plt.show()

print('done')