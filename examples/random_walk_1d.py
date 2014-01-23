# -*- coding: utf-8 -*-
# Copyright 2012-2013 Pierre de Buyl
# Copyright 2013 Felix Hoëfling
#
# This file is part of pyh5md
#
# pyh5md is free software and is licensed under the modified BSD license (see
# LICENSE file).

import numpy as np
import pyh5md

# Open a H5MD file
f = pyh5md.H5MD_File('walk_1d.h5', 'w', creator='pyh5md examples/jump_process.py', creator_version='0', author='Pierre de Buyl')

# Add a trajectory group
part = f.particles_group('particles')
part.box(dimension=1, boundary=['none'])

# Create the trajectory data
r = np.zeros((30,1), dtype=np.int32)

# Add the trajectory position data element in the trajectory group
part_pos = part.trajectory('position', r.shape, r.dtype)

# Create an observable
obs_com = f.observable('center_of_mass', (), np.float64)

# Run a simulation
step=0
time=0.
for i in range(800):
    step+=1
    time+=.1
    r += -1 + 2*np.random.random_integers(0,1,r.shape)
    # Append the current position data to the H5MD file.
    part_pos.append(r, step, time)
    obs_com.append(r[:,0].mean(), step, time)

# Close the file
f.close()
