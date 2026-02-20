
from pathlib import Path

import pandas as pd

import argopy

index = argopy.ArgoIndex()

sbd_lib = Path('../data/baffin_bay/')
for wmo in sbd_lib.iterdir():
    if wmo.name != 'desktop.ini':
        print(wmo)
        data = pd.read_csv(wmo / 'Ascent profile CTD Message.csv', encoding='unicode_escape', sep=';')
        for colname in data.columns:
            if 'Unnamed' in colname:
                data = data.drop(colname, axis=1)
            
        rawtech = pd.read_csv(wmo / 'Technical Message 1.csv', encoding='unicode_escape', sep=';')

        prefix = ''
        tech = pd.DataFrame()

        for ix in rawtech.index:

            header = rawtech.loc[ix, 'Header']

            if type(header) is str:
                if header[0] == '-':
                    prefix = header.strip('-')
                else:
                    tech[f'{prefix} : {header}'] = rawtech.loc[ix].iloc[1:].values

        gi = 'GENERAL INFORMATIONS : Float time :'
        tech['date'] = [
            pd.Timestamp(
                year=int(row[1][f'{gi} Year'])+2000,
                month=int(row[1][f'{gi} Month']),
                day=int(row[1][f'{gi} Day']),
                hour=int(row[1][f'{gi} Hour']),
                minute=int(row[1][f'{gi} Minute']),
                second=int(row[1][f'{gi} Second'])
            ) for row in tech.iterrows()
        ]

        gi = 'GENERAL INFORMATION :'
        tech['cycle'] = [int(c) for c in tech[f'{gi} Cycle number']]
        
        flt = index.query.wmo(wmo.name).to_dataframe()

        extra_tech_cycles = list(set(tech.cycle.unique()) - set(flt.cyc.unique()))