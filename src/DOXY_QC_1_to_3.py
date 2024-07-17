
import sys

from pathlib import Path

import bgcArgoDMQC as bgc

## download last run July 11, 2024 - new profiles appropriately flagged - likely not necessary

download = False
if download:
    ix = bgc.io.read_index()
    ix = ix.loc[ix.institution == 'ME']
    ix['wmo'] = [int(f.split('/')[1]) for f in ix.file]
    for wmo in ix.wmo.unique():
        sys.stdout.write(f'downloading {wmo}...\n')
        bgc.io.get_argo(wmo, local_path=bgc.io.Path.ARGO_PATH, overwrite=True, mission='B')

meds = Path(bgc.io.Path.ARGO_PATH) / 'meds'
wmo_paths = list(meds.glob('*'))
wmo_paths = [p.name for p in wmo_paths]

ix = bgc.io.read_index()
ix['wmo'] = [f.split('/')[1] for f in ix.file]

wmo_list = sorted(list(set(wmo_paths) & set(ix.wmo.values)))

history = {
    "HISTORY_INSTITUTION":"BI",
    "HISTORY_STEP":"ARGQ",
    "HISTORY_ACTION":"CF",
    "HISTORY_PARAMETER":"DOXY",
}

changelog = []

for wmo in wmo_list:
    files = list((meds / wmo / 'profiles').glob('B*.nc'))
    for fn in files:
        sys.stdout.write(f'Checking for DOXY_QC=1 in file {fn.name}...')
        prof = bgc.prof(file=fn)
        if ('DOXY_QC' in prof.df.columns) and (prof.df.DOXY_QC == 1).any():
            sys.stdout.write('found. Updating file...\n')
            changelog.append(fn)
            prof.update_field('DOXY_QC', 3, where=prof.DOXY_QC == 1)
            export_file = prof.update_file(history)
        else:
            sys.stdout.write('none found.\n')
