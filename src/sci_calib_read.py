
from netCDF4 import Dataset
# from bgcArgoDMQC.io import read_ncstr

# defining read_ncstr so you don't have to install bgcArgoDMQC if that is
# a problem, comment out if you have the package installed
import numpy as np
def read_ncstr(arr):
    arr = arr.data if hasattr(arr, 'mask') else arr
    decode_str = np.array([f.decode('utf-8') for f in arr])
    out = ''.join(decode_str)

    return out.strip()

# function to get the value of a varname (ex. 'dS' or 'r') from the coeff string
def find_value(coeff, varname):
    # look for varname and equals sign
    v_str = f'{varname}='
    var_loc = coeff.find(v_str)

    # add a space if you don't find it
    v_str = f'{varname} =' if var_loc == -1 else var_loc
    var_loc = coeff.find(v_str) if var_loc == -1 else var_loc

    value = float(coeff[(var_loc + len(v_str)):].split('(')[0]) if var_loc != -1 else 'n/a'
    error = float(coeff[(var_loc + len(v_str)):].split('+/-')[1].split(')')[0])

    return value, error

# put your fileanme here
fn = '/Users/GordonC/Documents/data/Argo/dac/meds/4900870/profiles/D4900870_001.nc'
nc = Dataset(fn)

comment = read_ncstr(nc['SCIENTIFIC_CALIB_COMMENT'][:][0,0,2,:])
coeff = read_ncstr(nc['SCIENTIFIC_CALIB_COEFFICIENT'][:][0,0,2,:])

# I don't have the file, so replace coeff to parse
coeff = 'r =0.9999(+/-0), vertically averaged dS =-0.005(+/-0.001) in PSS-78.'

# get variable values, doing r as well though its not in the result str
r, r_err = find_value(coeff, 'r')
dS, dS_err = find_value(coeff, 'dS')
# this will return n/a for both, not sure if there is usually an error
# if it does exist in the string so the error field might be nonsense
cpcor, _ = find_value(coeff, 'cpcor')

history_date = read_ncstr(nc['HISTORY_DATE'][:][-1,0,:])
dd = history_date[6:8]
mm = history_date[4:6]
yyyy = history_date[:4]

result = f'PSAL ADJUST [dd mm yyyy N S_off stddev] {dd} {mm} {yyyy} {dS} {dS_err} |cpcor={cpcor}'
print(result)