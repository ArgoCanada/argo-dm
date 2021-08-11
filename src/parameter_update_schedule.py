#!/usr/bin/python

from pathlib import Path

import datetime
import numpy as np
import pandas as pd

import bgcArgoDMQC as bgc

# get index
ix = bgc.get_index('global', dac='meds', profiler_type=844)
df = pd.read_csv(Path('../docs/parameter_change_tracking.csv'))
df = df[df.n_pts < 150]

# keep only the most recent profile for each float
for wmo in ix.wmo.unique():
    ix = ix.drop(ix.index[ix.wmo == wmo][ix[ix.wmo == wmo].cycle != ix[ix.wmo == wmo].cycle.max()])
# recently greylisted float
ix = ix.drop(ix.index[ix.wmo == 4902480])
ix = ix[ix.wmo.isin(df.wmo)]

# parse dates
datestr = [str(int(d)) for d in ix.date]
ix['time'] = np.array([datetime.datetime(int(d[:4]), int(d[4:6]), int(d[6:8]), int(d[8:10]), int(d[10:12]), int(d[12:])) for d in datestr])

# drop some unncessary columns - for export later
ix = ix.drop('date_update', axis=1)
ix = ix.drop('institution', axis=1)
ix = ix.drop('ocean', axis=1)

# get the IMEI number
imei_sheet = Path('../data/arvor-canada-operational_ocean-ops.csv')
imei = pd.read_csv(imei_sheet)
ix['imei'] = [imei.IMEI[imei.REF == w].values[0] for w in ix.wmo]
ix['program'] = [imei.NETWORKS[imei.REF == w].values[0] for w in ix.wmo]

# next surfacing date
ix['parameter_change_date'] = ix.time + datetime.timedelta(days=10)

# define a date where I will send the first message
start_date = datetime.datetime(2021, 5, 25)
# get the start date that is after the message sending date
for i in ix.index[ix.parameter_change_date < start_date]:
    ix.parameter_change_date[i] += datetime.timedelta(days=10)
ix.parameter_change_date = [d.date() for d in ix.parameter_change_date]
# email date
ix['email_date'] = ix['parameter_change_date'] - datetime.timedelta(days=2)
ix['email_date'] = [d+datetime.timedelta(days=1) if d.weekday() == 6 else d for d in ix.email_date]

# sort by parameter change date
ix = ix.sort_values('parameter_change_date')
ix = ix.reset_index()

# add columns for tracking
ix['message_drafted'] = ix.shape[0]*['No']
ix['message_sent'] = ix.shape[0]*['No']
ix['message_received_confirmed'] = ix.shape[0]*['No']

# export to csv
ix = ix.rename(columns={'file':'latest_file'})
# ix = ix[ix.email_date > datetime.date.today()]
ix = ix.drop('level_0', axis=1)
ix = ix.drop('index', axis=1)
ix.to_csv(Path('../docs/parameter_change_tracking_missed.csv'))