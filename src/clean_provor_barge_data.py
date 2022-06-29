
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

rudics_path = Path('../data/provor') / imei
data_files = [
    'CTD Measures (Average).csv',
    'CTD Measures (Raw data).csv',
    'DO Measures (Raw data).csv',
    'ECO2 Measures (Raw data).csv',
]

# ctd = pd.read_csv(
#     rudics_path / data_files[0],
#     sep=';', encoding='unicode-escape',
#     lineterminator='\r'
# )
# ctd = ctd[(ctd['Mean pressure (dbar)'].notna()) & (ctd['Mean pressure (dbar)'] > 0)]
# ctd = ctd.drop(['Unnamed: 0', 'Unnamed: 8'], axis=1)
# ctd = ctd.backfill()
# ctd = ctd.astype({'Cycle number':int, 'Profile number':int, 'Phase number':int})
# ctd['1st sample date'] = pd.to_datetime(ctd['1st sample date'])

# oxy = pd.read_csv(
#     rudics_path / data_files[2],
#     sep=';', encoding='unicode-escape',
#     lineterminator='\r'
# )
# oxy = oxy[(oxy['Pressure (dbar)'].notna()) & (oxy['Pressure (dbar)'] > 0)]
# oxy = oxy.drop(['Unnamed: 0', 'Unnamed: 9'], axis=1)
# oxy = oxy.backfill()
# oxy = oxy[oxy['Profile number'].notna()]
# oxy = oxy.astype({'Cycle number':int, 'Profile number':int, 'Phase number':int})
# oxy['1st sample date'] = pd.to_datetime(oxy['1st sample date'])

# eco = pd.read_csv(
#     rudics_path / data_files[3],
#     sep=';', encoding='unicode-escape',
#     lineterminator='\r'
# )
# eco = eco[(eco['Pressure (dbar)'].notna()) & (eco['Pressure (dbar)'] > 0)]
# eco = eco.drop(['Unnamed: 0', 'Unnamed: 8'], axis=1)
# eco = eco.fillna(method='backfill')
# eco = eco.astype({'Cycle number':int, 'Profile number':int, 'Phase number':int})
# eco['1st sample date'] = pd.to_datetime(eco['1st sample date'])

# ctd.to_hdf(Path(f'../data/provor/{imei}') / f'{wmo}_ctd.h5', key='df', mode='w')
# oxy.to_hdf(Path(f'../data/provor/{imei}') / f'{wmo}_optode.h5', key='df', mode='w')
# eco.to_hdf(Path(f'../data/provor/{imei}') / f'{wmo}_ecopuck.h5', key='df', mode='w')

# ctd.to_csv(Path(f'../data/provor/{imei}') / f'{wmo}_ctd.csv')
# oxy.to_csv(Path(f'../data/provor/{imei}') / f'{wmo}_optode.csv')
# eco.to_csv(Path(f'../data/provor/{imei}') / f'{wmo}_ecopuck.csv')

imei = imei_numbers[1]
wmo = wmo_numbers[1]

ctd = pd.read_csv(
    rudics_path / data_files[1],
    sep=';', encoding='unicode-escape',
    lineterminator='\r'
)
ctd = ctd[(ctd['Pressure (dbar)'].notna()) & (ctd['Pressure (dbar)'] > 0)]
ctd = ctd.drop(['Unnamed: 0', 'Unnamed: 8'], axis=1)
ctd = ctd.backfill()
ctd = ctd[ctd['Profile number'].notna()]
ctd = ctd.astype({'Cycle number':int, 'Profile number':int, 'Phase number':int})
ctd['1st sample date'] = pd.to_datetime(ctd['1st sample date'])

oxy = pd.read_csv(
    rudics_path / data_files[2],
    sep=';', encoding='unicode-escape',
    lineterminator='\r'
)
oxy = oxy[(oxy['Pressure (dbar)'].notna()) & (oxy['Pressure (dbar)'] > 0)]
oxy = oxy.drop(['Unnamed: 0', 'Unnamed: 9'], axis=1)
oxy = oxy.backfill()
oxy = oxy[oxy['Profile number'].notna()]
oxy = oxy.astype({'Cycle number':int, 'Profile number':int, 'Phase number':int})
oxy['1st sample date'] = pd.to_datetime(oxy['1st sample date'])

eco = pd.read_csv(
    rudics_path / data_files[3],
    sep=';', encoding='unicode-escape',
    lineterminator='\r'
)
eco = eco[(eco['Pressure (dbar)'].notna()) & (eco['Pressure (dbar)'] > 0)]
eco = eco.drop(['Unnamed: 0', 'Unnamed: 8'], axis=1)
eco = eco.fillna(method='backfill')
eco = eco.astype({'Cycle number':int, 'Profile number':int, 'Phase number':int})
eco['1st sample date'] = pd.to_datetime(eco['1st sample date'])

ctd.to_hdf(Path(f'../data/provor/{imei}') / f'{wmo}_ctd.h5', key='df', mode='w')
oxy.to_hdf(Path(f'../data/provor/{imei}') / f'{wmo}_optode.h5', key='df', mode='w')
eco.to_hdf(Path(f'../data/provor/{imei}') / f'{wmo}_ecopuck.h5', key='df', mode='w')

ctd.to_csv(Path(f'../data/provor/{imei}') / f'{wmo}_ctd.csv')
oxy.to_csv(Path(f'../data/provor/{imei}') / f'{wmo}_optode.csv')
eco.to_csv(Path(f'../data/provor/{imei}') / f'{wmo}_ecopuck.csv')