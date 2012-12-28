import numpy as np
import pyh5md

f = pyh5md.H5MD_File('poc.h5', 'w', creator='run_h5md', creator_version='0', author='Pierre de Buyl')

at = f.trajectory('atoms')

r = np.zeros((100,3), dtype=np.float64)

at_pos = at.add_data('position', r.shape, r.dtype)

at_pos.append(r, 0, 0.)

f.f.close()
