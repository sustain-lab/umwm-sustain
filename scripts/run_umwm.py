#!/usr/bin/env python3

import f90nml
from netCDF4 import Dataset
import os
import shutil
import subprocess

# TODO umwm must be compiled and executable umwm-run present in path
umwm_path = '/home/milan/sustain/umwm-sustain/umwm-dev'

# path to store finished experiments
output_path = '/home/milan/sustain/umwm-sustain/experiments'

class UMWM():
    def __init__(self, src_path, exp_path):
        self.src_path = src_path
        self.exp_path = exp_path
        self.executable = src_path + '/build/bin/umwm-run'
        self.namelist = exp_path + '/namelists/main.nml'
        os.mkdir(exp_path)
        for dir in ['input', 'output', 'namelists']:
            os.mkdir(exp_path + '/' + dir)
        shutil.copy(src_path + '/namelists/main.nml', self.namelist)

    def build(self):
        pass

    def run(self):
        cwd = os.getcwd()
        os.chdir(self.exp_path)
        subprocess.call(self.executable, shell=True)
        os.chdir(cwd)

    def set_parameters(self, **kwargs):
        nml = f90nml.read(self.namelist)
        for key in kwargs:
            for sublist in nml.keys():
                if key in nml[sublist].keys():
                    nml[sublist][key] = kwargs[key]
        nml.write(self.namelist, force=True)

exp = 1
for wspd in range(5, 65, 5):
    umwm = UMWM(umwm_path, output_path + '/run' + '%2.2i' % exp)
    umwm.set_parameters(wspd0 = wspd)
    umwm.run()
    exp += 1
