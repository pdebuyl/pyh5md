import numpy as np
from h5md_module import File, element

with File('example_for_1.1.h5', 'r') as f:
    all_particles = f.particles_group('all')
    assert 'id' not in all_particles

    for loc, name in (
        (f['observables'], 'v'),
        (all_particles, 'mass'),
        (all_particles['box'], 'edges'),
        (all_particles, 'position'),
        (all_particles, 'force'),
        (all_particles, 'velocity'),
    ):
        el = element(loc, name)
        print '---------------------------------------------------------------'
        print '%-10s ----------------------------------------------------' % name
        print el.element_type
        print el.value.shape, el.step, el.step_offset, el.time, el.time_offset, el.value
