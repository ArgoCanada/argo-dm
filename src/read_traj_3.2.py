#!/usr/bin/python

from pathlib import Path
from netCDF4 import Dataset

files = list(Path('/Users/gordonc/Documents/data/Argo-DM/traj_3.2').glob('*.nc'))
nc = Dataset(files[0])
