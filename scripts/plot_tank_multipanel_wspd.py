#!/usr/bin/env python3

import matplotlib
matplotlib.use('Agg')

import matplotlib.pyplot as plt
from datetime import datetime, timedelta
import f90nml
from netCDF4 import Dataset
import os
import shutil
import subprocess

# path to store finished experiments
path = '/home/milan/Work/sustain/umwm-sustain/experiments/tank'
time = datetime(2018, 1, 1, 0, 1, 0)

wspd = range(5, 65, 5)

def get_wave_fields(path):
    run_dict = {w: 'run' + '%2.2i' % (wspd.index(w) + 1) for w in wspd}
    Hs = []
    Tm = []
    Tp = []
    wa = []
    ustar = []
    Cd = []
    for w in wspd:
        umwmout = path + '/' + run_dict[w] + '/output/umwmout_'\
                + time.strftime('%Y-%m-%d_%H:%M:%S') + '.nc'
        with Dataset(umwmout, 'r') as nc:
            Hs.append(nc.variables['swh'][0,4,23])
            Tm.append(nc.variables['mwp'][0,4,23])
            Tp.append(nc.variables['dwp'][0,4,23])
            wa.append(nc.variables['dcp'][0,4,23] / nc.variables['wspd'][0,4,23])
            ustar.append(nc.variables['ust'][0,4,23])
            Cd.append(nc.variables['cd'][0,4,23])
    return Hs, Tm, Tp, wa, ustar, Cd

Hs, Tm, Tp, wa, ustar, Cd = get_wave_fields(path)

fig = plt.figure(figsize=(12, 8))

axes = []
for col in range(2):
    for row in range(3):
        axes.append(plt.subplot2grid((3, 2), (row, col)))

ax1, ax2, ax3, ax4, ax5, ax6 = axes

ax1.plot(wspd, Hs, 'k-', lw=1, marker='.', ms=8)
ax2.plot(wspd, Tm, 'k-', lw=1, marker='.', ms=8)
ax3.plot(wspd, Tp, 'k-', lw=1, marker='.', ms=8)
ax4.plot(wspd, wa, 'k-', lw=1, marker='.', ms=8)
ax5.plot(wspd, ustar, 'k-', lw=1, marker='.', ms=8)
ax6.plot(wspd, Cd, 'k-', lw=1, marker='.', ms=8)

ax1.set_ylabel('Sig. wave height [m]')
ax2.set_ylabel('Mean period [s]')
ax3.set_ylabel('Peak period [s]')
ax4.set_ylabel('Wave age')
ax5.set_ylabel('Friction velocity [m/s]')
ax6.set_ylabel('Drag coefficient')

ax1.set_ylim(0, 0.3)
ax2.set_ylim(0, 1.2)
ax3.set_ylim(0, 1.8)
ax4.set_ylim(0, 0.12)
ax5.set_ylim(0, 2.5)
ax6.set_ylim(0, 0.003)

for ax in axes:
    ax.grid()
    ax.set_xlim(0, 60)

for ax in [ax3, ax6]:
    ax.set_xlabel('Wind speed [m/s]')

fig.suptitle('SUSTAIN wave simulations -- wind speed dependent')
plt.savefig('sustain_multipanel_wspd.png', dpi=100)
plt.close(fig)
