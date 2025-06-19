
from pathlib import Path

import numpy as np
import pandas as pd
import argopy

import seaborn as sns
import matplotlib.pyplot as plt

ix = argopy.ArgoIndex().to_dataframe()
meds = ix.loc[ix.dac == 'meds']

wmo_numbers = [4902684, 4902685, 4902686, 4902687, 4902688]
imei_numbers = [
    '300125062902880',
    '300125062426150',
    '300125062423120',
    '300125062031400',
    '300125062035430',
]

meds = meds.loc[meds.wmo.isin(wmo_numbers)]
meds['date_exact'] = meds.date.values
meds['date'] = [pd.Timestamp(year=d.year, month=d.month, day=d.day, hour=d.hour) for d in meds.date]

meds = meds.set_index(['wmo', 'date'])

wmo_list = []
date_list = []
lat_list = []
lon_list = []

data_path = Path('../data/provor/')
for wmo, imei in zip(wmo_numbers, imei_numbers):
    # extract coordinates from tech files
    for fn in (data_path / imei).glob('*_technical.txt'):
        with open(fn) as fid:
            line = ''
            i = 0
            while line.strip() != '[GPS]' and i < 100:
                line = fid.readline()
                i += 1
            gps_string = fid.readline()

            if len(gps_string) != 0:
                # extract date/time
                utc_string = gps_string.split('UTC=')[1]
                print(utc_string[:17])
                date = pd.Timestamp(
                    year=2000+int(utc_string[:2]),
                    month=int(utc_string[3:5]),
                    day=int(utc_string[6:8]),
                    hour=int(utc_string[9:11])
                )
                print(date)
                date_list.append(date)

                # extract lat
                lat_string = gps_string.split('Lat=')[1]
                print(lat_string[:11])
                lat = float(lat_string[:2]) + float(lat_string[2:10])/60
                lat_dir = lat_string[10]
                lat = -lat if lat_dir == 'S' else lat
                print(lat)
                lat_list.append(lat)

                # extract long
                lon_string = gps_string.split('Long=')[1]
                print(lon_string[:12])
                lon = float(lon_string[:3]) + float(lon_string[3:11])/60
                lon_dir = lon_string[11]
                lon = -lon if lon_dir == 'W' else lon
                print(lon)
                lon_list.append(lon)

                wmo_list.append(wmo)
            
            else:
                lat = pd.NA
                lon = pd.NA

df = pd.DataFrame(dict(
    wmo=wmo_list, 
    date=date_list, 
    tech_file_lat=lat_list, 
    tech_file_lon=lon_list
))
df = df.set_index(['wmo', 'date'])

meds = meds.join(df, on=['wmo', 'date'])
meds['tech_file_lat_rounded'] = meds.tech_file_lat.round(decimals=3)
meds['tech_file_lon_rounded'] = meds.tech_file_lon.round(decimals=3)
meds['lat_diff'] = meds.latitude - meds.tech_file_lat_rounded
meds['lon_diff'] = meds.longitude - meds.tech_file_lon_rounded
meds['lat_rounding_diff'] = meds.latitude.abs() - np.floor(meds.latitude.abs())
meds['lon_rounding_diff'] = meds.longitude.abs() - np.floor(meds.longitude.abs())

fig, axes = plt.subplots(1, 2)
sns.histplot(data=meds, stat='count', x='lat_diff', hue='wmo', multiple='stack', ax=axes[0], bins=np.arange(-0.00125, 0.0005, 0.0005))
sns.histplot(data=meds, stat='count', x='lon_diff', hue='wmo', multiple='stack', ax=axes[1], legend=False, bins=np.arange(-0.25, 1.15, 0.1))
axes[1].set_ylabel('')
axes[1].set_yticks(list(range(0, 25, 5)))
fig.suptitle('Argo Index minus Technical File')
fig.savefig('../figures/cts5_lat_lon_index_tech_file_diff.png', bbox_inches='tight', dpi=350)

fig, axes = plt.subplots(1, 2)
sns.histplot(data=meds, stat='count', x='lat_rounding_diff', hue='wmo', multiple='stack', ax=axes[0], legend=False, bins=np.arange(0, 1.05, 0.05))
sns.histplot(data=meds, stat='count', x='lon_rounding_diff', hue='wmo', multiple='stack', ax=axes[1], bins=np.arange(0, 1.05, 0.05))
axes[1].set_ylabel('')
fig.suptitle('Argo Index Coordinate Decimal')
fig.savefig('../figures/cts5_lat_lon_index_decimal.png', bbox_inches='tight', dpi=350)