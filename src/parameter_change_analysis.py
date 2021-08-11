#!/usr/bin/python

from pathlib import Path

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
sns.set(style='ticks', palette='colorblind')

fn = Path('../docs/parameter_change_tracking.csv')
df = pd.read_csv(fn)

df = df[df.n_bytes != 0]

few_pts = df[df.n_pts < 500]
bgc_index = ['BioGeoChemical' in s for s in df.program]
doxy = df[bgc_index]
core = df[~np.array(bgc_index)]

fig, ax = plt.subplots()
ax.plot(core.n_pts, core.n_bytes/1000, 'o', label='Core floats')
ax.plot(doxy.n_pts, doxy.n_bytes/1000, 'o', label='DOXY floats')

ax.set_xlabel('$N_{pts}$')
ax.set_ylabel('Data Size (kB)')

ax.legend(loc=4)

fig.savefig(Path('../figures/data_npts_scatter.png'), bbox_inches='tight', dpi=350)