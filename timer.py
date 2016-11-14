#!/usr/bin/env python
# -*- coding: utf-8 -*-

import sys
import os
import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from matplotlib.colors import LinearSegmentedColormap

import pic

FILE_I_PATH = '../data/'
FILE_O_PATH = './'

p = pic.load_profile('../data/profile.json')

ENABLED_MPI = p['MPI']['enabled']
MPI_SIZE    = int(p['MPI']['size'])

TIMESTEP_MAX  = int(p['PIC']['timestep']['max'])
TIMESTEP_STEP = int(p['PIC']['timestep']['step'])
#TIMESTEP_STEP = 10

LX0 = int(p['PIC']['LY0']) + 5
LY0 = int(p['PIC']['LZ0']) + 5

ORIGIN = 'lower'
INTERPOLATION = 'spline36'
#interpolation = 'None'
#interpolation = 'bicubic'

def setup_data(path, index):
    d = np.loadtxt(path, delimiter='\t').reshape(TIMESTEP_MAX+1, 4)[:,index]
    #print(np.loadtxt(path, delimiter=' \t ').reshape(4, TIMESTEP_MAX+1)[1:,:].shape)
    return d
def file_in(prefix):
    return FILE_I_PATH + prefix + '.txt'

def file_out(prefix):
    if(not os.path.exists(FILE_O_PATH + 'energy/')): os.mkdir(FILE_O_PATH + 'energy/')
    return FILE_O_PATH + prefix + '.png'

def main():

    x = np.array([i for i in range(TIMESTEP_MAX + 1)])
    time = setup_data(file_in('timer'), 1)
    
    #t0 = eles[0] + ions[0] + f_b[0] + f_e[0]

    plt.fill_between(x, 0, time, facecolor='cyan', alpha=0.5)

    plt.savefig(file_out('timer'), bbox_inches='tight', transparent=True)

    plt.clf()
    
if __name__ == '__main__':
    main()
