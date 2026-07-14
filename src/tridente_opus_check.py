
import matplotlib.pyplot as plt
import seaborn as sns
sns.set_theme(style='ticks', context='paper')

import argopy

tridente_opus_floats = [
    4902726,
    4902731,
    4902734,
    4902729,
    4902722,
    4902736,
    4902727,
    4902719,
    4902732,
    4902733,
    4902725,
    4902735,
    4902730,
]

idx = argopy.ArgoIndex(index_file='bgc-b')
idx = idx.query.wmo(tridente_opus_floats)

ix = idx.load().to_dataframe()

fs = argopy.gdacfs()
ds = fs.open_dataset('aux/meds/4902736/profiles/R4902736_003_aux.nc')

fig, axes = plt.subplots(2, 4, sharey=True)
varnames = ['TEMP', 'PSAL', 'DOXY', 'PH_IN_SITU_TOTAL', 'CHLA', 'BBP700', 'CDOM', 'NITRATE']

for v, ax in zip(varnames, axes.flatten()):
    sns.scatterplot(y=ds['PRES'].values.flatten(), x=ds[v].values.flatten(), ax=ax)
ax.set_ylim((2050, -50))

plt.show()