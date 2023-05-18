
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
old = pd.Timedelta(days=12)
delta_list = []

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
            if delta_time > old:
                print(wmo, ass,  last_date.strftime('%b %d %y'), delta_time.days)
    delta_list.append(delta_time)