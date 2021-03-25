#!/usr/bin/python

from pathlib import Path
import numpy as np
import pandas as pd

import matplotlib.pyplot as plt
import seaborn as sns

import datetime
import timezonefinder
import pytz

#------------------------------------------------------------------------------
# SETUP & DATA CLEANING
#------------------------------------------------------------------------------

# load timezone finder object
tf = timezonefinder.TimezoneFinder()
# point to local index files
local_global_index = Path('/Users/gordonc/Documents/projects/bgcArgoDMQC/bgcArgoDMQC/ref/ar_index_global_prof.txt.gz')
local_bgc_index = Path('/Users/gordonc/Documents/projects/bgcArgoDMQC/bgcArgoDMQC/ref/argo_bio-profile_index.txt.gz')

# load index files into dataframes
cix = pd.read_csv(local_global_index, compression='gzip', header=8)
bix = pd.read_csv(local_bgc_index, compression='gzip', header=8)

# temporary - decimate index to small size to run faster and test
# cix = cix.iloc[np.random.randint(low=0, high=cix.shape[0], size=500)]
# bix = bix.iloc[np.random.randint(low=0, high=bix.shape[0], size=500)]

# drop core floats that are associated with bgc floats (?)
# cix = cix[~cix.wmo.isin(bix.wmo)]

# remove any NaN or invalid valued coordinates or dates
cix = cix[cix.latitude.notna()]
cix = cix[cix.longitude.notna()]
cix = cix[cix.latitude <= 90]
cix = cix[cix.longitude <= 180]
cix = cix[cix.latitude >= -90]
cix = cix[cix.longitude >= -180]
cix = cix[cix.date.notna()]
bix = bix[bix.latitude.notna()]
bix = bix[bix.longitude.notna()]
bix = bix[bix.latitude <= 90]
bix = bix[bix.longitude <= 180]
bix = bix[bix.latitude >= -90]
bix = bix[bix.longitude >= -180]
bix = bix[bix.date.notna()]

#------------------------------------------------------------------------------
# GET LOCAL TIMES
#------------------------------------------------------------------------------

# add timezone names to index dataframes
cix['timezone'] = np.array([tf.timezone_at(lng=lon, lat=lat) for lat, lon in zip(cix.latitude, cix.longitude)])
bix['timezone'] = np.array([tf.timezone_at(lng=lon, lat=lat) for lat, lon in zip(bix.latitude, bix.longitude)])

# make datetime column - clunky but ok
datestr = [str(int(d)) for d in cix.date]
cix['time'] = np.array([datetime.datetime(int(d[:4]), int(d[4:6]), int(d[6:8]), int(d[8:10]), int(d[10:12]), int(d[12:])) for d in datestr])
datestr = [str(int(d)) for d in bix.date]
bix['time'] = np.array([datetime.datetime(int(d[:4]), int(d[4:6]), int(d[6:8]), int(d[8:10]), int(d[10:12]), int(d[12:])) for d in datestr])

# I get a NonExistentTimeError for these dates. I don't know why.
# Something to do with daylight savings based on the traceback? Removing.
cix = cix[
    ~cix.time.isin([
        datetime.datetime(2020,9,6,0,30,18), 
        datetime.datetime(2015,3,29,0,5,0),
    ])
]

# get local time
cix['local_time'] = np.array([dt + pytz.timezone(tz).utcoffset(dt) for dt, tz in zip(cix.time, cix.timezone)])
bix['local_time'] = np.array([dt + pytz.timezone(tz).utcoffset(dt) for dt, tz in zip(bix.time, bix.timezone)])
# year and fractional hour for plotting
cix['local_year'] = np.array([dt.year for dt in cix.local_time])
bix['local_year'] = np.array([dt.year for dt in bix.local_time])
cix['local_hour'] = np.array([dt.hour + dt.minute / 60 for dt in cix.local_time])
bix['local_hour'] = np.array([dt.hour + dt.minute / 60 for dt in bix.local_time])

#------------------------------------------------------------------------------
# PLOTTING
#------------------------------------------------------------------------------

# all core profiles
g = sns.displot(data=cix, x='local_hour', col='local_year', col_wrap=8, bins=np.arange(0, 25))
g.fig.tight_layout()
g.fig.savefig(Path('../figures/core_local_times_by_year.png'), bbox_inches='tight', dpi=250)
plt.close(g.fig)

# all bgc files
g = sns.displot(data=bix, x='local_hour', col='local_year', col_wrap=8, bins=np.arange(0, 25))
g.fig.tight_layout()
g.fig.savefig(Path('../figures/bgc_local_times_by_year.png'), bbox_inches='tight', dpi=250)
plt.close(g.fig)

# drop all except 2020
cix = cix[cix.local_year == 2020]
bix = bix[bix.local_year == 2020]

# 2020 histograms
fig, axes = plt.subplots(1,2)
sns.histplot(data=cix, x='local_hour', bins=np.arange(0, 25), ax=axes[0])
sns.histplot(data=bix, x='local_hour', bins=np.arange(0, 25), ax=axes[1])
axes[0].set_title('Core-Argo')
axes[1].set_title('BGC-Argo')
fig.suptitle('Profiles by Local Hour of Day - 2020')
fig.set_size_inches(fig.get_figwidth()*1.5, fig.get_figheight())
fig.savefig(Path('../figures/core_bgc_2020_local_times.png'), bbox_inches='tight', dpi=350)
plt.close(fig)