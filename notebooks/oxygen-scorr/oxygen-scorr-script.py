
import pandas as pd
from netCDF4 import Dataset
# import argopy
import bgcArgoDMQC as bgc

# floats with twice applied Scorr / Sref = 35
floats_of_interest = [4901137, 4901135, 4901139, 4901140, 4901141, 4901142, 4901134]

# download the data
download = False # can turn off after ran once
if download:
    for flt in floats_of_interest:
        bgc.io.get_argo(flt, local_path='./data')

# convenience function load nc variables into dataframe
def nc_to_df(nc):
    data = {k:v[:] for k, v in nc.variables.items() if len(v.dimensions) == 1 and v.dimensions[0] == 'N_MEASUREMENT'}
    df = pd.DataFrame(data)
    return df

for flt in floats_of_interest:
    fn = f'data/meds/{flt}/{flt}_Rtraj.nc'
    nc = Dataset(fn)
    df = nc_to_df(nc)
    break