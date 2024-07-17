
from pathlib import Path

import numpy as np
import pandas as pd
import argopandas as argo

asset_file = Path('/Users/GordonC/Documents/argo/meds/write-offs/ARGO Floats 420104.csv')
inventory_file = Path('/Users/GordonC/Documents/argo/meds/write-offs/WMOID+SN+IMEI_20230428.csv')

asset  = pd.read_csv(asset_file)
invent = pd.read_csv(inventory_file)

wmo_list = []

for s in asset.ManufSerialNumber:

    if type(s) is float:
        wmo = np.nan
    else:
        sn = 'SN' + s if len(s) < 4 else s
        wmo_series = invent.loc[invent.Serial == sn].WMOID
        wmo = wmo_series.iloc[0] if wmo_series.shape[0] > 0 else np.nan
        if np.isnan(wmo):
            print(sn, wmo)
    wmo_list.append(str(wmo))

asset['WMO'] = wmo_list

ct = pd.Timestamp('now', tz='utc')
old = pd.Timedelta(days=150)
delta_list = []
last_writeoff = [
    6040676, 6035471, 2016821, 6042148, 6042146, 
    6038196, 6038197, 6042155, 6042157, 6038203,
    6035472
]

for wmo, ass in zip(asset.WMO, asset['Inventory number']):
    if np.isnan(float(wmo)):
        delta_time = np.nan
    else:
        ix = argo.float(wmo).prof
        if ix.shape[0] == 0:
            delta_time = 0
        else:
            last_date = ix.date.iloc[-1]
            delta_time = ct - last_date
            if delta_time > old and ass not in last_writeoff:
                print(wmo, ass,  last_date.strftime('%b %d %y'), delta_time.days)
    delta_list.append(delta_time)