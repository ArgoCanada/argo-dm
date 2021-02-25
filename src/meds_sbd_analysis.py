#!/usr/bin/python

from pathlib import Path
from netCDF4 import Dataset

import bgcArgoDMQC as bgc

# some indexing to choose floats
# get core and bgc profiles for meds dac
gx = bgc.get_index(index='global')
bx = bgc.get_index()
gx = gx[gx.dac == 'meds']
bx = bx[bx.dac == 'meds']

# get arvor floats only
gx = gx[gx.profiler_type == 844]
bx = bx[bx.profiler_type == 844]

# get core files only
gx = gx[~gx.wmo.isin(bx.wmo)]

flts = [4902543,4902544,4902545,4902546,4902547,6903075]
for f in flts:
    dac = bgc.io.get_dac(f)
    fpath = Path(bgc.ARGO_PATH) / '{}/{}/profiles'.format(dac,f)
    files = list(fpath.glob('*.nc'))
    print(f, files[-1], len(files))
    if f == flts[-1]:
        files = [files[-3]]
    npts = 0
    for fn in files:
        nc = Dataset(fn)
        npts = npts + nc.dimensions['N_LEVELS'].size
    print(npts, len(list(nc.variables.keys())))