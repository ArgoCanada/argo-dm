
from pathlib import Path

import pandas as pd
import argopandas as argo

ix = argo.prof[:]
meds = ix.loc[(ix.institution == 'ME') & (ix.profiler_type == 844)]
meds['wmo'] = [int(f.split('/')[1]) for f in meds.file]

today = pd.Timestamp('now', tz='UTC')
profile_soon_lower = (today - pd.Timedelta(hours=235)).strftime('%Y-%m-%d')
profile_soon_upper = (today - pd.Timedelta(days=8)).strftime('%Y-%m-%d')

reprogram = meds.subset_date(profile_soon_lower, profile_soon_upper)

imei_info = pd.read_csv(Path('/Users/GordonC/Documents/argo/meds/tracking/WMOID+SN+IMEI_20240130.csv'))
reprogram['imei'] = [int(imei_info.loc[imei_info.WMO == wmo].IMEI.iloc[0]) for wmo in reprogram.wmo]

sent = pd.read_csv(Path('../data/tracking/MC28_sent.csv'))
reprogram = reprogram.loc[~reprogram.imei.isin(sent.imei)]

for imei in reprogram.imei:
    print(imei)
    input()