
import warnings
warnings.filterwarnings('ignore')

import sys

import argopy
import pandas as pd

ix = argopy.ArgoIndex().load()

def parse_iridium_id(idstring):

    if '/' in idstring:
        ids = idstring.split('/')
        return int(ids[1])
    elif '-' in idstring:
        ids = idstring.split('-')
        if len(ids[0]) > len(ids[1]):
            return int(ids[1])
        else:
            return int(ids[0])
    else:
        return int(idstring)


lines = pd.read_csv('../data/tracking/iridium_cost_centre_review.csv')
lines['imei'] = lines['ID'].apply(parse_iridium_id)

argo = pd.read_csv('/Users/GordonC/Documents/projects/blog/deployment/ArgoCanada.csv')
argo = argo.loc[argo.IMEI.notna()]
argo['IMEI'] = argo.IMEI.astype(int)
argo = argo.set_index('IMEI')

lines['active'] = lines.shape[0]*[' ']


for j in lines.index:
    imei = lines.loc[j, 'imei']
    if imei in argo.index:
        print()
        print(argo.loc[imei])
        try:
            latest = ix.query.wmo(argo.loc[imei, 'WMO']).to_dataframe().date.max()
            print(latest)
            latest = latest.year
        except:
            print('argopy fetch failed')
            latest = -1

        print()
        if latest == 2026:
            lines.loc[j, 'active'] = 'y'
        else:
            lines.loc[j, 'active'] = input('Active? (y/n): ')

lines.to_csv('../data/tracking/iridium_cost_centre_review.csv')
