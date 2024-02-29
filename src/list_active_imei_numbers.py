
from pathlib import Path

import ftplib

import numpy as np
import pandas as pd
import argopandas as argo

ix = argo.prof[:]
ix = ix.loc[ix.institution == 'ME']
ix['wmo'] = [int(f.split('/')[1]) for f in ix.file]
ix = ix.loc[ix.date.notna()]

ice_floats = [4902530, 4902531, 4902610, 4902611]
recent_fails = [4902617, 4902689]
recent_deploys = [4902665]
active_floats = ix.subset_date('2023-10')

deployed_wmo = np.append(np.array(ice_floats + recent_fails + recent_deploys), active_floats.wmo.unique())

track = pd.read_csv(Path('/Users/GordonC/Documents/argo/meds/tracking/WMOID+SN+IMEI_20240208.csv'), dtype={'SIM':str})
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
billing = billing.loc[billing['Circuit Number'].notna()]

bill_imei = billing['Circuit Number']
billed_inactive = inactive_imei.loc[inactive_imei.isin(bill_imei)]
wmo = [int(track.loc[track.IMEI == b_imei].WMO.iloc[0]) for b_imei in billed_inactive]
to_deactivate = pd.DataFrame(
    dict(
        IMEI=billing.loc[billing['Circuit Number'].isin(billed_inactive)]['Circuit Number'].values,
        Charge=billing.loc[billing['Circuit Number'].isin(billed_inactive)]['Net Charges'].values,
        BillCode=billing.loc[billing['Circuit Number'].isin(billed_inactive)]['Billing Code'].values,
    )
)
to_deactivate = to_deactivate.reset_index().drop('index', axis=1)

print(to_deactivate)
to_deactivate.to_csv(f'../data/tracking/to_deactivate_imei_numbers_{now.year}{now.month:02d}{now.day:02d}.csv')

for col in track:
    if 'Unnamed' in col:
        track = track.drop(col, axis=1)
track['Last Profile'] = [ix.loc[ix.wmo == w].date.iloc[-1].strftime('%Y/%m/%d') if w in ix.wmo.values else 'No profile' for w in track.WMO]

print(track.loc[track.WMO.isin(wmo)].to_string())

ftp = ftplib.FTP('ftp.joubeh.com', user='dfobio', passwd='976143')
provor_imei = [np.int64(i) for i in ftp.nlst()]
provor_sim = [np.int64(i) for i in track.loc[track.SIM.notna()].SIM]

bio_gliders = [
    8988169234001519859,
    8988169234001519875,
    8988169234001519883,
    8988169234001519891,
    8988169234001754811,
]

ios_gliders = [
    8988169234001823509,
    8988169234001290907,
    8988169234002615334,
    8988169234001749225,
    8988169234003917655,
    8988169234003917663,
    8988169234003917630,
    8988169234003917648,
    8988169234003917689,
    8988169234004449047,
    8988169234004449153,
    8988169224000681180,
]

non_argo = bill_imei.loc[~bill_imei.isin(track.IMEI)]
non_argo = non_argo.loc[~non_argo.isin(provor_imei)]
non_argo = non_argo.loc[~non_argo.isin(provor_sim)]

unidentified = non_argo.loc[~non_argo.isin(bio_gliders + ios_gliders)]
print(non_argo)

print(billing.loc[billing['Circuit Number'].isin(unidentified.values)][['Billing Code', 'Circuit Number', 'Net Charges']])
print(billing.loc[billing['Circuit Number'].isin(bio_gliders)][['Billing Code', 'Circuit Number', 'Net Charges']])
print(billing.loc[billing['Circuit Number'].isin(ios_gliders)][['Billing Code', 'Circuit Number', 'Net Charges']])
