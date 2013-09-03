# -*- coding: utf-8 -*-
# Copyright 2012-2013 Pierre de Buyl
#
# This file is part of pyh5md
#
# pyh5md is free software and is licensed under the modified BSD license (see
# LICENSE file).

import numpy as np
import pyh5md

N=3
NX=32
NY=32

# Open a H5MD file
f = pyh5md.H5MD_File('walk_2d.h5', 'w', creator='pyh5md examples/random_walk_open_2d.py', creator_version='0', author='Pierre de Buyl')

# Add a trajectory group
part = f.particles_group('tracers')
offset = np.array( [0, 0] )
edges = np.array( [NX, NY] )
part.set_box(d=2, boundary=['none', 'none'], edges = edges, offset=offset)

# Create the trajectory data
r = np.zeros((N,2), dtype=np.int32)
r[:,:] = 16
idid = np.arange(N)

# Add the trajectory position data element in the trajectory group
part_pos = part.trajectory('position', r.shape, r.dtype, chunks=(10,N,2), N_fixed=False)
part_id = part.trajectory('id', idid.shape, idid.dtype, chunks=(10,N), N_fixed=False)

# Available slots for particle data
slots = []
max_id = idid.max()

# Run a simulation
step=0
for i_time in range(100):
    step+=1
    for j in range(r.shape[0]):
        # bypass empty slots
        if idid[j]>=0:
            r[j,:] += -1+2*np.random.random_integers(0,1,r.shape[-1:])
            # Remove particles that are out of the boundaries
            if ( r[j,0]<0 or r[j,0]>NX or r[j,1]<0 or r[j,1]>NY ):
                idid[j] = -1
                slots.append(j)
                print "emptying slot", j
    if idid.max()<0:
        print "Exiting because of idid.max()<0"
        #break
    # Insert probalistically new particles
    if np.random.rand() > 0.95:
        if (len(slots)>1):
            j = slots.pop(0)
        else:
            new_N = part_id.value.shape[1]+part_id.value.chunks[1]
            new_r = np.zeros( (new_N, 2), dtype=r.dtype)
            new_r[:r.shape[0],:r.shape[1]] = r
            del r
            r = new_r
            new_id = np.zeros( (new_N,), dtype=idid.dtype )
            new_id[:idid.shape[0]] = idid
            new_id[idid.shape[0]:] = -1
            idid_shape = idid.shape
            del idid
            idid = new_id
            shape = part_pos.value.shape
            part_pos.value.resize( (shape[0], new_N, shape[2]) )
            shape = part_id.value.shape
            part_id.value.resize( (shape[0], new_N) )
            part_id.value[:,idid_shape[0]:] = -1
            j = shape[1]
        print "new slot", j
        max_id+=1
        idid[j] = max_id
        r[j] = [16,16]
    # Append the current position data to the H5MD file.
    part_pos.append(r, step, step*1.0)
    part_id.append(idid, step, step*1.0)
    print i_time, step, idid.shape, part_id.value.shape, idid.dtype, part_id.value.dtype, r.dtype, part_pos.value.dtype

print slots

# Close the file
f.close()
