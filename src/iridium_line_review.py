
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

lines['plan'] = lines.shape[0]*[' ']
lines['rate'] = lines.shape[0]*[pd.NA]

rates = {'b':21.45, 'f':23.54, 'z':27.47+30*0.86}

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

        if lines.loc[j, 'active'] not in ['n', 'y']:
            print()
            if latest == 2026:
                lines.loc[j, 'active'] = 'y'
            else:
                lines.loc[j, 'active'] = input('Active? (y/n): ')
        
        fltinfo = argo.loc[imei].iloc[0] if len(argo.loc[imei].shape) > 1 else argo.loc[imei]

        if fltinfo['Serial'].split('-')[0] == 'AI2600':
            lines.loc[j, 'plan'] = 'b'
        elif fltinfo['Serial'].split('-')[0] == 'AI2632':
            lines.loc[j, 'plan'] = 'f'
        elif fltinfo['Serial'].split('-')[0][0] == 'P':
            lines.loc[j, 'plan'] = 'z'
        elif fltinfo['Model'] == 'NOVA-CTD':
            lines.loc[j, 'plan'] = 'b'
        elif fltinfo['Model'] == 'DOVA':
            lines.loc[j, 'plan'] = 'b'
        else:
            lines.loc[j, 'plan'] = input('Plan? (b/f/z): ')

lines = lines.loc[lines.plan.isin(['b', 'f', 'z'])]
lines['rate'] = [rates[p] for p in lines.plan]
        
        

lines.to_csv('../data/tracking/iridium_cost_centre_review.csv')
