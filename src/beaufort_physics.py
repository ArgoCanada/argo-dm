
import argopy
import seaborn as sns

import matplotlib.pyplot as plt

sns.set_theme(palette='colorblind', style='ticks')

data = argopy.DataFetcher().region([-167, -120, 67, 78, 0, 2000])
ds = data.to_xarray().argo.teos10(['SA', 'SIG0'])
df = ds.to_dataframe()

fig, axes = plt.subplots(1, 3, sharey=True)

sns.lineplot(data=df, x='TEMP', y='PRES', hue='PLATFORM_NUMBER', units='CYCLE_NUMBER', sort=False, estimator=None, legend=False, ax=axes[0], palette='colorblind')
sns.lineplot(data=df, x='PSAL', y='PRES', hue='PLATFORM_NUMBER', units='CYCLE_NUMBER', sort=False, estimator=None, legend=False, ax=axes[1], palette='colorblind')
sns.lineplot(data=df, x='SIG0', y='PRES', hue='PLATFORM_NUMBER', units='CYCLE_NUMBER', sort=False, estimator=None, legend=False, ax=axes[2], palette='colorblind')

axes[0].set_ylim((2050, -50))

fig.savefig('../figures/beaufort_profiles.png', dpi=300, bbox_inches='tight')