
import sys

import pandas as pd
from pathlib import Path

import bgcArgoDMQC as bgc

# download last run July 11, 2024 - new profiles appropriately flagged - likely not necessary
download = False
if download:
    ix = bgc.io.read_index()
    ix = ix.loc[ix.institution == 'ME']
    ix['wmo'] = [int(f.split('/')[1]) for f in ix.file]
    for wmo in ix.wmo.unique():
        sys.stdout.write(f'downloading {wmo}...\n')
        bgc.io.get_argo(wmo, local_path=bgc.io.Path.ARGO_PATH, overwrite=True, mission='B')

# local file location
meds = Path(bgc.io.Path.ARGO_PATH) / 'meds'
wmo_paths = list(meds.glob('*'))
wmo_paths = [p.name for p in wmo_paths]

# get core index
ix = bgc.io.read_index()
ix['wmo'] = [f.split('/')[1] for f in ix.file]

# should be inclusive but downloaded files & in index
wmo_list = sorted(list(set(wmo_paths) & set(ix.wmo.values)))

# information for HISTORY_ variables
history = {
    "HISTORY_INSTITUTION":"BI",
    "HISTORY_STEP":"ARGQ",
    "HISTORY_ACTION":"CF",
    "HISTORY_PARAMETER":"DOXY",
}

# date for file naming
now = pd.Timestamp('now')

# open text file to log changes
with open(f'../docs/historical_doxy_qc_1_to_3_{now.month:02d}-{now.year}.txt', 'w') as changelog:
    for wmo in wmo_list:
        files = list((meds / wmo / 'profiles').glob('B*.nc'))
        changelog.write(f'[{wmo}]\n')
        for fn in files:
            sys.stdout.write(f'Checking for DOXY_QC=1 in file {fn.name}...')
            prof = bgc.prof(file=fn)
            # DOXY in file (there are some MTIME only B-files) and has DOXY_QC = 1 entries
            if ('DOXY_QC' in prof.df.columns) and (prof.df.DOXY_QC == 1).any():
                sys.stdout.write('found. Updating file...\n')
                changelog.write(f'{fn}\n')
                prof.update_field('DOXY_QC', 3, where=prof.DOXY_QC == 1)
                export_file = prof.update_file(history)
            else:
                sys.stdout.write('none found.\n')
