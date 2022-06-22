
# system
import sys

# data modules
import numpy as np
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
ix = ix[ix.institution == 'ME']
bx = argo.bio_prof.subset_date(start_date)
bx = bx[bx.institution == 'ME']

# get data, note bgc data will have to be updated/not
# hard coded once the PROVOR floats are deployed
core_vars = ['PRES', 'TEMP', 'TEMP_QC', 'PSAL', 'PSAL_QC']
bgc_vars  = ['PRES', 'DOXY', 'DOXY_QC']
if not ix.empty:
    core = ix.levels[core_vars]
if not bx.empty:
    bgc  = bx.levels[bgc_vars]

flags = [b'1', b'2', b'3', b'4', b'5', b'8']
qc_dict = {v:6*[np.nan] for v in core_vars}
qc_dict['TEMP_QC'] = flags
qc_dict['PSAL_QC'] = flags
qc = pd.DataFrame(qc_dict)
palette = ['#229954', '#2874A6', '#E67E22', '#E74C3C', '#6C3483', '#2E4053']
# plot the core data
for f, pt in zip(ix.file, ix.profiler_type):
    fig, axes = plt.subplots(1, 3)
    d = core.loc[f]
    d = pd.concat([qc, d])
    sns.scatterplot(x='TEMP', y='PRES', hue='TEMP_QC', data=d, ax=axes[0], linewidth=0.1, palette=palette)
    sns.scatterplot(x='PSAL', y='PRES', hue='PSAL_QC', data=d, ax=axes[1], linewidth=0.1, palette=palette, legend=False)
    sns.scatterplot(x='PSAL', y='TEMP', data=d, ax=axes[2], linewidth=0.1)
    axes[0].set_title(f'{f}, Npts = {d.loc[d.PRES.notna()].shape[0]}, float type: {pt}', loc='left')
    [ax.set_ylim((2050, -50)) for ax in axes[:2]]
    mngr = plt.get_current_fig_manager()
    geom = mngr.window.geometry('1500x500+0+100')
    axes[1].set_ylabel('')
    axes[1].set_yticklabels([])
    plt.show()

# plot the bgc data
qc_dict = {v:6*[np.nan] for v in bgc_vars}
qc_dict['DOXY_QC'] = flags
qc = pd.DataFrame(qc_dict)
for f, pt in zip(bx.file, bx.profiler_type):
    fig, ax = plt.subplots()
    sns.scatterplot(x='DOXY', y='PRES', hue='DOXY_QC', data=bgc.loc[f], ax=ax, linewidth=0.1)
    ax.set_ylim((2050, -50))
    ax.set_title(f'{f}, Npts = {bgc.loc[f].loc[bgc.loc[f].DOXY.notna()].shape[0]}, float type: {pt}', loc='left')
    mngr = plt.get_current_fig_manager()
    geom = mngr.window.geometry('600x600+0+100')
    plt.show()

plt.close('all')