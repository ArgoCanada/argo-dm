#!/usr/bin/python

from pathlib import Path

import numpy as np

import matplotlib.pyplot as plt
from matplotlib.ticker import FormatStrFormatter
import matplotlib.dates as mdates
from matplotlib.gridspec import GridSpec
import datetime
import seaborn as sns
sns.set(style='ticks', palette='colorblind')

time0 = mdates.date2num(datetime.datetime(2021, 4, 1, 6, 0, 0))
times_5hr = time0 + np.arange(0, 365*24*5, 245)/24
times_6hr = time0 + np.arange(0, 365*24*5, 246)/24
times_13hr = time0 + np.arange(0, 365*24*5, 251)/24

daytime_5hr = np.array([mdates.num2date(d).hour for d in times_5hr])
daytime_6hr = np.array([mdates.num2date(d).hour for d in times_6hr])
daytime_13hr = np.array([mdates.num2date(d).hour for d in times_13hr])

gs = GridSpec(3, 3)
fig = plt.figure()
axes = [
    fig.add_subplot(gs[0,:2]),
    fig.add_subplot(gs[1,:2]),
    fig.add_subplot(gs[2,:2]),
    fig.add_subplot(gs[0,2]),
    fig.add_subplot(gs[1,2]),
    fig.add_subplot(gs[2,2]),
]

for ax, data, diffval in zip(axes[:3], [daytime_5hr, daytime_6hr, daytime_13hr], [5, 6, 13]):
    ax.plot(data[:36], 'k-s')
    ax.set_ylabel('Surfacing Time')
    ax.yaxis.set_major_formatter(FormatStrFormatter('%02d'))
    ax.set_title('Cycle Period = 10 days + {} hours'.format(diffval), fontsize=10, fontweight='bold', loc='left')

    # for v in np.arange(0, 1790, 365):
        # ax.axvline(v/10, linewidth=3, color=sns.color_palette('colorblind')[2])


axes[2].set_xlabel('Cycle Number')

bins = 0.5 + np.arange(-1, 24)
for ax, data in zip(axes[3:], [daytime_5hr, daytime_6hr, daytime_13hr]):
    sns.histplot(data, bins=bins, ax=ax, color='k')
    ax.xaxis.set_major_formatter(FormatStrFormatter('%02d'))

axes[-1].set_xlabel('Lifetime (5yr) Distribution')

fig.set_size_inches(1.75*fig.get_figwidth(), 1.75*fig.get_figheight())
fig.tight_layout()
fig.savefig(Path('../figures/profile_time_of_day_1yr.png'), bbox_inches='tight', dpi=350)

plt.close(fig)