#!/usr/bin/python

from pathlib import Path
import copy
import numpy as np
import pandas as pd

curr_oper = pd.read_csv(Path('../data/arvor-canada-operational_ocean-ops.csv'))
to_deploy = pd.read_csv(Path('/Users/gordonc/Documents/argo/meds/2021-deployment-plan-ocean-ops.csv'))

drop_list = [
    'PROGRAM', 'DEPLOYMENT DATE', 'DEPLOYMENT LAT',
    'DEPLOYMENT LON', 'LAST LOCATION DATE', 'SENSOR MODELS',
    'STATUS'
]

plan = copy.deepcopy(curr_oper)
for key in drop_list:
    plan = plan.drop(key, axis=1)

plan['CURRENT PLAN'] = np.array([3 if 'BioGeoChemical' in n else 2 for n in plan.NETWORKS])
plan['NEW PLAN'] = plan['CURRENT PLAN'] + 1

plan.to_csv(Path('../data/arvor-data-plan-change.csv'))