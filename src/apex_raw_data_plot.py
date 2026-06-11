
from pathlib import Path

import pandas as pd

import matplotlib.pyplot as plt
import seaborn as sns

def apex_to_dataframe(fn):

    data = dict(
        TIME=[],
        PRES=[],
        TEMP=[],
        PSAL=[],
        sample=[]
    )

    with open(fn) as fid:
        lead = ' '
        mode = ''

        while lead != '':

            line = fid.readline()

            line_list = line.split(',')
            lead = line_list[0]

            if lead == 'Message':
                mode = line_list[2]
            elif lead in ('CTD_CP', 'CTD_PTS') and mode.strip() in ('CP Started', 'CP Stopped', 'Surface Mission'):
                data['TIME'].append(pd.Timestamp(line_list[1]))
                data['PRES'].append(float(line_list[2]))
                data['TEMP'].append(float(line_list[3]))
                data['PSAL'].append(float(line_list[4]))
                data['sample'].append(line_list[0])
    
    return pd.DataFrame(data)
       

datadir = Path('../dat/apex/')
sn = 10878
cycle = 24

fn = list((datadir / f'{sn}' / f'{cycle:03d}').glob('*science*'))[0]

df = apex_to_dataframe(fn)

fig, axes = plt.subplots(1, 2, sharey=True)
for ax, v in zip(axes, ('TEMP', 'PSAL')):
    sns.scatterplot(data=df, x=v, y='PRES', hue='sample', linewidth=0.25, ax=ax)

ax.set_ylim((2020, -20))
plt.show()