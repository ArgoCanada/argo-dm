
from pathlib import Path

import matplotlib.pyplot as plt
import seaborn as sns
sns.set(style='ticks', palette='colorblind')

import pandas as pd


def read_cts5_file(fn):

    column_dict = dict(
        sbe41=['date', 'pres', 'temp', 'psal', 'phase', 'processing'],
        do=['date', 'pres', 'tphase', 'rphase', 'temp_doxy', 'phase', 'processing'],
        eco=['date', 'pres', 'channel_1', 'channel_2', 'phase', 'processing'],
        ocr=['date', 'pres', 'channel_1', 'channel_2', 'channel_3', 'channel_4', 'phase', 'processing']
    )

    sensor = fn.as_posix().split('_')[-1].split('.')[0]

    columns = column_dict[sensor]

    df = pd.DataFrame(columns=columns)

    with open(fn) as f:
        for line in f:
            if line[0] == '[':
                phase = line.strip('[ ]\n')
            elif line[0] == '(':
                processing = line.strip('( )\n')
            else:
                data = line.strip().split(',') + [phase, processing]
                data[0] = pd.Timestamp(data[0])
                data[1:-2] = [float(x) for x in data[1:-2]]
                df = df.append({k:v for k, v in zip(columns, data)}, ignore_index=True)

    return df

fig, axes = plt.subplots(2, 3, sharey=True, constrained_layout=True)

varnames = ['temp', 'psal', 'tphase', 'channel_1', 'channel_2', 'channel_2']
sensors = ['sbe41', 'sbe41', 'do', 'eco', 'eco', 'ocr']
colors = ['darkred', 'darkgreen', 'darkblue', 'green', 'red', 'black']

prev_sensor = None
for i in [21, 22, 23]:
    for variable, sensor, ax, color in zip(varnames, sensors, axes.flatten(), colors):
        if sensor != prev_sensor:
            fn = Path(f'../data/provor/300125062902880/59e0_0{i}_01_{sensor}.csv')
            df = read_cts5_file(fn)
        df = df.loc[df.phase == 'ASCENT']

        sns.lineplot(data=df, x=variable, y='pres', color=color, sort=False, estimator=None, ax=ax)
        ax.set_xlabel(f'{sensor}:{variable}')
        prev_sensor = sensor
axes[0,0].set_ylim((1050, -50))
plt.show()

fig.savefig('initial_cts5_profiles.png', dpi=300, bbox_inches='tight')
