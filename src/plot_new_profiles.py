
# system
import sys

# data modules
import pandas as pd
import argopandas as argo

# plotting modules
import matplotlib.pyplot as plt
import seaborn as sns
sns.set(style='ticks', palette='colorblind')

# set up time stuff, look back one day every day
# look back to Friday if its a Monday
today = pd.Timestamp.today(tz='UTC')
time = today.time()
day = today.day_name()
if day == 'Monday':
    day_delta = 3
else:
    day_delta = 1

# can manually set number of days from command line
if len(sys.argv) > 1:
    day_delta = int(sys.argv[1])

start_date = today - pd.Timedelta(days=day_delta) - pd.Timedelta(hours=time.hour, minutes=time.minute, seconds=time.second)

# grab core and bgc index
ix = argo.prof.subset_date(start_date)
ix = ix[ix.file.str.contains('meds')]
bx = argo.bio_prof.subset_date(start_date)
bx = bx[bx.file.str.contains('meds')]

# get data, note bgc data will have to be updated/not
# hard coded once the PROVOR floats are deployed
core = ix.levels[['PRES', 'TEMP', 'TEMP_QC', 'PSAL', 'PSAL_QC']]
bgc  = bx.levels[['PRES', 'DOXY', 'DOXY_QC']]

# plot the core data
for f, pt in zip(ix.file, ix.profiler_type):
    fig, axes = plt.subplots(1, 3)
    sns.scatterplot(x='TEMP', y='PRES', hue='TEMP_QC', style='N_PROF', data=core.loc[f], ax=axes[0], linewidth=0.1)
    sns.scatterplot(x='PSAL', y='PRES', hue='PSAL_QC', style='N_PROF', data=core.loc[f], ax=axes[1], linewidth=0.1)
    sns.scatterplot(x='PSAL', y='TEMP', data=core.loc[f], ax=axes[2], linewidth=0.1)
    axes[0].set_title(f'{f}, Npts = {core.loc[f].loc[core.loc[f].PRES.notna()].shape[0]}, float type: {pt}', loc='left')
    [ax.set_ylim((2050, -50)) for ax in axes[:2]]
    fig.set_size_inches(2*fig.get_figwidth(), fig.get_figheight())
    fig.tight_layout()
    plt.show()

# plot the bgc data
for f, pt in zip(bx.file, bx.profiler_type):
    fig, ax = plt.subplots()
    sns.scatterplot(x='DOXY', y='PRES', hue='DOXY_QC', style='N_PROF', data=bgc.loc[f], ax=ax, linewidth=0.1)
    ax.set_ylim((2050, -50))
    ax.set_title(f'{f}, Npts = {bgc.loc[f].loc[bgc.loc[f].DOXY.notna()].shape[0]}, float type: {pt}', loc='left')
    plt.show()

plt.close('all')