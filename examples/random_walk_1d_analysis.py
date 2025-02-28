# -*- coding: utf-8 -*-
# Copyright 2012, 2013, 2016, 2025 Pierre de Buyl
# Copyright 2013 Felix Hoëfling
#
# This file is part of pyh5md
#
# pyh5md is free software and is licensed under the modified BSD license (see
# LICENSE file).

import numpy as np
import matplotlib.pyplot as plt
from pyh5md import File, element

# Open a H5MD file
f = File('walk_1d.h5', 'r')

# Open a trajectory group
part = f.particles_group('particles')

# Open trajectory position data element in the trajectory group
part_pos = element(part, 'position')

# Get data and time
r = part_pos.value
r_time = part_pos.time

# Compute the time-averaged mean-square displacement,
# drop large correlation times due to insufficient statistics
T = r.shape[0]
msd = np.empty((T//4, r.shape[1]))
time = r_time[:T//4]
for n in range(T//4):
    # the sum over "axis=2" is over the spatial components of the positions
    msd[n] = np.mean(np.sum(pow(r[n:] - r[:T-n], 2), axis=2), axis=0)

# Compute mean and standard error of mean (particle- and component-wise)
msd_mean = msd.mean(axis=1)
msd_err = msd.std(axis=1) / np.sqrt(msd.shape[1] - 1)

# Display the MSD and its standard error
plt.plot(time, msd_mean, 'k-', label=r'$\langle [{\bf r}(t)-{\bf r}(0)]^2\rangle$')
plt.plot(time, msd_mean+msd_err, 'k:', label=r'$\langle [{\bf r}(t)-{\bf r}(0)]^2\rangle \pm \sigma$')
plt.plot(time, msd_mean-msd_err, 'k:')
# display reference line for long-time diffusion with D = <a^2> / (2 d <\tau>),
# here: <a^2> = 1, <\tau> = 0.1, and d=1
plt.plot(time, 2 * (.5 * 1 / 0.1 / 1) * time, 'k--', label=r'$2 D t$')
plt.xlabel(r'$t$')
plt.ylabel(r'$MSD(t)$')
plt.xscale('log')
plt.yscale('log')
plt.legend(loc='upper left')

# Create a new figure
plt.figure()

# Obtain and plot the center_of_mass observable
f.observables = f.require_group('observables')
obs_com = element(f.observables, 'center_of_mass')
plt.plot(obs_com.time[:], obs_com.value[:], 'k-')
plt.xlabel(r'$t$')
plt.ylabel(r'center of mass')

# Close the file
f.close()

plt.show()
