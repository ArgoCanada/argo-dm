
from pathlib import Path
from netCDF4 import Dataset

import pandas as pd
import matplotlib.pyplot as plt

### PUT PATH TO YOUR FILE HERE ###
traj_file = Path('/Users/GordonC/Documents/data/Argo/dac/meds/4902481/4902481_BRtraj.nc')

# load netCDF dataset
traj = Dataset(traj_file)

# index for in-air data
ix_in_air = traj['PRES'][:].data <= 0

# extract in-air DOXY and date/cycle
in_air_doxy = traj['DOXY'][:].data[ix_in_air]
juld = traj['JULD'][:].data[ix_in_air]
cycle = traj['CYCLE_NUMBER'][:].data[ix_in_air]

# convert JULD (days since 1950) to pandas Timestamp
# datetime unix epoch is since 1970, Argo is from 1950, so need to adjust
offset = pd.Timestamp('1970-01-01') - pd.Timestamp('1950-01-01')
time = pd.Series([pd.Timestamp(j, unit='d') - offset for j in juld])

# plot in-air data
plt.plot(time, in_air_doxy, 'o')
plt.show()