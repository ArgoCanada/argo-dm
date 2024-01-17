
import matplotlib.pyplot as plt
import seaborn as sns
sns.set(style='ticks', palette='colorblind')

from netCDF4 import Dataset
import argopandas as argo

def plot_profile_flags(df, ax=None, ylim=(2000, 0), xlim="auto"):
    if ax is None:
        fig, ax = plt.subplots()

    df = df.loc[df.BBP700_QC.notna()]
    # plot results
    sns.lineplot(
      data=df, x="BBP700", y="PRES", 
      color="k", ax=ax, sort=False, 
      legend=False, estimator=None, zorder=0
    )
    g = sns.scatterplot(
      data=df, x="BBP700", y="PRES", hue="BBP700_QC", 
      hue_order=(b"0", b"1", b"2", b"3", b"4"), ax=ax, zorder=1
    )
    
    if xlim != "auto":
        ax.set_xlim(xlim)
    ax.set_ylim(ylim)

    return g

wmos = [4902684, 4902685]
fig, axes = plt.subplots(2, 4, sharey=True)
varnames = ['DOXY', 'CHLA', 'BBP700']
radio_vars = ['DOWN_IRRADIANCE380', 'DOWN_IRRADIANCE412', 'DOWN_IRRADIANCE490', 'DOWNWELLING_PAR']

for wmo, axrow in zip(wmos, axes):
    ix = argo.float(wmo).bio_prof
    data = ix.levels
    for ax, v in zip(axrow, varnames):
        sns.lineplot(data=data, x=v, y='PRES', hue='file', sort=False, estimator=None, ax=ax, markers=True, legend=False)
    for v in radio_vars:
        sns.lineplot(data=data, x=v, y='PRES', hue='file', sort=False, estimator=None, ax=axrow[-1], markers=True, legend=False)
    ax.set_ylim((250, 0))
    plt.show()

    plot_profile_flags(data.loc[f'meds/{wmo}/profiles/BR{wmo}_012.nc'])
    plt.show()
    break