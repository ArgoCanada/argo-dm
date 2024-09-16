import cartopy.crs as ccrs
import seaborn as sns

facecolor = '#fef7ea'
textcolor = '#4a0404'

custom_style = {
    'axes.edgecolor'  : textcolor,
    'axes.labelcolor' : textcolor,
    'axes.facecolor'  : facecolor,
    'xtick.color'     : textcolor,
    'ytick.color'     : textcolor,
}
sns.set_style('ticks', rc=custom_style)

import argopy

ix = argopy.ArgoIndex().load().to_dataframe()

ix['year'] = [d.year for d in ix.date]
ix = ix.loc[(ix.year >= 2024) | (ix.wmo.isin([4902610, 4902611]))]

last_prof = [ix.loc[ix.wmo == wmo].index[-1] for wmo in ix.wmo.unique()]
ix = ix.loc[last_prof]
ix['Active Floats'] = ['Canadian Floats' if inst == 'MEDS, Canada' else 'Global Array' for inst in ix.institution]

fig, ax = argopy.plot.scatter_map(ix, hue='Active Floats', cmap='Spectral', set_global=True, markersize=10)
fig.set_facecolor(facecolor)
meds = ix.loc[ix.institution == 'MEDS, Canada']
ax.scatter(meds.longitude, meds.latitude, color=sns.color_palette('Spectral', as_cmap=True)(0.1), transform=ccrs.PlateCarree(), edgecolor='k', zorder=10)

ax.legend(loc=1)
fig.savefig('../figures/latest_profiles_canada.png', dpi=350, bbox_inches='tight')