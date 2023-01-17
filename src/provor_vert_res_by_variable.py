
import argopandas as argo
import matplotlib.pyplot as plt
import seaborn as sns

wmo = 4902598
ix = argo.float(wmo).synthetic_prof
ix = ix.iloc[-3:-2]
data = ix.levels

fig, axes = plt.subplots(2, 3, sharey=True)
var_names = ['TEMP', 'CHLA', 'DOXY', 'PSAL', 'BBP700']
data['BBP700'] = data['BBP700']*1000
unit = [f' ({chr(176)}C)', ' (mg m$^{-3}$)',' ($\mathregular{\mu}$mol kg$^{-1}$)', '', ' ($x$1000 m$^{-1}$)']
col = ['red', 'green', 'blue', 'green', 'brown']

for i in [0,1]:
    var_axes = list(axes[i,:]) + [axes[i,0].twiny(), axes[i,1].twiny()] if i == 0 else list(axes[i,:])
    for ax, v, u, c in zip(var_axes, var_names, unit, col):
        if i==0:
            ax.plot(data[v].loc[data[v].notna()], data['PRES'].loc[data[v].notna()], color=c)
            ax.set_xlabel(v + u)
        else:
            ax.plot(data['PRES'].loc[data[v].notna()].diff(), data['PRES'].loc[data[v].notna()], '.', color='k')
            ax.set_xlabel('$\Delta$P (dbar)')

axes[0,0].set_ylim((2100,-100))
[axes[i,0].set_ylabel('PRES (dbar)') for i in [0,1]]
axes[0,1].set_xlim(left=-0.1)
fig.set_size_inches(fig.get_figwidth(), 1.25*fig.get_figheight())
fig.tight_layout()
fig.savefig('../figures/provor/vert_res.png', bbox_inches='tight', dpi=300)
