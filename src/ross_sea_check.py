
import sys
import pandas as pd

import argopy

ross_sea_floats = [4902664, 4902665, 4902667, 4902668, 4902669, 4902698, 4902704]

ac = pd.read_csv('../../blog/deployment/ArgoCanada.csv')
ac = ac.set_index('WMO')

ix = argopy.ArgoIndex().load().to_dataframe()
ix = ix.loc[ix.wmo.isin(ross_sea_floats)]

sys.stdout.write('WMO\tIMEI\t\tCycle\tLast GDAC Date\tRecent SBD Emails\n')
for wmo in ross_sea_floats:
    sys.stdout.write(f'{wmo}\t{int(ac.loc[wmo,'IMEI'])}\t{ix.loc[ix.wmo == wmo,'cyc'].max()}\t{ix.loc[ix.wmo == wmo,'date'].max().strftime("%Y-%m-%d")}\n')