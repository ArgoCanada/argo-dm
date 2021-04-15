#!/usr/bin/python

from pathlib import Path

import matplotlib.pyplot as plt
import bgcArgoDMQC as bgc

floats = [4902555, 4902552, 4902553, 4902554, 4902555]
fig, axes = plt.subplots(1, len(floats), sharex=True, sharey=True)
for i,f in enumerate(floats):
    # bgc.io.get_argo(f, local_path=bgc.ARGO_PATH)
    syn = bgc.sprof(f)
    syn.plot('profiles', varlist=['DOXY'], axes=axes[i])
    axes[i].set_title('WMO: {}'.format(f))

for ax in axes[1:]:
    ax.set_ylabel('')

# axes[0].set_ylim((400,0))

fig.suptitle('Recently Deployed ARVOR-DO Floats\nDarker colours represent more recent profiles', va='baseline')
fig.set_size_inches(9*1.15, 3*1.15)
fig.savefig(Path('../figures/doxy_options.png'), bbox_inches='tight', dpi=350)