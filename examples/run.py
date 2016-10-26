import numpy as np
from pyh5md import File, element

N = 32
DT = 0.1

with File('example_for_1.1.h5', 'w',author='Pierre', creator='run.py') as f:

    f.observables = f.require_group('observables')
    f.connectivity = f.require_group('connectivity')
    v_e = element(f.observables, 'v', store='linear', data=1, step=10, step_offset=10, time=5., time_offset=5.)

    f.all = f.particles_group('all')

    f.all.create_box(dimension=3, boundary=['periodic']*3,
                     store='time', shape=(3,), dtype=np.float64)

    pos = np.zeros((N, 3))
    pos_e = element(f.all, 'position', store='time', data=pos, step_from=f.all.box.edges)

    vel = np.random.random(pos.shape)-0.5
    vel_e = element(f.all, 'velocity', store='time', data=vel)

    force = np.random.random(pos.shape)-0.5
    force_e = element(f.all, 'force', store='time', data=force, time=True)

    mass = np.ones((N,))*100.0
    element(f.all, 'mass', store='fixed', data=mass)

    idx_all = np.arange(N)
    idx_list = np.random.choice(idx_all, 5)
    idx_e = element(f.observables, 'idx_list', store='linear', step=10, data=idx_list)
    idx_e.attrs['particles_group'] = f.all.ref

    pairs = np.random.randint(0, N, (11, 2))
    pairs_e = element(f.connectivity, 'random_pairs', store='fixed', data=pairs)
    pairs_e.attrs['particles_group'] = f.all.ref

    record = frozenset([0, 1, 2, 10])
    for step in range(21):
        force = np.random.random(pos.shape)-0.5
        vel += force*DT*0.5/mass.reshape((-1,1))
        pos += vel*DT
        vel += force*DT*0.5/mass.reshape((-1,1))
        idx_list = np.random.choice(idx_all, 5)
        if step in record:
            f.all.box.edges.append((1,1,1), step)
            pos_e.append(pos, step)
            vel_e.append(vel, step, step*DT)
            force_e.append(vel, step, step*DT)
        if step%v_e.step == 0:
            v_e.append(np.random.randint(10))
        if step%idx_e.step == 0:
            idx_e.append(idx_list, step)

