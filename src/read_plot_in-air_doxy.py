
from pathlib import Path
from netCDF4 import Dataset

import pandas as pd
import matplotlib.pyplot as plt

### PUT PATH TO YOUR FILE HERE ###
traj_file = Path('/Users/GordonC/Documents/data/Argo/dac/meds/4902481/4902481_BRtraj.nc')

### PUT PATH TO YOUR INDEX FILE HERE - WILL NEED TO BE UP TO DATE ###
index_file = Path('/Users/GordonC/Documents/projects/bgcArgoDMQC/bgcArgoDMQC/resource/data/Index/ar_index_global_prof.txt.gz')

# load netCDF dataset
traj = Dataset(traj_file)
index = pd.read_csv(index_file, compression='gzip', header=8)

# index for in-air data
ix_in_air = traj['PRES'][:].data <= 0

# extract in-air DOXY and date/cycle
in_air_doxy = traj['DOXY'][:].data[ix_in_air]
juld = traj['JULD'][:].data[ix_in_air]
cycle = traj['CYCLE_NUMBER'][:].data[ix_in_air]

# reduce index to only include our float
index['wmo'] = [int(f.split('/')[1]) for f in index.file]
index = index.loc[index.wmo == 4902481]
# get cycle number and profile direction
index['cycle'] = [int(f.split('_')[1].strip('.nc').strip('D')) for f in index.file]
# profile direction - we don't want descending profiles
index['direction'] = [f.split('.')[1][-1] if f.split('.')[1][-1] == 'D' else 'A' for f in index.file]
index = index.loc[index.direction == 'A']

# resolve cycle/lat/long from index
lat = pd.Series([index.loc[index.cycle == c].latitude.iloc[0] for c in cycle])
long = pd.Series([index.loc[index.cycle == c].longitude.iloc[0] for c in cycle])

# convert JULD (days since 1950) to pandas Timestamp
# datetime unix epoch is since 1970, Argo is from 1950, so need to adjust
offset = pd.Timestamp('1970-01-01') - pd.Timestamp('1950-01-01')
time = pd.Series([pd.Timestamp(j, unit='d') - offset for j in juld])

# plot in-air data
plt.plot(time, in_air_doxy, 'o')
plt.show()