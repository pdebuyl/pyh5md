import numpy as np
import nph
from nph import File, element

f = File('particles_3d.h5', 'w')
f.fill_h5md('Pierre de Buyl', 'run_h5md', 'N/A')

# Creating atom group
at = f.particles_group('atoms')

# Creating position data
r = np.zeros((100,3), dtype=np.float64)
at_pos = element(at,'position', time='time', data=r)

# Creating species
s = np.ones(r.shape[:1])
element(at, 'species', data=s, time='fixed')

# Creating velocity data
v = np.zeros((100,3), dtype=np.float64)
at_v = element(at, 'velocity', time='time', data=v)

# Create an observable
com = r.mean(axis=0)
obs_com = element(f, 'observables/center_of_mass', time='time', data=com)
# Create a scalar time independent observable
element(f, 'observables/random_number', data=np.random.random(), time='fixed')

edges = (1.,1.,1.)
box = at.create_box(dimension=3, boundary=['none', 'none', 'none'], time='time',
                    data=edges, step_from=at_pos)

DT = 0.1
time = 0.
def dump(t):
    if t%10==0:
        at_pos.append(r, t)
        at_v.append(v, t)
        obs_com.append(r.mean(axis=0), t)
        at.box.edges.append(edges, t)

dump(0)
t = 0
t_max = 200
while t<t_max:
    r += DT*0.5*v
    v += DT*np.random.normal(0., 1., v.shape)
    r += DT*0.5*v
    time += DT
    t += 1
    dump(t)

f.close()
