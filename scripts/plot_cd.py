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
output_path = '/home/milan/Work/sustain/umwm-sustain/experiments'

field_path = output_path + '/field'
tank_path = output_path + '/tank'

field_time = datetime(2012, 1, 1, 6, 0, 0)
tank_time = datetime(2018, 1, 1, 0, 1, 0)

wspd = range(5, 65, 5)

cd_field = []
for n in range(1, len(wspd) + 1):
    umwmout = tank_path + '/run' + '%2.2i' % n + '/output/umwmout_' + tank_time.strftime('%Y-%m-%d_%H:%M:%S') + '.nc'
    with Dataset(umwmout, 'r') as nc:
        cd_field.append(nc.variables['cd'][0,5,19])

cd_tank = []
for n in range(1, len(wspd) + 1):
    umwmout = tank_path + '/run' + '%2.2i' % n + '/output/umwmout_' + tank_time.strftime('%Y-%m-%d_%H:%M:%S') + '.nc'
    with Dataset(umwmout, 'r') as nc:
        cd_tank.append(nc.variables['cd'][0,4,23])

fig = plt.figure(figsize=(8, 6))
ax = fig.add_subplot(111, xlim=(0, 60), ylim=(0, 3e-3))
plt.plot(wspd, cd_field, 'b-', lw=2, label='Field, 200 km fetch')
plt.plot(wspd, cd_field, 'b.', ms=12)
plt.plot(wspd, cd_tank, 'r-' , lw=2, label='Tank, 20 m fetch')
plt.plot(wspd, cd_tank, 'r.', ms=12)
plt.legend(loc='upper left', fancybox=True, shadow=True)
plt.grid()
plt.xlabel('Wind speed [m/s]')
plt.ylabel('Drag coefficient')
plt.savefig('cd.png', dpi=100)
plt.close(fig)
