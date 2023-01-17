
from pathlib import Path
import ftplib
import numpy as np
import pandas as pd

import matplotlib.dates as mdates
import matplotlib.pyplot as plt
import seaborn as sns
sns.set(style='ticks')

import bgcArgoDMQC as bgc

### get latest DOXY audit
audit_file = 'ftp.mbari.org'
ftp = ftplib.FTP(audit_file)
ftp.login()
ftp.cwd('pub/BGC_argo_audits/DOXY/meds')
fn = ftp.nlst()[0]
local_file = Path(f'../data/audit/{fn}')
lf = open(local_file, 'wb')
ftp.retrbinary('RETR ' + fn, lf.write)
lf.close()

### read in audit file
df = pd.read_csv(local_file, sep='\t', header=25)
df['date'] = [mdates.datestr2num(t) for t in df['profile date']]

### loop through each float, calc O2sat and gains
for f in df.WMO.unique():
    sub = df.loc[df.WMO == f]
    syn = bgc.sprof(f)

    g = syn.plot('profiles', varlist=['O2Sat'])
    g.axes[0].set_ylim((200,0))

    syn.clean()
    gains = syn.calc_gains(ref='WOA')

    g = syn.plot('gain', ref='WOA')
    g.axes[0].set_title(f'WMO: {f}', loc='left', fontweight='bold')
    g.axes[0].plot(sub['date'], sub['flt O2 %sat'], '*')
    g.axes[1].plot(sub['date'], sub['WOA G_raw'], '*')

    plt.show()