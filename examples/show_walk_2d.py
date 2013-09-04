import numpy as np
import pyh5md
import matplotlib.pyplot as plt

a = pyh5md.H5MD_File('walk_2d.h5', 'r')

t = a.particles_group('tracers')

r = t.trajectory('position')
idid = t.trajectory('id')

# for j in range(r.value.shape[1]):
#     mask = idid.value[:,j] >= 0
#     plt.plot(r.step[mask], r.value[mask,j,:])

# plt.figure()
# for j in range(r.value.shape[1]):
#     plt.plot(r.step[:], r.value[:,j,:])

plt.figure()
ax1 = plt.subplot(211)
ax2 = plt.subplot(212)
all_id = set(idid.value[:].ravel().tolist())
all_id.discard(-1)
for j in all_id:
    for k in range(idid.value.shape[1]):
        mask = idid.value[:,k]==j
        #print j, k, mask
        if mask.sum()>1:
            print "found", j, "in", k
            ax1.plot(r.step[mask], r.value[mask,k,0], label=str(j))
            ax2.plot(r.step[mask], r.value[mask,k,1], label=str(j))
plt.legend()

plt.figure()
all_id = set(idid.value[:].ravel().tolist())
all_id.discard(-1)
for j in all_id:
    for k in range(idid.value.shape[1]):
        mask = idid.value[:,k]==j
        if mask.sum()>1: plt.plot(r.value[mask,k,0], r.value[mask,k,1], label=str(j))
plt.legend()


a.close()
plt.show()
