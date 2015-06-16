import numpy as np
from h5md_module import File, element

import sys

with File(sys.argv[1], 'r') as f:
    all_particles = f.particles_group('all')

    for loc, name in (
        (f['observables'], 'v'),
        (all_particles, 'mass'),
        (all_particles['box'], 'edges'),
        (all_particles, 'id'),
        (all_particles, 'position'),
        (all_particles, 'force'),
        (all_particles, 'velocity'),
    ):
        if name not in loc:
            continue
        el = element(loc, name)
        print '---------------------------------------------------------------'
        print '%-10s ----------------------------------------------------' % name
        print el.element_type
        print el.value.shape, el.step, el.step_offset, el.time, el.time_offset, el.value
