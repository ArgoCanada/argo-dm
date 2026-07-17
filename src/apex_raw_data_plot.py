
from pathlib import Path

import pandas as pd

import matplotlib.pyplot as plt
import seaborn as sns

def apex_to_dataframe(fn=None, kind='sbe'):

    data = dict(
        CYCLE=[],
        TIME=[],
        PRES=[],
        TEMP=[],
        PSAL=[],
        sample=[]
    )

    leads = ('CTD_CP', 'CTD_PTS') if kind == 'sbe' else ('LGR_PTSCI', 'LGR_CP_PTSCI')
    modes = ('CP Started', 'CP Stopped', 'Surface Mission') if kind == 'sbe' else ('CP started', 'CP stopped', 'Surface Mission')

    if fn is not None:
        with open(fn) as fid:
            lead = ' '
            mode = ''

            while lead != '':

                line = fid.readline()

                line_list = line.split(',')
                lead = line_list[0]

                if lead == 'Message':
                    mode = line_list[2].strip()
                elif lead in leads and mode in modes:
                    data['TIME'].append(pd.Timestamp(line_list[1]))
                    data['PRES'].append(float(line_list[2]))
                    data['TEMP'].append(float(line_list[3]))
                    data['PSAL'].append(float(line_list[4]))
                    data['sample'].append(line_list[0])
                data['CYCLE'] = len(data['TIME'])*[int(fn.name.split('.')[1])]
    
    return pd.DataFrame(data)
       

sn = 11421
kind = 'rbr'
datadir = Path(f'../dat/apex/{sn}')

df = pd.concat([apex_to_dataframe(list(cyc.glob('*science*'))[0], kind=kind) if int(cyc.name) > 0 else apex_to_dataframe() for cyc in datadir.glob('*')])

fig, axes = plt.subplots(1, 2, sharey=True)
for ax, v in zip(axes, ('TEMP', 'PSAL')):
    sns.scatterplot(data=df, x=v, y='PRES', hue='sample', linewidth=0.25, ax=ax)

ax.set_ylim((2020, -20))
ax.set_xlim((34.5, 35))
fig.savefig(f'../figures/apex_{sn}.png', dpi=350, bbox_inches='tight')