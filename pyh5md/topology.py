# -*- coding: utf-8 -*-
# Copyright 2014 Pierre de Buyl
#
# This file is part of pyh5md
#
# pyh5md is free software and is licensed under the modified BSD license (see
# LICENSE file).

import numpy as np
import h5py

from pyh5md.base import VL_STR, TimeData, FixedData, is_h5md

VL_INT = h5py.special_dtype(vlen=int)

def get_bond_list(group, name=None, time=False, time_unit=None):
    if name is None:
        raise ValueError('No name provided')
    if name in group.keys():
        # Open existing bond list
        item = group[name]
        if type(item)==h5py.Group:
            assert is_h5md(item)
            return TimeData(group, name)
        elif type(item)==h5py.Dataset:
            return FixedData(group, name)
        else:
            raise Exception('name does not provide H5MD data')
    else:
        # Create new bond list
        if time:
            return TimeData(group, name, shape=(), dtype=VL_INT, chunks=(16,))
        else:
            return FixedData(group, name, shape=(), dtype=VL_INT)

class TopologyGroup(h5py.Group):
    """Represents the topology group."""
    def __init__(self, parent, name):
        if name not in parent['particles'].keys():
            raise ValueError('Given particles_group does not exist')
        if 'topology' not in parent.keys():
            parent.create_group('topology')
        t = parent['topology']
        if name in t.keys():
            self._id = h5py.h5g.open(t.id, name)
        else:
            self._id = h5py.h5g.create(t.id, name)
    def bond_list(self, name, time=False, time_unit=None):
        """Returns the bond list as a TimeData of FixedData object."""
        return get_bond_list(self, name, time, time_unit)


def read_bonds(data):
    return np.array(data).reshape( (-1, 2) )

def write_bonds(data):
    return np.array(data).reshape( (-1,) )
