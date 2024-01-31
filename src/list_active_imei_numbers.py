
from pathlib import Path

import numpy as np
import pandas as pd
import argopandas as argo

ix = argo.prof[:]
ix = ix.loc[ix.institution == 'ME']
ix['wmo'] = [int(f.split('/')[1]) for f in ix.file]

ice_floats = [4902531, 4902610, 4902611]
recent_fails = [4902617, 4902689]
active_floats = ix.subset_date('2024-01')

deployed_wmo = np.append(np.array(ice_floats + recent_fails), active_floats.wmo.unique())

track = pd.read_csv(Path('/Users/GordonC/Documents/argo/meds/tracking/WMOID+SN+IMEI_20240130.csv'))
active_non_deployed = track.loc[(track.Date.isna()) & (track['Lab/Department'] != 'TAKUVIK')].WMO.unique()

active_comms = np.unique(np.append(deployed_wmo, active_non_deployed))
imei = [int(track.loc[track.WMO == wmo].IMEI.iloc[0]) for wmo in active_comms]
status = ['Active' if wmo in deployed_wmo else 'Undeployed' for wmo in active_comms]

active_imei = pd.DataFrame(dict(WMO=active_comms, IMEI=imei, Status=status))
now = pd.Timestamp('now')
active_imei.to_csv(f'../data/tracking/active_imei_numbers_{now.year}{now.month:02d}{now.day:02d}.csv')

inactive_imei = track.IMEI.loc[~track.IMEI.isin(imei)]
inactive_imei = inactive_imei.loc[inactive_imei.notna()].astype(np.int64)

billing = pd.read_csv(Path('/Users/GordonC/Documents/argo/meds/tracking/Bill_Code_Summary_Report_Excel_sept2023.csv'))
billing = billing.loc[billing['Billing Code'].isin(['153-1018', '153-1052'])]

bill_imei = [i.split('-')[0].strip() for i in billing['Circuit Number']]
bill_imei = [np.int64(i) if len(i) == 15 else np.nan for i in bill_imei]

billed_inactive = inactive_imei.loc[inactive_imei.isin(bill_imei)]
wmo = [int(track.loc[track.IMEI == b_imei].WMO.iloc[0]) for b_imei in billed_inactive]

print(pd.DataFrame(dict(WMO=wmo, IMEI=billed_inactive)))