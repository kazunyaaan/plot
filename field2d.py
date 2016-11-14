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

import matplotlib.pyplot as plt

## path
#path.DATA_PATH = '../data/'
#path.PLOT_PATH = './'
#profile.reload()

PROC = 2

ORIGIN = 'lower'
INTERPOLATION = 'spline36'
C_MAX = 0.01
C_MIN = -C_MAX
#C_MAP = omake.generate_cmap(['blue', '#222222', 'red'])
C_MAP = plt.cm.seismic

def parse():
    parser = argparse.ArgumentParser(
            description='fieldデータから2dのカラーコンタをつくるやーつ'
            )
    # 必須
    parser.add_argument('-f', '--field', type=str, required=True)
    parser.add_argument('-i', '--index', type=str, required=True)
    parser.add_argument('-z', type=int, required=True)
    
    # 任意
    parser.add_argument('-cmax', type=int)
    parser.add_argument('-cmin', type=int)
    parser.add_argument('--version', action='version', version='%(prog)s 2.0')
    
    return parser.parse_args()
    
def load(file_path):
    return np.fromfile(file_path, np.float64).reshape(profile.LZ, profile.LY, profile.LX, 3)[k, profile.LY//2-80:profile.LY//2+80, profile.LX//2-80:profile.LX//2+80, index]

def save(file_path, fig):
    fig.savefig(file_path, bbox_inches='tight', transparent=True)
    #plt.savefig(file_path), bbox_inches='tight', transparent=True)


def plot(ts):
    d = load(file.input([prefix, ts, rank]))
    #print(np.max(d))
    fig = plt.figure()
    
    plt.imshow(d, origin=ORIGIN, interpolation=INTERPOLATION, cmap=C_MAP, vmin=C_MAX, vmax=C_MIN)
    plt.colorbar()

    save(file.output(['2d_'+prefix, ts, rank]), fig)
    plt.clf()
    
def loop(p):
    for ts in range(profile.TIMESTEP_STEP*p, profile.TIMESTEP_MAX+1, profile.TIMESTEP_STEP*PROC):
        print(file.input([prefix, ts, rank]))
        plot(ts)

def main():
    global prefix, index, k, rank
    args = parse()
    prefix = args.field;
    if args.index == 'x':
        index = 2
    elif args.index == 'y':
        index = 1
    elif args.index == 'z':
        index = 0
    rank = args.z // profile.LZ0;
    k = 2 + args.z % profile.LZ0;

    if (rank >= profile.SIZE):
        quit()

    p = Pool(PROC)
    p.map(loop, range(PROC))

if __name__ == '__main__':
    main()

