
from pathlib import Path

import xarray as xr
import pandas as pd

import matplotlib.pyplot as plt
import seaborn as sns

wmo = 4902688
fn = Path(f'/Users/GordonC/Documents/projects/medsrtqc/data/chla_reprocess/dac/meds/E/{wmo}/profiles/BR{wmo}_002.nc')
ds = xr.open_dataset(fn)

df = pd.DataFrame({
    'PRES':ds['PRES'].data.flatten(),
    'CHLA':ds['CHLA'].data.flatten(),
    'CHLA_ADJUSTED':ds['CHLA_ADJUSTED'].data.flatten(),
})
df = df.loc[df.CHLA.notna()]
df['CHLA / CHLA_ADJUSTED'] = df['CHLA'] / df['CHLA_ADJUSTED']
df = df.melt(id_vars=('PRES', 'CHLA / CHLA_ADJUSTED'), value_name='CHLA_VAL', var_name='STATUS')

fig, axes = plt.subplots(1, 2, sharey=True)
sns.scatterplot(data=df, x='CHLA_VAL', y='PRES', hue='STATUS', ax=axes[0])
sns.scatterplot(data=df.loc[df.STATUS == 'CHLA'], x='CHLA / CHLA_ADJUSTED', y='PRES', ax=axes[1])

fig.suptitle(ds['SCIENTIFIC_CALIB_COEFFICIENT'][3, 0, 2].data.item().decode().strip().replace('],', '],\n'))

axes[0].set_ylim((1020, -20))

fig.savefig('../figures/chla_physio_ratio_example.png', dpi=350, bbox_inches='tight')

axes[0].set_ylim((33, -3))

fig.savefig('../figures/chla_physio_ratio_example_shallow.png', dpi=350, bbox_inches='tight')

plt.close(fig)