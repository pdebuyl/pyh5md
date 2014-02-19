# -*- coding: utf-8 -*-
# Copyright 2014 Pierre de Buyl
#
# This file is part of pyh5md
#
# pyh5md is free software and is licensed under the modified BSD license (see
# LICENSE file).

import numpy as np
import h5py

from pyh5md.base import VL_STR, TimeData, FixedData

class Box(h5py.Group):
    """Represents a simulation box."""
    def __init__(self, parent, dimension, boundary, edges=None, time=False, unit=None, time_unit=None):
        """Initializes a simulation box."""
        assert(len(boundary)==dimension)
        for b in boundary:
            assert(b in ['none', 'periodic'])
        if edges is None:
            if not all([b=='none' for b in boundary]):
                raise ValueError("Not all boundary elements are 'none' though edges is missing in set_box.")
        else:
            assert(len(edges)==dimension)
        if 'box' in parent.keys():
            raise NotImplemented
            self._id = h5py.h5g.open(parent.id, 'box')
        else:
            self._id = h5py.h5g.create(parent.id, 'box')
        self.attrs['dimension'] = dimension
        self.attrs.create('boundary', data=boundary)
        if time:
            if edges is not None:
                self.edges = TimeData(self, 'edges', data=np.asarray(edges), unit=unit, time_unit=time_unit)
        else:
            if edges is not None:
                ds = create_compact_dataset(self, 'edges', data=edges)
                if unit is not None:
                    assert isinstance(unit, str)
                    ds.attrs.create('unit', data=unit)


        
