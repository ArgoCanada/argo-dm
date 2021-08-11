#!/usr/bin/python

from pathlib import Path

from netCDF4 import Dataset

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
sns.set(style='ticks', palette='colorblind')

import gsw

wmo = 4902481
sbd_file = list(Path('../sbd/{}/'.format(wmo)).glob('Ascent*'))[0]
nc_file = list(Path('/Users/gordonc/Documents/data/Argo/meds/{}/profiles/'.format(wmo)).glob('R*.nc'))[-1]

df = pd.read_csv(sbd_file, sep=';', encoding='unicode-escape')
sbd_pres = df['CTD - Pressure (dbar)'].to_numpy()
sbd_temp = df['CTD - Temperature (°C)'].to_numpy()
sbd_psal = df['CTD - Salinity (PSU)'].to_numpy()
n = 1
while sbd_pres[-n] == 1000:
    sbd_pres = sbd_pres[:-n]
    sbd_temp = sbd_temp[:-n]
    sbd_psal = sbd_psal[:-n]

nc = Dataset(nc_file)
nc_pres = np.squeeze(nc['PRES'][:].data)
nc_temp = np.squeeze(nc['TEMP'][:].data)
nc_psal = np.squeeze(nc['PSAL'][:].data)

lat = nc['LATITUDE'][:].data[0]
lon = nc['LONGITUDE'][:].data[0]

sbd_pden = gsw.pot_rho_t_exact(gsw.SA_from_SP(sbd_psal, sbd_pres, lon, lat), sbd_temp, sbd_pres, 0) - 1000
nc_pden = gsw.pot_rho_t_exact(gsw.SA_from_SP(nc_psal, nc_pres, lon, lat), nc_temp, nc_pres, 0) - 1000

fig, axes = plt.subplots(1, 4, sharey=True)

n_sbd = sbd_pres.shape[0]
n_nc = nc_pres.shape[0]

thick = 4
thin = 1

axes[0].plot(sbd_temp, sbd_pres, label='SBD, $N={:d}$'.format(n_sbd), lw=thick)
axes[0].plot(nc_temp, nc_pres, label='netCDF, $N={:d}$'.format(n_nc), lw=thin)
axes[0].set_xlabel('TEMP ({}C)'.format(chr(176)))
axes[0].set_ylabel('PRES (dbar)')
axes[0].legend(loc=4, fontsize=8)

axes[1].plot(sbd_psal, sbd_pres, label='SBD, $N={:d}$'.format(n_sbd), lw=thick)
axes[1].plot(nc_psal, nc_pres, label='netCDF, $N={:d}$'.format(n_nc), lw=thin)
axes[1].set_xlabel('PSAL')

axes[2].plot(sbd_pden, sbd_pres, label='SBD, $N={:d}$'.format(n_sbd), lw=thick)
axes[2].plot(nc_pden, nc_pres, label='netCDF, $N={:d}$'.format(n_nc), lw=thin)
axes[2].set_xlabel('PDEN (kg m$^{-3}$)')

axes[3].plot(-np.diff(sbd_pres), sbd_pres[:-1] + np.diff(sbd_pres)/2, lw=thick)
axes[3].plot(np.diff(nc_pres), nc_pres[:-1] + np.diff(nc_pres)/2, lw=thin)
axes[3].set_xlabel('$\Delta$PRES (dbar)')

axes[0].set_ylim((2000,0))

w, h = fig.get_figwidth(), fig.get_figheight()
fig.set_size_inches(w*4/3, h)

fig.savefig(Path('../figures/nc_sbd/{}_gdac_sbd_overlay.png'.format(wmo)), bbox_inches='tight', dpi=350)

# plt.show()

plt.close()