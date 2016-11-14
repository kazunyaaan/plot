import json
from pic import path

def reload():
    load()

def load():
    p = _load(path.DATA_PATH + 'profile.json')
    _setup(p)

def _setup(p):
    global DELT, DELX
    DELT = 1;
    DELX = 1;

    global C
    C = float(p['PIC']['C'])

    global NUM_DENS
    NUM_DENS = int(p['PIC']['density'])

    global SIZE
    SIZE = int(p['MPI']['size'])

    global LX0, LY0, LZ0
    LX0 = int(p['PIC']['LZ0'])
    LY0 = int(p['PIC']['LY0'])
    LZ0 = int(p['PIC']['LX0'])

    global LX, LY, LZ
    LX = int(p['PIC']['LZ'])
    LY = int(p['PIC']['LY'])
    LZ = int(p['PIC']['LX'])

    global TIMESTEP_MAX, TIMESTEP_STEP
    TIMESTEP_MAX = int(p['PIC']['timestep']['max'])
    TIMESTEP_STEP = int(p['PIC']['timestep']['step'])

    if ('PML' in p['PIC']):
        global L, M, R0, SIGMA_MAX
        L = int(p['PIC']['PML']['L'])
        M = int(p['PIC']['PML']['M'])
        R0 = float(p['PIC']['PML']['R0'])
        SIGMA_MAX = float(p['PIC']['PML']['SIGMA_MAX'])

    global SHAPE_FACTOR
    SHAPE_FACTOR = int(p['PIC']['shapefactor'])

def _load(path):
    f = open(path)
    p = json.load(f)
    f.close()
    return p

def main():
    print(L)

load()
    
if __name__ == '__main__':
    main()
