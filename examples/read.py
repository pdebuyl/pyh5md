#!/usr/bin/env python
"""
Open a H5MD file and displays the elements in the given particles group
"""
from __future__ import print_function, division

import argparse

parser = argparse.ArgumentParser(description=__doc__)
parser.add_argument('file', type=str, help='H5MD file')
parser.add_argument('--group', type=str, help='name of the particles group')
args = parser.parse_args()

import numpy as np
from pyh5md import File, element

with File(args.file, 'r') as f:
    if args.group is None:
        print('Particles groups in this file:', *list(f['particles'].keys()))
        import sys
        sys.exit()
    assert args.group in f['particles'], "group not found in particles group"
    all_particles = f.particles_group(args.group)

    for loc, name in (
        (f['observables'], 'v'),
        (all_particles, 'mass'),
        (all_particles['box'], 'edges'),
        (all_particles, 'id'),
        (all_particles, 'position'),
        (all_particles, 'force'),
        (all_particles, 'velocity'),
    ):
        if name not in loc:
            continue
        el = element(loc, name)
        print('---------------------------------------------------------------')
        print('%-10s ----------------------------------------------------' % name)
        print(el.element_type)
        print("shape   :", el.value.shape)
        print("step    :", el.step, el.step_offset)
        print("time    :", el.time, el.time_offset)
        print("value   :", el.value)
