#!/usr/bin/python

from pathlib import Path
import pandas as pd

core_file = Path('../data/meds_operational_core.csv')
bgc_file  = Path('../data/meds_operational_bgc.csv')

cf = pd.read_csv(core_file)
bf = pd.read_csv(bgc_file)

nova  = cf[cf.MODEL == 'NOVA']
dova  = bf[bf.MODEL == 'NOVA']
arvor = cf[cf.MODEL == 'ARVOR']
arvor_do = bf[bf.MODEL == 'ARVOR']