#!/usr/bin/python

from pathlib import Path
from netCDF4 import Dataset

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
sns.set_style('ticks')

import gsw
import bgcArgoDMQC as bgc
# import argopy
# argopy.set_options(mode='expert')
# fetcher = argopy.DataFetcher()

df = pd.read_csv(Path('../docs/parameter_change_tracking.csv'))
ix = bgc.get_index('global', dac='meds')

# for wmo in df.wmo:
    # bgc.io.get_argo(wmo, local_path=bgc.ARGO_PATH)

for i, wmo in zip(df.index, df.wmo):
    cycle = ix.cycle[ix.wmo == wmo].max()
    # data = fetcher.profile([wmo], [cycle]).to_xarray().to_dataframe()
    data = Dataset(Path('/Users/gordonc/Documents/data/argo/meds/{}/profiles/R{}_{:03d}.nc'.format(wmo, wmo, cycle)))
    print(wmo, cycle, data['TEMP'][:].data[0,:].shape[0])

    PDEN = gsw.rho_t_exact(gsw.SA_from_SP(data['PSAL'][:].data[0,:], 
                                        data['PRES'][:].data[0,:], 
                                        data['LATITUDE'][:].data[0], 
                                        data['LONGITUDE'][:].data[0]), 
                                        data['TEMP'][:].data[0,:], 
                                        data['PRES'][:].data[0,:]) - 1000
    vdict = {k:data[k][:].data[0,:] for k in ['TEMP', 'PSAL']}
    vdict['PDEN'] = PDEN
    fig, axes = plt.subplots(1, 4, sharey=True)
    for ax, var in zip(axes, ['TEMP', 'PSAL', 'PDEN']):
        ax.plot(vdict[var], data['PRES'][:].data[0,:])
        ax.set_xlabel(var)
    axes[0].set_ylabel('PRES')
    axes[-1].plot(np.diff(data['PRES'][:].data[0,:]), data['PRES'][:].data[0,:-1] + np.diff(data['PRES'][:].data[0,:])/2)
    axes[-1].set_xlabel('$\Delta$P')
    axes[0].set_ylim((2000,0))
    axes[0].set_title('{}, cycle {}'.format(wmo, cycle))
    axes[1].set_title('Npts: {}'.format(data['PRES'][:].data[0,:].shape[0]))
    fig.savefig(Path('../figures/parameter_change/{:02d}_{}_{}.png'.format(i+1, wmo, cycle)), dpi=350, bbox_inches='tight')
    plt.close(fig)
