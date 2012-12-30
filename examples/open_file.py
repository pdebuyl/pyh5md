# Copyright 2012 Pierre de Buyl
#
# This file is part of pyh5md
#
# pyh5md is free software and is licensed under the modified BSD license (see
# LICENSE file).

import numpy as np
import pyh5md

f = pyh5md.H5MD_File('poc.h5', 'r')

at = f.trajectory('atoms')

at_pos = at.data('position')

r = at_pos.v.value

print r

f.f.close()
