# Copyright 2012-2013 Pierre de Buyl
#
# This file is part of pyh5md
#
# pyh5md is free software and is licensed under the modified BSD license (see
# LICENSE file).

import numpy as np
import pyh5md
from pyh5md.core import is_h5md
import h5py

with pyh5md.H5MD_File('particles_3d.h5', 'r') as f:
    f.check()

