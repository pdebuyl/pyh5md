# Copyright 2012-2013 Pierre de Buyl
#
# This file is part of pyh5md
#
# pyh5md is free software and is licensed under the modified BSD license (see
# LICENSE file).

import numpy as np
import pyh5md

f = pyh5md.H5MD_File('particles_3d.h5', 'r')

at = f.trajectory_group('atoms')

at_pos = at.trajectory('position')

r = at_pos.v.value

print r

f.f.close()
