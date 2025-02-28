# -*- coding: utf-8 -*-
# Copyright 2012, 2013, 2016, 2025 Pierre de Buyl
# Copyright 2013 Felix Hoëfling
#
# This file is part of pyh5md
#
# pyh5md is free software and is licensed under the modified BSD license (see
# LICENSE file).

import numpy as np
from pyh5md import File, element

# Open a H5MD file
f = File('walk_1d.h5', 'w', creator='pyh5md examples/jump_process.py', creator_version='0', author='Pierre de Buyl')

# Add a trajectory group
part = f.particles_group('particles')
part.create_box(dimension=1, boundary=['none'])

# Create the trajectory data
r = np.zeros((30,1), dtype=np.int32)

# Add the trajectory position data element in the trajectory group
part_pos = element(part, 'position', store='time', shape=r.shape, dtype=r.dtype, time=True)

# Create an observable
f.observables = f.require_group('observables')
obs_com = element(f.observables, 'center_of_mass', shape=(), dtype=np.float64, store='time', time=True)

# Run a simulation
step=0
time=0.
for i in range(800):
    step+=1
    time+=.1
    r += -1 + 2*np.random.randint(0,2,r.shape)
    # Append the current position data to the H5MD file.
    part_pos.append(r, step, time)
    obs_com.append(r[:,0].mean(), step, time)

# Close the file
f.close()
