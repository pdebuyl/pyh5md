import numpy as np
import nph
from nph import File, element

N = 32

with File('hop.h5', 'w') as f:
    f.fill_h5md('Pierre', 'run.py', 'N/A')

    f.observables = f.require_group('observables')
    e = element(f.observables, 'v', time='linear', shape=(0,1), maxshape=(None, 1), dtype=int, step=10)

    all_p = f.particles_group('/particles/all')

    all_p.create_box(dimension=3, boundary=['periodic']*3, 
                     #time='fixed', data=(1,1,1.))
                     time='time', shape=(0,)+(3,), maxshape=(None,3), dtype=np.float64)

    pos = np.zeros((N, 3))
    pos_e = element(all_p, 'position', time='time', shape=(0,)+pos.shape, maxshape=(None, None)+pos.shape[1:], dtype=pos.dtype, step_from=all_p.box.edges)

    mass = np.ones((N,))*100.0

    element(all_p, 'mass', time='fixed', data=mass)

    record = frozenset([0, 1, 2, 10])
    for step in range(21):
        pos += np.random.random(pos.shape)*0.1
        if step in record:
            all_p.box.edges.append((1,1,1), step)
            pos_e.append(pos, step)
        if step%e.attrs['step'] == 0:
            e.append(np.random.randint(10))


