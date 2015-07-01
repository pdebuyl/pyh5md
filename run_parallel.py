import numpy as np
from h5md_module import File, element
from mpi4py import MPI

import argparse

parser = argparse.ArgumentParser()
parser.add_argument('--collective', action='store_true')
args = parser.parse_args()

N = 128*128
DT = 0.1

comm = MPI.COMM_WORLD
rank = comm.rank
size = comm.size
print rank

local_ids = np.empty(N, dtype=int)

def assign_ids():
    global local_ids
    if rank==0:
        data = np.arange(N*size, dtype=int)
        np.random.shuffle(data)
        for i in range(1, size):
            comm.Send(data[i*N:(i+1)*N], dest=i, tag=11)
        local_ids = data[0:N]
    else:
        comm.Recv(local_ids, source=0, tag=11)


with File('parallel_example_for_1.1.h5', 'w',author='Pierre', creator='run.py',
          driver='mpio', comm=comm) as f:

    f.observables = f.require_group('observables')
    f.connectivity = f.require_group('connectivity')
    v_e = element(f.observables, 'v', store='linear', data=1, step=10, step_offset=10, time=5., time_offset=5.)

    f.all = f.particles_group('all')

    f.all.create_box(dimension=3, boundary=['periodic']*3,
                     store='time', shape=(0,)+(3,), maxshape=(None,3), dtype=np.float64)

    id_e = element(f.all, 'id', store='time', shape=(0, N*size,), dtype=int, maxshape=(None, N*size))

    pos = np.zeros((N, 3))
    pos_e = element(f.all, 'position', store='time', shape=(0, N*size, 3), maxshape=(None, N*size, 3), dtype=np.float64, step_from=f.all.box.edges)

    vel = np.random.random(pos.shape)-0.5
    vel_e = element(f.all, 'velocity', store='time', shape=(0, N*size, 3), maxshape=(None, N*size, 3), dtype=np.float64, time=5.)

    force = np.random.random(pos.shape)-0.5
    force_e = element(f.all, 'force', store='linear', shape=(0, N*size, 3), maxshape=(None, N*size, 3), dtype=np.float64, step=1, time=DT)

    mass = np.ones((N,))*100.0
    element(f.all, 'mass', store='fixed', shape=(N*size,), dtype=np.float64)
    
    record = frozenset([0, 1, 2, 10])
    for step in range(21):
        assign_ids()
        force = np.random.random(pos.shape)-0.5
        vel += force*DT*0.5/mass.reshape((-1,1))
        pos += vel*DT
        vel += force*DT*0.5/mass.reshape((-1,1))
        store_ids = False
        if step in record:
            f.all.box.edges.append((1,1,1), step)
            pos_e.append(pos, step, region=(rank*N,(rank+1)*N), collective=args.collective)
            vel_e.append(vel, step, step*DT, region=(rank*N,(rank+1)*N), collective=args.collective)
            store_ids = True
        if step%force_e.step == 0:
            force_e.append(force, region=(rank*N,(rank+1)*N), collective=args.collective)
            store_ids = True
        if step%v_e.step == 0:
            v_e.append(np.random.randint(10))
            store_ids = True
        if store_ids:
            id_e.append(local_ids, step, region=(rank*N,(rank+1)*N), collective=args.collective)
