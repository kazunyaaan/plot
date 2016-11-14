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

PROC = 1

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
    parser.add_argument('-s', '--species', type=str, required=True)
    parser.add_argument('-t', '--times', type=int, required=True)
    
    # 任意
    parser.add_argument('-cmax', type=int)
    parser.add_argument('-cmin', type=int)
    parser.add_argument('--version', action='version', version='%(prog)s 2.0')
    
    return parser.parse_args()
    
def load(prefix, ts, pid):
    for n in range(profile.SIZE):
        #print(file.input([prefix, ts, n]))
        d = np.loadtxt(file.input([prefix, ts, n]), delimiter="\t")
        if (d.size > 0):
            d = d.reshape(d.size//7, 7)

            if (d == pid).any():
                pid_ = np.where(d == pid)
                d[pid_[0], 1] = d[pid_[0], 1] - 2.0 + n * profile.LZ0
                return np.c_[d[pid_[0], 1:4][0]]

def save(file_path, fig):
    fig.savefig(file_path, bbox_inches='tight', transparent=True)


def plot(ts):
    global m1, m2, p1, p2, n1

    fig = plt.figure()

    ax1 = fig.add_subplot(121)
    ax2 = fig.add_subplot(122)

    p1 = np.hstack((p1, load(species, ts, 110051503)))
    p2 = np.hstack((p2, load(species, ts, 77255503)))
    m1 = np.hstack((m1, load(species, ts, 108405403)))
    m2 = np.hstack((m2, load(species, ts, 70137108)))
    n1 = np.hstack((n1, load(species, ts, 50848704)))

    #if (p1.shape[1] > times):
    #    p1 = np.delete(p1, 0, 1)
    #    p2 = np.delete(p2, 0, 1)
    #    m1 = np.delete(m1, 0, 1)
    #    m2 = np.delete(m2, 0, 1)
    #    n1 = np.delete(n1, 0, 1)

    w = 200

    imin = profile.LX/2-w
    imax = profile.LX/2+w
    jmin = profile.LY/2-w
    jmax = profile.LY/2+w

    a = 0.2

    aplot

    ax1.plot(p1[2], p1[0], ".", label='P1', color='red', alpha=1.00)
    ax1.plot(m1[2], m1[0], ".", label='M1', color='blue', alpha=1.00)

    #ax.plot(X, Y, k + .1*d[k, :, :], zdir='z', levels=k + .1*levels, alpha=.2)
    ax.plot(p1[2], p1[1], p1[0], label='P1', color='red', alpha=1.00)
    ax.plot(p2[2], p2[1], p2[0], label='P2', color='red', alpha=1.00)
    ax.plot(m1[2], m1[1], m1[0], label='M1', color='blue', alpha=1.00)
    ax.plot(m2[2], m2[1], m2[0], label='M2', color='blue', alpha=1.00)
    ax.plot(n1[2], n1[1], n1[0], label='N1', color='green', alpha=1.00)

    cset = ax.plot(p1[2], p1[1], 0, zdir='z', color='red', alpha=a)
    cset = ax.plot(p2[2], p2[1], 0, zdir='z', color='red', alpha=a)
    cset = ax.plot(m1[2], m1[1], 0, zdir='z', color='blue', alpha=a)
    cset = ax.plot(m2[2], m2[1], 0, zdir='z', color='blue', alpha=a)
    cset = ax.plot(n1[2], n1[1], 0, zdir='z', color='green', alpha=a)
    
    cset = ax.plot(p1[1], p1[0], imin, zdir='x', color='red', alpha=a)
    cset = ax.plot(p2[1], p2[0], imin, zdir='x', color='red', alpha=a)
    cset = ax.plot(m1[1], m1[0], imin, zdir='x', color='blue', alpha=a)
    cset = ax.plot(m2[1], m2[0], imin, zdir='x', color='blue', alpha=a)
    cset = ax.plot(n1[1], n1[0], imin, zdir='x', color='green', alpha=a)

    cset = ax.plot(p1[2], p1[0], jmax, zdir='y', color='red', alpha=a)
    cset = ax.plot(p2[2], p2[0], jmax, zdir='y', color='red', alpha=a)
    cset = ax.plot(m1[2], m1[0], jmax, zdir='y', color='blue', alpha=a)
    cset = ax.plot(m2[2], m2[0], jmax, zdir='y', color='blue', alpha=a)
    cset = ax.plot(n1[2], n1[0], jmax, zdir='y', color='green', alpha=a)

    ax.legend()

    ax.set_xlim3d(imin, imax)
    ax.set_ylim3d(jmin, jmax)
    ax.set_zlim3d(0, profile.LZ0*profile.SIZE)


    save(file.output([species, ts]), fig)
    plt.clf()
    
def main():
    global species, times, m1, m2, p1, p2, n1
    args = parse()
    species = args.species
    times = args.times

    p1 = load(species, 0, 110051503)
    p2 = load(species, 0, 77255503)
    m1 = load(species, 0, 108405403)
    m2 = load(species, 0, 70137108)
    n1 = load(species, 0, 50848704)



    
    
    for ts in range(0, profile.TIMESTEP_MAX+1, 1):
        print(ts)
        plot(ts)

if __name__ == '__main__':
    main()

