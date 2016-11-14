from pic import path

import os
from functools import singledispatch

@singledispatch
def input(args):
    print('type error')

@singledispatch
def output(args):
    print('type error')

@input.register(str)
def _input(args):
    return path.DATA_PATH + args

@output.register(str)
def _output(args):
    return path.PLOT_PATH + args

@input.register(list)
def _input(args):
    return path.DATA_PATH + args[0] + '/' + args[0] + '%06d' % args[1] + '_r' + '%02d' % args[2]

@output.register(list)
def _output(args):
    if(not os.path.exists(path.PLOT_PATH + args[0] + '/')): os.mkdir(path.PLOT_PATH + args[0] + '/')
    return path.PLOT_PATH + args[0] + '/' + args[0] + '%06d' % args[1]
