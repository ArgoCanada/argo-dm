
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
sns.set(style='ticks', palette='colorblind')

import timezonefinder
tf = timezonefinder.TimezoneFinder()
import pytz

import argopandas as argo

profiler_type = {
    '836':'PROVOR   ',
    '844':'ARVOR_SBE',
    '878':'ARVOR_RBR',
}

ix = argo.prof.subset_date('2022-01')
ix = ix.loc[ix.institution == 'ME']
prof = ix.prof
ix['wmo'] = [prof.PLATFORM_NUMBER.loc[f,0] for f in prof.index.unique('file')]
ix['cycle'] = [prof.CYCLE_NUMBER.loc[f,0] for f in prof.index.unique('file')]

for wmo in ix['wmo'].unique():
    if not ix.cycle.loc[ix.wmo == wmo].isin([1]).any():
        ix = ix.loc[~(ix.wmo == wmo)]

ix = ix.loc[(ix.latitude.notna()) & (ix.longitude.notna())]
ix['timezone'] = [pytz.timezone(tf.certain_timezone_at(lat=lat, lng=lon)) for lat, lon in zip(ix.latitude, ix.longitude)]
ix['local_time'] = [utc_time.tz_convert(tz) for utc_time, tz in zip(ix.date, ix.timezone)]
ix['surface_hour'] = [local_time.hour + 0.5 for local_time in ix.local_time]
ix['platform'] = [profiler_type[f'{p}'] for p in ix.profiler_type]

fig, ax = plt.subplots()
sns.histplot(data=ix, x='surface_hour', hue='platform', bins=np.arange(24), multiple='stack', ax=ax)
ax.set_title('Argo Canada Deployments 2022-present')
ax.set_xlabel('Local Hour at Surface')
ax.set_ylabel('Profiles')
# ax.set_title('Argo Canada All Floats')

for wmo in ix['wmo'].unique():
    if ix.loc[ix.wmo == wmo].surface_hour.std() < 4:
        print(
            ix.loc[ix.wmo == wmo].platform.iloc[0],
            wmo, 
            f'{ix.loc[ix.wmo == wmo].surface_hour.std():.1f}',
            ix.loc[ix.wmo == wmo].date.iloc[-1],
            ix.loc[ix.wmo == wmo].timezone.iloc[0]
        )
fig.savefig('../figures/meds-surfacing-times-2022.png', bbox_inches='tight', dpi=250)
plt.close(fig)