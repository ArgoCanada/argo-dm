
import argopy
import bgcArgoDMQC as bgc

import matplotlib.pyplot as plt
import numpy as np

def nearest_psal(p1, p2, s):
    s_out = np.full_like(p1, np.nan)
    for i, pr in enumerate(p1):
        for j, p in enumerate(pr):
            s_out[i, j] = s[np.abs(p2 - p) == np.nanmin(np.abs(p2 - p))][0] if not np.isnan(p) else np.nan
    
    return s_out

index = argopy.ArgoIndex(index_file='bgc-b')
index.query.compose({'dac':'meds', 'profiler_label':'ARVOR-D'})

fs = argopy.gdacfs()

resid_files = []

for fn in index.files:
    bds = fs.open_dataset(fn)
    try:
        sds = fs.open_dataset(fn.replace('BR', 'SR').replace('BD', 'SD'))
    except FileNotFoundError:
        print(f'No S file found for {fn}, skipping.')
        continue
    psal = nearest_psal(bds['PRES'].data, sds['PRES'].data, sds['PSAL'].data)
    
    o2conc = bgc.unit.umol_per_sw_to_umol_per_L(
        bds['DOXY'].data,
        psal, bds['TEMP_DOXY'].data, 
        bds['PRES'].data, 
        np.full_like(psal, bds['LATITUDE'].data[0]), 
        np.full_like(psal, bds['LONGITUDE'].data[0])
    )

    ppox_converted = bgc.unit.doxy_to_pO2(o2conc, psal, bds['TEMP_DOXY'].data, bds['PRES'].data)

    if np.nanmean(np.abs(bds['PPOX_DOXY'].data.flatten() - ppox_converted.flatten())) > 1:
        print(f'High residuals found for {fn}.')
        resid_files.append(fn)
        fig, axes = plt.subplots(2, 2)
        axes = axes.flatten()
        axes[0].plot(bds['PPOX_DOXY'].data.flatten(), ppox_converted.flatten(), 'o')
        axes[0].set_xlabel('GDAC')
        axes[0].set_ylabel('Converted from DOXY')
        axes[0].set_title(fn)
        axes[1].plot(bds['DOXY'].data.flatten(), bds['PRES'].data.flatten(), 'o')
        axes[1].set_xlabel('DOXY')
        axes[1].set_ylabel('PRES')
        axes[2].plot(bds['TEMP_DOXY'].data.flatten(), bds['PRES'].data.flatten(), 'o')
        axes[2].plot(sds['TEMP'].data.flatten(), sds['PRES'].data.flatten(), 'o')
        axes[3].plot(psal.flatten(), bds['PRES'].data.flatten(), 'o')
        axes[1].set_ylim((4000, 0))
        axes[2].set_ylim((4000, 0))
        axes[3].set_ylim((4000, 0))
        axes[2].set_ylabel('PRES')
        axes[2].set_xlabel('TEMP & TEMP_DOXY')
        axes[3].set_xlabel('PSAL')
        plt.show()