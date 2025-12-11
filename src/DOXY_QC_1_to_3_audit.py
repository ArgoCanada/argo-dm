
import sys

import pandas as pd
from pathlib import Path

import bgcArgoDMQC as bgc

# download last run August 26, 2025 - new profiles appropriately flagged - likely not necessary again?
download = False
if download:
    ix = bgc.io.read_index()
    ix = ix.loc[ix.dac == 'meds']
    ix['wmo'] = [int(f.split('/')[1]) for f in ix.file]
    for i, wmo in enumerate(ix.wmo.unique()):
        sys.stdout.write(f'downloading {wmo} ({i+1} of {ix.wmo.unique().shape[0]})...\n')
        bgc.io.get_argo(wmo, local_path=bgc.io.Path.ARGO_PATH, overwrite=True, mission='B')

# local file location
meds = Path(bgc.io.Path.ARGO_PATH) / 'meds'
wmo_paths = list(meds.glob('*'))
wmo_paths = [int(p.name) for p in wmo_paths[:-2]]

# get float appearing in audit index
audit = pd.read_csv('../data/audit/SUMMARY_QC1_floats_ALL_DACS_August2025.csv')
audit = audit.loc[audit.dac == 'meds']
# exclude floats recently submitted for D-mode
audit = audit.loc[~audit.WMO.isin([4900627, 4900879, 4900883, 4902386, 4902390, 4902410])]

# should be inclusive but downloaded files & in index
wmo_list = sorted(list(set(wmo_paths) & set(audit.WMO.values)))

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
        files = list((meds / f'{wmo}' / 'profiles').glob('B*.nc'))
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
