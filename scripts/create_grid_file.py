#!/usr/bin/env python

from netCDF4 import Dataset
import numpy as np

def create_grid_file(x, y, z):
    with Dataset('umwm.gridtopo.nc', 'w', format='NETCDF4') as nc:
        jm, im = x.shape
        nc.createDimension('x', size=im)
        nc.createDimension('y', size=jm)
        nc.createVariable('x', datatype='f4', dimensions=('y', 'x'))[:] = x[:]
        nc.createVariable('y', datatype='f4', dimensions=('y', 'x'))[:] = y[:]
        nc.createVariable('z', datatype='f4', dimensions=('y', 'x'))[:] = z[:]


dx = dy = 1

# tank parameters
length = 23
width = 6
depth = 0.72
# TODO parabolic beach

x = np.arange(0, length + 2 * dx, dx)
y = np.arange(0, width + 2 * dy, dy)
x, y = np.meshgrid(x, y)
z = depth * np.ones(x.shape)

create_grid_file(x, y, z)
