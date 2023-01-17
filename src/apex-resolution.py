
import numpy as np

import matplotlib.pyplot as plt
import seaborn as sns
sns.set(style='ticks', palette='colorblind')

import argopandas as argo

ix = argo.prof.subset_date('2021-01')
ix = ix.loc[ix.profiler_type == 846]

# ix = ix.iloc[np.random.randint(0, ix.shape[0], 500)]

data = ix.levels[['PRES', 'PSAL', 'TEMP']]

n_levels = np.nan*np.ones((ix.shape[0],))
for i,f in enumerate(ix.file):
    if f in data.index.unique('file'):
        n_levels[i] = data.loc[f].index.max()[1]


ix['dac'] = [f.split('/')[0] for f in ix.file]
ix['model'] = ix.shape[0]*['APEX']
ix['n_levels'] = n_levels

fig, ax = plt.subplots()
sns.swarmplot(data=ix, x='model', y='n_levels', hue='dac')
ax.legend(loc=4, bbox_to_anchor=(1.3, 0.0))
fig.savefig('../figures/apex-res.png', bbox_inches='tight', dpi=300)