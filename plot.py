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

def setup_data(path):
    return np.loadtxt(path, delimiter=' \t ')[:, 1:]

def file_in(prefix, ts):
    return FILE_I_PATH + prefix + '/' + prefix + '%06d' % ts + '_r01.txt'

def file_out(prefix, ts):
    if(not os.path.exists(FILE_O_PATH + prefix + '/')): os.mkdir(FILE_O_PATH + prefix + '/')
    return FILE_O_PATH + prefix + '/' + prefix + '%06d' % ts + '.png'

def generate_cmap(colors):
    values = range(len(colors))

    vmax = np.ceil(np.max(values))
    color_list = []
    for v, c in zip(values, colors):
        color_list.append( ( v/ vmax, c) )
    return LinearSegmentedColormap.from_list('custom_cmap', color_list)

def main():
    argvs = sys.argv
    argc = len(argvs)

    if (argc != 3): quit()

    prefix = argvs[1]
    index  = int(argvs[2])
    
    for ts in range(0, TIMESTEP_MAX + 1, TIMESTEP_STEP):
        print(str(ts) + ' ' + file_in(prefix, ts) + ' index : ' + str(index))

        v = setup_data(file_in(prefix, ts), index)
        
        vmax = 0.08#np.max(v)
        vmin = -vmax

        cm = plt.cm.seismic
        cm = generate_cmap(['blue', '#222222', 'red'])

        plt.imshow(v, origin = ORIGIN, interpolation = INTERPOLATION,
            cmap = cm, vmin = vmin, vmax = vmax)
        plt.colorbar()

        plt.savefig(file_out(prefix, ts), bbox_inches='tight', transparent=True)

        plt.clf()
    
if __name__ == '__main__':
    main()
