
from pathlib import Path
import copy
import pandas as pd
from netCDF4 import Dataset

def file(fn):
    root = Path('/Users/GordonC/Documents/data/Argo/dac/meds/E/')
    return root / fn.split('_')[0].strip('BRD') / 'profiles' / fn

def orig_file(fn):
    return Path(fn.as_posix().replace('/E/', '/'))

base = Path('../../filecheck-summarizer/summary/')

if (base / '4900882/files.txt').exists():
    for fn in pd.read_csv(base / '4900882/files.txt').files:
        ec = Dataset(file(fn), 'r+')
        nc = Dataset(orig_file(file(fn)))
        ec['DOXY'][:] = nc['DOXY'][:].data
        ec['MOLAR_DOXY'][:] = nc['MOLAR_DOXY'][:].data
        nc.close()
        ec.close()

for wmo in ['4901785', '4901791', '4902384', '4902386']:
        if (base / wmo / 'files.txt').exists():
            for fn in pd.read_csv(base / wmo / 'files.txt').files:
                ec = Dataset(file(fn), 'r+')
                data_mode = copy.deepcopy(ec['PARAMETER_DATA_MODE'][:])
                data_mode[0,0] = b'R'
                ec['PARAMETER_DATA_MODE'][:] = data_mode
                ec.close()

for wmo in ['4901785', '4901790', '4901791', '4902383', '4902384', '4902386']:
     if (base / wmo / 'files.txt').exists():
            for fn in pd.read_csv(base / wmo / 'files.txt').files:
                ec = Dataset(file(fn), 'r+')
                data_mode = copy.deepcopy(ec['DATA_MODE'][:])
                data_mode[0] = b'R'
                ec['DATA_MODE'][:] = data_mode
                ec.close()