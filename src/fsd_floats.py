#!/usr/bin/python

from pathlib import Path

import matplotlib.pyplot as plt
import cmocean.cm as cmo
import seaborn as sns
sns.set(style='ticks', palette='colorblind')

import gsw
import argopy
argopy.set_options(mode='expert')
fetcher = argopy.DataFetcher()

wmo = 4902502
dep = 1900
df = fetcher.float(wmo).to_dataframe()
df = df[df.PRES > dep]

# profiles
fig, axes = plt.subplots(1, 2, sharey=True)
for i in df.CYCLE_NUMBER.unique():
    sub = df[df.CYCLE_NUMBER == i]
    axes[0].plot(sub.TEMP, sub.PRES)
    axes[1].plot(sub.PSAL, sub.PRES)

axes[0].set_ylim((1000,0))
axes[0].set_ylabel('PRES (dbar)')
axes[0].set_xlabel('TEMP ({}C)'.format(chr(176)))
axes[1].set_xlabel('PSAL')


fig.suptitle('Float {}'.format(wmo))

fig.savefig(Path('../figures/{}_profiles_deep.png'.format(wmo)), bbox_inches='tight', dpi=300)
plt.close(fig)

# ts diagram
fig, ax = plt.subplots()
ax.plot(df.PSAL, df.TEMP, 'k.')
ax.set_xlabel('PSAL')
ax.set_ylabel('TEMP ({}C)'.format(chr(176)))
ax.set_title('{} TS Diagram (state variables)'.format(wmo))

fig.savefig(Path('../figures/{}_ts_diagram_deep.png'.format(wmo)), bbox_inches='tight', dpi=300)
plt.close(fig)

# ts diagram with SA and theta
SA = gsw.SA_from_SP(df.PSAL, df.PRES, df.LONGITUDE, df.LATITUDE)
theta = gsw.pt0_from_t(SA, df.TEMP, df.PRES)

fig, ax = plt.subplots()
ax.plot(SA, theta, 'k.')
ax.set_xlabel('SA')
ax.set_ylabel('$\\theta_0$ ({}C)'.format(chr(176)))
ax.set_title('{} TS Diagram ($\\theta$-SA), PRES > {}dbar'.format(wmo, dep))

fig.savefig(Path('../figures/{}_ts_abs_diagram_deep.png'.format(wmo)), bbox_inches='tight', dpi=300)
plt.close(fig)

df['SA'] = SA
df['theta'] = theta

pal = cmo.haline

deep_SA = []
time = []
fig, ax = plt.subplots()
for i in df.CYCLE_NUMBER.unique():
    sub = df[df.CYCLE_NUMBER == i]
    ax.plot(sub.SA, sub.theta, '-^', color=pal(i/df.CYCLE_NUMBER.iloc[-1]))

    deep_SA.append(sub.SA.mean())
    time.append(sub.TIME.mean())

ax.set_xlabel('SA')
ax.set_ylabel('$\\theta_0$ ({}C)'.format(chr(176)))
ax.set_title('{} TS Diagram ($\\theta$-SA), PRES > {}dbar'.format(wmo, dep))

rf, rax = plt.subplots()
fake_im = rax.imshow([[]], cmap=pal)
cb = plt.colorbar(fake_im, ax=ax)
cb.set_ticks([])

fig.savefig(Path('../figures/{}_ts_lin_abs_diagram_deep.png'.format(wmo)), bbox_inches='tight', dpi=300)
plt.close(fig)

fig, ax = plt.subplots()
ax.plot(time, deep_SA)
ax.set_title('Float {}'.format(wmo, dep))
ax.set_ylabel('Mean SA (PRES > 1900 dbar)')
for tick in ax.get_xticklabels():
    tick.set_rotation(45)
fig.savefig(Path('../figures/{}_deep_SA.png'.format(wmo)), bbox_inches='tight', dpi=300)
plt.close(fig)
