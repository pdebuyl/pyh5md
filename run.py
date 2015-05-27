import numpy as np
from h5md_module import File, element

N = 32
DT = 0.1

with File('hop.h5', 'w') as f:
    f.fill_h5md('Pierre', 'run.py', 'N/A')

    f.observables = f.require_group('observables')
    v_e = element(f.observables, 'v', store='linear', data=(1,), step=10, step_offset=10, time=5., time_offset=5.)

    f.all = f.particles_group('all')

    f.all.create_box(dimension=3, boundary=['periodic']*3,
                     store='time', shape=(0,)+(3,), maxshape=(None,3), dtype=np.float64)

    pos = np.zeros((N, 3))
    pos_e = element(f.all, 'position', store='time', data=pos, step_from=f.all.box.edges)

    vel = np.random.random(pos.shape)-0.5
    vel_e = element(f.all, 'velocity', store='time', data=vel, time=5.)

    force = np.random.random(pos.shape)-0.5
    force_e = element(f.all, 'force', store='time', data=force, time=True)

    mass = np.ones((N,))*100.0
    element(f.all, 'mass', store='fixed', data=mass)

    record = frozenset([0, 1, 2, 10])
    for step in range(21):
        force = np.random.random(pos.shape)-0.5
        vel += force*DT*0.5/mass.reshape((-1,1))
        pos += vel*DT
        vel += force*DT*0.5/mass.reshape((-1,1))
        if step in record:
            f.all.box.edges.append((1,1,1), step)
            pos_e.append(pos, step)
            vel_e.append(vel, step, step*DT)
            force_e.append(vel, step, step*DT)
        if step%v_e['step'][()] == 0:
            v_e.append(np.random.randint(10))

