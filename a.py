#!/usr/bin/env python
# -*- coding: utf-8 -*-

import sys
import os
import pic

INPUT_PATH = '../data/'
OUTPUT_PATH = './'

p = pic.load_profile('../data/profile.json')

ENABLED_MPI = p['MPI']['enabled']
INPUT_PATH = '../data/'
OUTPUT_PATH = '../'

origin = 'lower'
#origin = 'upper'

def main():
    print(ENABLED_MPI)

if __name__ == '__main__':
    main()

