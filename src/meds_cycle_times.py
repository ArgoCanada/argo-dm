#!/usr/bin/python

from pathlib import Path

import numpy as np
import pandas as pd
import datetime

import matplotlib.pyplot as plt
import seaborn as sns
sns.set(style='ticks', palette='colorblind')

import bgcArgoDMQC as bgc

cix = bgc.get_index(index='global')
bix = bgc.get_index()

# cix = cix[cix.dac == 'meds']
# bix = bix[bix.dac == 'meds']

cix = cix[cix.date.notna()]
bix = bix[bix.date.notna()]

cix = cix[cix.date > 2.02e13]
bix = bix[bix.date > 2.02e13]

datestr = [str(int(d)) for d in cix.date]
cix['time'] = np.array([datetime.datetime(int(d[:4]), int(d[4:6]), int(d[6:8]), int(d[8:10]), int(d[10:12]), int(d[12:])) for d in datestr])
datestr = [str(int(d)) for d in bix.date]
bix['time'] = np.array([datetime.datetime(int(d[:4]), int(d[4:6]), int(d[6:8]), int(d[8:10]), int(d[10:12]), int(d[12:])) for d in datestr])

cdiffs = np.array([])
ndiffs = np.array([])
for w in cix.wmo.unique():
    xd = np.diff(cix[cix.wmo == w].time)
    frac_day = np.array([pd.Timedelta(x).days + pd.Timedelta(x).seconds/60/60/24 for x in xd])
    cdiffs = np.append(cdiffs, frac_day)
    ndiffs = np.append(ndiffs, np.diff(cix[cix.wmo == w].cycle))

cdiffs = cdiffs[ndiffs == 1]

bdiffs = np.array([])
ndiffs = np.array([])
for w in bix.wmo.unique():
    xd = np.diff(bix[bix.wmo == w].time)
    frac_day = np.array([pd.Timedelta(x).days + pd.Timedelta(x).seconds/60/60/24 for x in xd])
    bdiffs = np.append(bdiffs, frac_day)
    ndiffs = np.append(ndiffs, np.diff(bix[bix.wmo == w].cycle))

bdiffs = bdiffs[ndiffs == 1]

fig, axes = plt.subplots(1, 2)

sns.histplot(cdiffs, bins=np.arange(-0.5, 20.5, 1), ax=axes[0])
sns.histplot(bdiffs, bins=np.arange(-0.5, 20.5, 1), ax=axes[1])
axes[0].set_title('Argo Core Floats')
axes[1].set_title('Argo BGC Floats')
fig.suptitle('Time Difference Between Adjacent Profiles (days), 2020-present')

fig.tight_layout()
fig.savefig(Path('../figures/cycle_periods_2020-present.png'), bbox_inches='tight', dpi=250)