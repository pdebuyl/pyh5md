# Copyright 2012 Pierre de Buyl
#
# This file is part of pyh5md
#
# pyh5md is free software and is licensed under the modified BSD license (see
# LICENSE file).

import numpy as np
import pyh5md

# Open a H5MD file
f = pyh5md.H5MD_File('poc.h5', 'w', creator='pyh5md examples/jump_process.py', creator_version='0', author='Pierre de Buyl')

# Add a trajectory group
part = f.trajectory_group('particles')

# Create the trajectory data
r = np.zeros((10,1), dtype=np.int32)

# Add the trajectory position data element in the trajectory group
part_pos = part.trajectory('position', r.shape, r.dtype)

# Create an observable
obs_sin = f.observable('sin', (1,), np.float64)

# Run a simulation
step=0
time=0.
for i in range(100):
    step+=1
    time+=.1
    r += np.random.random_integers(-1,1,r.shape)
    # Append the current position data to the H5MD file.
    part_pos.append(r, step, time)
    obs_sin.append(np.sin(time), step, time)

# Close the file
f.f.close()
