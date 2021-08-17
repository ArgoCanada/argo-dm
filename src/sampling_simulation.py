#!/usr/bin/python

from pathlib import Path

import numpy as np

import matplotlib.pyplot as plt
from matplotlib.ticker import FormatStrFormatter
import matplotlib.dates as mdates
from matplotlib.gridspec import GridSpec
from matplotlib.offsetbox import AnchoredText
import datetime
import seaborn as sns
sns.set(style='ticks', palette='colorblind')

time0 = mdates.date2num(datetime.datetime(2021, 4, 1, 6, 0, 0))
times_5hr = time0 + np.arange(0, 365*24*5, 245)/24
times_6hr = time0 + np.arange(0, 365*24*5, 246)/24
times_7hr = time0 + np.arange(0, 365*24*5, 247)/24

daytime_5hr = np.array([mdates.num2date(d).hour for d in times_5hr])
daytime_6hr = np.array([mdates.num2date(d).hour for d in times_6hr])
daytime_7hr = np.array([mdates.num2date(d).hour for d in times_7hr])

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

N = 36
for ax, data, diffval, lbl in zip(axes[:3], [daytime_5hr, daytime_6hr, daytime_7hr], [5, 6, 7], ['A', 'C', 'E']):
    ax.plot(data[:N], 'k-s')
    ax.set_ylabel('Surfacing Time')
    ax.yaxis.set_major_formatter(FormatStrFormatter('%02d'))
    ax.set_title('Cycle Period = 10 days + {} hours'.format(diffval), fontsize=10, fontweight='bold', loc='left')
    ax.fill_between(np.arange(-1, N+1), 0, 3, color='navy', alpha=0.3)
    ax.fill_between(np.arange(-1, N+1), 21, 24, color='navy', alpha=0.3)
    ax.set_ylim(0,24)
    ax.set_xlim((-0.9, N))
    lb = AnchoredText(lbl, prop=dict(fontweight='bold', fontsize=14), frameon=False, loc=2)
    ax.add_artist(lb)
    # for v in np.arange(0, 1790, 365):
        # ax.axvline(v/10, linewidth=3, color=sns.color_palette('colorblind')[2])


axes[2].set_xlabel('Cycle Number')

bins = 0.5 + np.arange(-1, 24)
for ax, data, lbl in zip(axes[3:], [daytime_5hr, daytime_6hr, daytime_7hr], [' B', ' D', ' F']):
    sns.histplot(data, bins=bins, ax=ax, color='k')
    ax.xaxis.set_major_formatter(FormatStrFormatter('%02d'))
    lb = AnchoredText(lbl, prop=dict(fontweight='bold', fontsize=14), frameon=False, loc=2)
    ax.add_artist(lb)

axes[-1].set_xlabel('Lifetime (5yr) Distribution')

fig.set_size_inches(1.75*fig.get_figwidth(), 1.75*fig.get_figheight())
fig.tight_layout()
fig.savefig(Path('../figures/profile_time_of_day_1yr_updated.png'), bbox_inches='tight', dpi=350)

plt.close(fig)

times_11hr = time0 + np.arange(0, 365*24*5, 251)/24
times_13hr = time0 + np.arange(0, 365*24*5, 253)/24

daytime_11hr = np.array([mdates.num2date(d).hour for d in times_11hr])
daytime_13hr = np.array([mdates.num2date(d).hour for d in times_13hr])

gs = GridSpec(2, 3)
fig = plt.figure()
axes = [
    fig.add_subplot(gs[0,:2]),
    fig.add_subplot(gs[1,:2]),
    fig.add_subplot(gs[0,2]),
    fig.add_subplot(gs[1,2]),
]

N = 36
for ax, data, diffval, lbl in zip(axes[:2], [daytime_11hr, daytime_13hr], [11, 13], ['A', 'C']):
    ax.plot(data[:N], 'k-s')
    ax.set_ylabel('Surfacing Time')
    ax.yaxis.set_major_formatter(FormatStrFormatter('%02d'))
    ax.set_title('Cycle Period = 10 days + {} hours'.format(diffval), fontsize=10, fontweight='bold', loc='left')
    ax.fill_between(np.arange(-1, N+1), 0, 3, color='navy', alpha=0.3)
    ax.fill_between(np.arange(-1, N+1), 21, 24, color='navy', alpha=0.3)
    ax.set_ylim(0,24)
    ax.set_xlim((-0.9, N))
    lb = AnchoredText(lbl, prop=dict(fontweight='bold', fontsize=14), frameon=False, loc=2)
    ax.add_artist(lb)
    # for v in np.arange(0, 1790, 365):
        # ax.axvline(v/10, linewidth=3, color=sns.color_palette('colorblind')[2])


axes[1].set_xlabel('Cycle Number')

bins = 0.5 + np.arange(-1, 24)
for ax, data, lbl in zip(axes[2:], [daytime_11hr, daytime_13hr], [' B', ' D']):
    sns.histplot(data, bins=bins, ax=ax, color='k')
    ax.xaxis.set_major_formatter(FormatStrFormatter('%02d'))
    lb = AnchoredText(lbl, prop=dict(fontweight='bold', fontsize=14), frameon=False, loc=2)
    ax.add_artist(lb)

axes[-1].set_xlabel('Lifetime (5yr) Distribution')

fig.set_size_inches(1.75*fig.get_figwidth(), 1.75*fig.get_figheight()*2/3)
fig.tight_layout()
fig.savefig(Path('../figures/profile_time_of_day_near12hr_1yr.png'), bbox_inches='tight', dpi=350)

plt.close(fig)
