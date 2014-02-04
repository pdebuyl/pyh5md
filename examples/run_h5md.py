# Copyright 2012-2013 Pierre de Buyl
#
# This file is part of pyh5md
#
# pyh5md is free software and is licensed under the modified BSD license (see
# LICENSE file).

import numpy as np
import pyh5md
from pyh5md.topology import get_bond_list, TopologyGroup

f = pyh5md.H5MD_File('particles_3d.h5', 'w', creator='run_h5md', creator_version='0', author='Pierre de Buyl')

# Creating atom group
at = f.particles_group('atoms')

# Creating position data
r = np.zeros((100,3), dtype=np.float64)
at_pos = at.trajectory('position', r.shape, r.dtype)

tg = TopologyGroup(f.f, 'atoms')
bl = tg.bond_list('loose', time=True)

# Creating species
s = np.ones(r.shape[:1])
at_s = at.trajectory('species', data=s, time=False)

# Creating velocity data
v = np.zeros((100,3), dtype=np.float64)
at_v = at.trajectory('velocity', v.shape, v.dtype)

# Create an observable
obs_com = f.observable('center_of_mass', r.shape[-1:], r.dtype)
# Create a scalar time independent observable
obs_fixed = f.observable('random_number', data=np.random.random(), time=False)

edges = (1.,)
box = at.box(dimension=1, boundary=['none'], edges=edges, time=True)

bonds = [ (0, 1), (1, 2), (2, 3) ]

DT = 0.1
time = 0.
for t in xrange(201):
    if t%10==0:
        at_pos.append(r, t, time)
        bl.append(np.array(bonds).reshape((-1,)), t, time)
        at_v.append(v, t, time)
        obs_com.append(r.mean(axis=0), t, time)
    r += DT*0.5*v
    v += DT*np.random.normal(0., 1., v.shape)
    r += DT*0.5*v
    time += DT
    box.edges.append(edges, t, time)
    if t==100:
        bonds += [(4, 5), (5, 6), (6, 7)]

f.close()
