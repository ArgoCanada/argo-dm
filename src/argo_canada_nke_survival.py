
from pathlib import Path

import matplotlib.pyplot as plt

import pandas as pd
import seaborn as sns

facecolor = '#fef7ea'
textcolor = '#4a0404'

custom_style = {
    'axes.edgecolor': textcolor,
    'axes.labelcolor': textcolor,
    'axes.facecolor': facecolor,
    'xtick.color': textcolor,
    'ytick.color': textcolor
}
sns.set_style('ticks', rc=custom_style)

import argopy
argopy.set_options(mode='expert')

ix = argopy.ArgoIndex().load().to_dataframe()
# canadian floats
ix = ix.loc[ix.institution == 'MEDS, Canada']
# recent floats
ix = ix.loc[ix.date > '2015-01']
# NKE floats
ix = ix.loc[ix.profiler_code.isin((841, 844, 878, 834, 836, 838))]

index = []
delta = []

for wmo in ix.wmo.unique():
    sub = ix.loc[ix.wmo == wmo]
    index.append(sub.cyc.idxmin())
    index.append(sub.cyc.idxmax())
    delta.append(pd.Timestamp('now') - sub.date.loc[index[-1]])
    delta.append(pd.Timestamp('now') - sub.date.loc[index[-1]])

ix = ix.loc[index]
ix['delta'] = delta

ix = ix.loc[~ix.index.duplicated()]
ct = [ix.loc[ix.wmo == wmo].shape[0]*[i] for i,wmo in enumerate(ix.wmo.unique())]
ix['count'] = [
    x
    for xs in ct
    for x in xs
]

profiler_type = {
    '865':'NOVA',
    '843':'POPS',
    '844':'ARVOR_SBE',
    '846':'APEX',
    '878':'ARVOR_RBR',
    '838':'ARVOR_DEEP',
    '836':'PROVOR_CTS4',
    '834':'PROVOR_CTS5',
}
ix['platform'] = [profiler_type[f'{p}'] for p in ix.profiler_code]

fig, ax = plt.subplots(facecolor=facecolor)
g = sns.lineplot(
    data=ix, x='date', y='count', 
    hue='platform', units='wmo',
    palette='muted', linewidth=0.5,
    sort=False, estimator=None, ax=ax
)
plt.setp(ax.get_legend().get_texts(), color=textcolor)
plt.setp(ax.get_legend().get_title(), color=textcolor)
ax.set_yticks([])
ax.set_ylabel('')
ax.set_xlim(right=pd.Timestamp('now'))
ax.set_title('Lifetime of Argo Canada NKE Floats with at least 1 Profile', loc='left', color=textcolor, fontweight='bold')
ax.set_xlabel('')
fig.set_size_inches(10,4)
fig.savefig(
    '../figures/argo-tech-workshop/argo_canada_nke_lifetimes.png', 
    dpi=350, bbox_inches='tight'
)
plt.close(fig)

# subset floats that have not reported recently
fail = ix.loc[ix.delta > pd.Timedelta(days=60)]

xlim = ax.get_xlim()
ylim = ax.get_ylim()
fig, ax = plt.subplots(facecolor=facecolor)
g = sns.lineplot(
    data=fail, x='date', y='count', 
    hue='platform', units='wmo',
    palette='muted', linewidth=0.5,
    sort=False, estimator=None, ax=ax
)
plt.setp(ax.get_legend().get_texts(), color=textcolor)
plt.setp(ax.get_legend().get_title(), color=textcolor)
ax.set_yticks([])
ax.set_ylabel('')
ax.set_xlim(right=pd.Timestamp('now'))
ax.set_title('Lifetime of Argo Canada NKE Floats with at least 1 Profile', loc='left', color=textcolor, fontweight='bold')
ax.set_xlabel('')
ax.set_xlim(xlim)
ax.set_ylim(ylim)
fig.set_size_inches(10,4)
fig.savefig(
    '../figures/argo-tech-workshop/argo_canada_nke_lifetimes_failed.png', 
    dpi=350, bbox_inches='tight'
)
plt.close(fig)