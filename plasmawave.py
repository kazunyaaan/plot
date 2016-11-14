#!/usr/bin/env python
# -*- coding: utf-8 -*-

import sys
import os
import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from matplotlib.colors import LinearSegmentedColormap
from scipy import fftpack

import pic

FILE_I_PATH = '../data/'
FILE_O_PATH = './'

p = pic.load_profile('../data/profile.json')

#MPI_SIZE    = int(p['MPI']['size'])

TIMESTEP_MAX  = int(p['PIC']['timestep']['max'])
TIMESTEP_STEP = int(p['PIC']['timestep']['step'])
#TIMESTEP_STEP = 10

LX0 = int(p['PIC']['LZ0']) + 5
LY0 = int(p['PIC']['LY0']) + 5
LZ0 = int(p['PIC']['LX0']) + 5

ORIGIN = 'lower'
INTERPOLATION = 'spline36'
#interpolation = 'None'
#interpolation = 'bicubic'

def setup_data(path):
    v = np.fromfile(path, np.float64).reshape(LZ0, LY0, LX0, 3)[2:LZ0-3, 2:LY0-3, 2:LX0-3, 2]
    v = np.sum(v, axis = 0)
    v = np.sum(v, axis = 0)
    
    print(v.shape)
    return v

def file_in(prefix, ts):
    return FILE_I_PATH + prefix + '/' + prefix + '%06d' % ts + '_r00'

def file_out(prefix, ts):
    if(not os.path.exists(FILE_O_PATH + 'wave/')): os.mkdir(FILE_O_PATH + 'wave/')
    return FILE_O_PATH + 'wave/' + prefix + '_wave.png'

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

    if (argc != 2): quit()

    prefix = argvs[1]

    d = []
    
    for ts in range(0, TIMESTEP_MAX + 1, TIMESTEP_STEP):
        d.append(setup_data(file_in(prefix, ts)))

    d = np.array(d);
    ft = fftpack.fftshift(np.abs(fftpack.fft2(d)))
    ft = np.log10(ft**2)[TIMESTEP_MAX/2:TIMESTEP_MAX, (LX0-5)/2:(LX0-5)]
    #ft = ft[int(TIMESTEP_MAX/2):TIMESTEP_MAX, int((LX0-5)/2):LX0-5]
    print(ft.shape)

    #plt.yscale('log')

    cm = plt.cm.jet
    #cm = generate_cmap(['blue', '#222222', 'red'])

    #plt.pcolor(X, Y, ft, cmap = cm)
    plt.imshow(ft, origin = ORIGIN, interpolation = INTERPOLATION, cmap = cm, aspect='auto')

    #plt.xticks(np.arange(0,LX0 - int(LX0/2),25/np.pi), np.arange(0,(LX0 - int(LX0/2))*(2*np.pi/50),25/np.pi*(2*np.pi/50)))

    #plt.yticks(np.arange(0,TIMESTEP_MAX - int(TIMESTEP_MAX/2),100), np.arange(0,(TIMESTEP_MAX - int(TIMESTEP_MAX/2))*0.05,100*0.05))
    plt.colorbar()

    print(file_out(prefix, ts))
    plt.savefig(file_out(prefix, ts), bbox_inches='tight', transparent=True)

    plt.clf()
    
if __name__ == '__main__':
    main()
