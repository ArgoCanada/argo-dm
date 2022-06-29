
from pathlib import Path
import pandas as pd

imei_numbers = [
    '300125061656740',
    '300125061360970',
]

wmo_numbers = [
    '4902598',
    '4902599',
]

imei = imei_numbers[0]
wmo = wmo_numbers[0]

rudics_path = Path('../data/provor')
data_files = [
    'CTD Measures (Average).csv',
    'DO Measures (Raw data).csv',
    'ECO2 Measures (Raw data).csv',
]
sensors = [
    'ctd',
    'optode',
    'ecopuck',
]

for imei, wmo in zip(imei_numbers, wmo_numbers):
    for f, s in zip(data_files, sensors):
        df = pd.read_csv(
            rudics_path / imei / f,
            sep=';', encoding='unicode-escape',
            lineterminator='\r'
        )
        if s == 'ctd':
            df = df.rename(columns={'Mean pressure (dbar)':'Pressure (dbar)'})
        df = df[(df['Pressure (dbar)'].notna()) & (df['Pressure (dbar)'] > 0)]
        for c in df.columns:
            if 'Unnamed' in c:
                df = df.drop(c, axis=1)
        df = df.backfill()
        df = df[df['Profile number'].notna()]
        df = df.astype({'Cycle number':int, 'Profile number':int, 'Phase number':int})
        df['1st sample date'] = pd.to_datetime(df['1st sample date'])
        df.to_hdf(Path(f'../data/provor/{imei}') / f'{wmo}_{s}.h5', key='df', mode='w')
        df.to_csv(Path(f'../data/provor/{imei}') / f'{wmo}_{s}.csv')