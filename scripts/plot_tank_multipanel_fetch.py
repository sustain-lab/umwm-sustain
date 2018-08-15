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

def get_wave_fields(umwmout):
    with Dataset(umwmout, 'r') as nc:
        Hs = nc.variables['swh'][0,4,:]
        Tm = nc.variables['mwp'][0,4,:]
        Tp = nc.variables['dwp'][0,4,:]
        wa = nc.variables['dcp'][0,4,:] / nc.variables['wspd'][0,4,:]
        ustar = nc.variables['ust'][0,4,:]
        Cd = nc.variables['cd'][0,4,:]
    return Hs, Tm, Tp, wa, ustar, Cd

fig = plt.figure(figsize=(12, 8))

axes = []
for col in range(2):
    for row in range(3):
        axes.append(plt.subplot2grid((3, 2), (row, col)))

ax1, ax2, ax3, ax4, ax5, ax6 = axes

run_dict = {w: 'run' + '%2.2i' % wspd.index(w) for w in wspd}
colors_dict = {10: 'k', 20: 'b', 30: 'g', 40: 'y', 50: 'r', 60: 'm'}

for w in range(10, 70, 10):
    umwmout = path + '/' + run_dict[w] + '/output/umwmout_'\
            + time.strftime('%Y-%m-%d_%H:%M:%S') + '.nc'
    Hs, Tm, Tp, wa, ustar, Cd = get_wave_fields(umwmout)

    color = colors_dict[w]

    ax1.plot(Hs, color + '-', lw=1, label='%2i' % w + ' m/s')
    ax2.plot(Tm, color + '-', lw=1)
    ax3.plot(Tp, color + '-', lw=1)
    ax4.plot(wa, color + '-', lw=1)
    ax5.plot(ustar, color + '-', lw=1)
    ax6.plot(Cd, color + '-', lw=1)

ax1.legend(loc='upper left', fancybox=True, shadow=True, ncol=3, prop={'size': 8})

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
    ax.set_xlim(0, 23)

for ax in [ax3, ax6]:
    ax.set_xlabel('Fetch [m]')

fig.suptitle('SUSTAIN wave simulations -- fetch limited')
plt.savefig('sustain_multipanel.png', dpi=100)
plt.close(fig)
