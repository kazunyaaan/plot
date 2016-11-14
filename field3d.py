#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
import argparse
import numpy as np
from multiprocessing import Pool
from pic import path, profile, file, omake

## CUI
import matplotlib
matplotlib.use('Agg')
from mpl_toolkits.mplot3d import Axes3D
import matplotlib.pyplot as plt

## path
#path.DATA_PATH = '../data/'
#path.PLOT_PATH = './'
#profile.reload()

PROC = 10

ORIGIN = 'lower'
INTERPOLATION = 'spline36'
C_MAX = 0.01
C_MIN = -C_MAX
C_MAP = omake.generate_cmap(['blue', '#222222', 'red'])
#cm = plt.cm.seismic

x = range(0, profile.LX, 1)
y = range(0, profile.LY, 1)

X, Y = np.meshgrid(x, y)
levels = np.linspace(0.1, 1.5, 100)

def parse():
    parser = argparse.ArgumentParser(
            description='fieldデータから2dのカラーコンタをつくるやーつ'
            )
    # 必須
    parser.add_argument('-f', '--field', type=str, required=True)
    parser.add_argument('-i', '--index', type=str, required=True)
    
    # 任意
    parser.add_argument('-cmax', type=int)
    parser.add_argument('-cmin', type=int)
    parser.add_argument('--version', action='version', version='%(prog)s 2.0')
    
    return parser.parse_args()
    
def load(prefix, ts):
    d = np.zeros((profile.LZ0*profile.SIZE, profile.LY, profile.LX))
    for n in range(profile.SIZE):
        d[profile.LZ0*n:profile.LZ0*(n+1), :, :] = np.fromfile(file.input([prefix, ts, n]), np.float64).reshape(profile.LZ, profile.LY, profile.LX, 3)[2:2+profile.LZ0, :, :, index]

    #print(d.shape)

    #print(np.min(d))
    #print(np.max(d))
    
    return d

def save(file_path, fig):
    fig.savefig(file_path, bbox_inches='tight', transparent=True)
    #plt.savefig(file_path), bbox_inches='tight', transparent=True)


def plot(ts):
    fig = plt.figure()
    ax = fig.gca(projection='3d')

    d = load(prefix, ts)
    
    levels = np.linspace(0.3, 1.5, 100)

    for k in range(profile.LZ0*profile.SIZE):
        ax.contourf(X, Y, k + .1*d[k, :, :], zdir='z', levels=k + .1*levels, alpha=.2)

    ax.legend()

    ax.set_xlim3d(profile.LX0/2-80, profile.LX0/2+80)
    ax.set_ylim3d(profile.LY0/2-80, profile.LY0/2+80)

    save(file.output([prefix, ts]), fig)
    plt.clf()
    
def loop(p):
    for ts in range(500 + profile.TIMESTEP_STEP*p, profile.TIMESTEP_MAX+1, profile.TIMESTEP_STEP*PROC):
        plot(ts)
        print(ts)

def main():
    global prefix, index
    args = parse()
    prefix = args.field;
    if args.index == 'x':
        index = 2
    elif args.index == 'y':
        index = 1
    elif args.index == 'z':
        index = 0

    p = Pool(PROC)
    p.map(loop, range(PROC))

if __name__ == '__main__':
    main()

