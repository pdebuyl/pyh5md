# Copyright 2012 Pierre de Buyl
#
# This file is part of pyh5md
#
# pyh5md is free software and is licensed under the modified BSD license (see
# LICENSE file).

import numpy as np
import pyh5md

f = pyh5md.H5MD_File('poc.h5', 'w', creator='run_h5md', creator_version='0', author='Pierre de Buyl')

at = f.trajectory('atoms')

r = np.zeros((100,3), dtype=np.float64)

at_pos = at.data('position', r.shape, r.dtype)

at_pos.append(r, 0, 0.)

f.f.close()
