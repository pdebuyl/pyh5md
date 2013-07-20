# Copyright 2012-2013 Pierre de Buyl
#
# This file is part of pyh5md
#
# pyh5md is free software and is licensed under the modified BSD license (see
# LICENSE file).

import numpy as np
import matplotlib.pyplot as plt
import pyh5md

# Open a H5MD file
f = pyh5md.H5MD_File('walk_1d.h5', 'r')
f.check()

# Open a trajectory group
part = f.trajectory_group('particles')

# Open trajectory position data element in the trajectory group
part_pos = part.trajectory('position')

# Get data and time
r = part_pos.value
r_time = part_pos.time

# Compute the MSD
# The sum over "axis=2" is over the spatial components of the positions
msd = ((r - r[0])**2).sum(axis=2)

# Compute the mean and standard deviation (particle-wise)
msd_mean = msd.mean(axis=1)
msd_std = msd.std(axis=1)

# Display the MSD and 
plt.plot(r_time, msd_mean, 'k-', label=r'$\langle [{\bf r}(t)-{\bf r}(0)]^2\rangle$')
plt.plot(r_time, msd_mean+msd_std, 'k:', label=r'$\langle [{\bf r}(t)-{\bf r}(0)]^2\rangle \pm \sigma$')
plt.plot(r_time, msd_mean-msd_std, 'k:')
plt.xlabel(r'$t$')
plt.xlabel(r'$t$')
plt.legend()

# Create a new figure
plt.figure()

# Obtain and plot the center_of_mass observable
obs_com = f.observable('center_of_mass')
plt.plot(obs_com.time, obs_com.value, 'k-')
plt.xlabel(r'$t$')
plt.ylabel(r'center of mass')

# Close the file
f.close()

plt.show()
