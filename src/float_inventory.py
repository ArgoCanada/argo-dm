#!/usr/bin/python

from pathlib import Path
from numpy import nan

import regex as re
import pandas as pd

# get various sources for float info
file_oce_ops = Path('/Users/GordonC/Documents/argo/meds/tracking/ocean-ops-meds-2021-11-05.csv')
file_cost_centre = file_oce_ops.parent / '420104_CG_BG.csv'
file_internal_tracking = file_oce_ops.parent / 'WMOID+SN+IMEI_20211026.csv'
# load into dataframes
df_oo = pd.read_csv(file_oce_ops)
df_cc = pd.read_csv(file_cost_centre, encoding= 'windows-1252')
df_it = pd.read_csv(file_internal_tracking, encoding= 'windows-1252')

# get only what Argo is responsible for
df_cc = df_cc[df_cc['Holder ID'] == 'BLAIR GREENAN, ARGO PROGRAM']

# active floats that are not in inventory
missing = df_oo[~df_oo['Serial'].isin(df_cc['ManufSerialNumber'])]

# parse internal serial number format, put into dataframe
serial = []
for sn in df_it['Serial #']:
    if type(sn) is str:
        if re.match('SN\d', sn):
            serial.append(str(int(sn[2:])))
        else:
            serial.append(sn)
    else:
        serial.append(nan)
df_it['Serial'] = serial

# get ones not included in the inventory, but this will also include inactive though
df_it = df_it[df_it['Serial'].notna()]
missing_or_inactive = df_it[~df_it['Serial'].isin(df_cc['ManufSerialNumber'])]

# export to csv and visually inspect
missing.to_csv(file_oce_ops.parent / 'missing_active_floats.csv')
missing_or_inactive.to_csv(file_oce_ops.parent / 'missing_or_inactive_floats.csv')