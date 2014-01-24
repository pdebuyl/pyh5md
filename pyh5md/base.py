# -*- coding: utf-8 -*-
# Copyright 2012-2014 Pierre de Buyl
#
# This file is part of pyh5md
#
# pyh5md is free software and is licensed under the modified BSD license (see
# LICENSE file).

import numpy as np
import h5py

VL_STR = h5py.special_dtype(vlen=str)

def populate_H5MD_data(g, name, shape, dtype, chunks=None):
    """Creates a step,time,value H5MD data group."""
    g.step = g.create_dataset('step', shape=(0,), dtype=np.int32, maxshape=(None,))
    g.time = g.create_dataset('time', shape=(0,), dtype=np.float64, maxshape=(None,))
    g.value = g.create_dataset('value', shape=(0,)+shape, dtype=dtype, maxshape=(None,)+shape, chunks=chunks)

class TimeData(h5py.Group):
    """Represents time-dependent data within a H5MD file."""
    def __init__(self, parent, name, shape=None, dtype=None, data=None, chunks=None, unit=None, time_unit = None):
        """Create a new TimeData object."""
        if name in parent.keys():
            self._id = h5py.h5g.open(parent.id, name)
            self.step = self['step']
            self.time = self['time']
            self.value = self['value']
        else:
            if data is not None:
                if shape is not None or isinstance(dtype, np.dtype):
                    raise Exception('Overspecification')
                else:
                    self._id = h5py.h5g.create(parent.id, name)
                    populate_H5MD_data(self, name, data.shape, data.dtype, chunks=chunks)
            else:
                self._id = h5py.h5g.create(parent.id, name)
                populate_H5MD_data(self, name, shape, dtype, chunks=chunks)
            if unit is not None:
                self['value'].attrs.create('unit',data=unit,dtype=VL_STR)
            if time_unit is not None:
                self['time'].attrs.create('unit',data=time_unit,dtype=VL_STR)

    def append(self, data, step, time):
        """Appends a time slice to the data group."""
        s = self['step']
        t = self['time']
        v = self['value']
        if not isinstance(data, np.ndarray):
            data = np.array(data, ndmin=0, dtype=v.dtype)
        assert s.shape[0]==t.shape[0] and t.shape[0]==v.shape[0]
        assert data.shape==v.shape[1:]
        idx = v.shape[0]
        v.resize(idx+1,axis=0)
        v[-1] = data
        s.resize(idx+1, axis=0)
        s[-1] = step
        t.resize(idx+1, axis=0)
        t[-1] = time

class FixedData(h5py.Dataset):
    """Represents time-independent data within a H5MD file."""
    def __init__(self, parent, name, shape=None, dtype=None, data=None, unit=None):
        if name not in parent.keys():
            parent.create_dataset(name, shape, dtype, data)
        oid = h5py.h5o.open(parent.id, name)
        h5py.Dataset.__init__(self, oid)
        if unit is not None:
            self.attrs.create('unit',data=unit,dtype=VL_STR)
