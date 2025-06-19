
from pathlib import Path

import numpy as np
import pandas as pd
import argopy

asset_file = Path('/Users/GordonC/Documents/argo/meds/write-offs/ARGO Floats 420103.csv')
inventory_file = Path('/Users/GordonC/Documents/argo/meds/write-offs/ArgoCanada.csv')

asset  = pd.read_csv(asset_file)
invent = pd.read_csv(inventory_file)

wmo_list = []

for s in asset.ManufSerialNumber:

    if type(s) is float:
        wmo = np.nan
    else:
        sn = 'SN' + s if len(s) < 4 else s
        sn = sn.replace('DE', 'CA')
        wmo_series = invent.loc[invent.Serial == sn].WMO
        wmo = wmo_series.iloc[0] if wmo_series.shape[0] > 0 else np.nan
        if np.isnan(wmo):
            print(sn, wmo)
    wmo_list.append(str(wmo))

asset['WMO'] = wmo_list

ct = pd.Timestamp('now')
old = pd.Timedelta(days=150)
delta_list = [4902565] # deployed failed floats, no profiles
last_writeoff = []
ross_sea = [4902664, 4902665, 4902667, 4902668, 4902669]
beaufort_sea = [4902659, 4902610, 4902611]

exception_list = last_writeoff+ross_sea+beaufort_sea

argo = argopy.IndexFetcher(mode='expert', src='gdac')

for wmo, ass, sn in zip(asset.WMO, asset['Inventory number'], asset['ManufSerialNumber']):
    if np.isnan(float(wmo)):
        delta_time = np.nan
    elif invent.loc[invent.WMO == int(wmo), 'Datestring'].isna().item():
        delta_time = np.nan
    elif int(wmo) not in delta_list:
        ix = argo.float(wmo).to_dataframe()
        if ix.shape[0] == 0:
            delta_time = 0
        else:
            last_date = ix.date.max()
            delta_time = ct - last_date
            if delta_time > old and int(wmo) not in exception_list:
                print(wmo, ass, sn,  last_date.strftime('%b %d %y'), delta_time.days)
    else:
        print(f'Error: {wmo} not processed.')
        
    delta_list.append(int(wmo))