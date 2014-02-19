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

H5MD_SET = frozenset(['step', 'time', 'value'])

def is_h5md(g):
    """Check whether a group is a well-defined H5MD time-dependent group. Raises
    an exception if a group contains the elements of H5MD_SET but does not
    comply to an equal length for all of them."""
    if H5MD_SET <= set(g.keys()):
        s_d = len(g['step'].shape)
        s_l = g['step'].shape[0]
        t_d = len(g['time'].shape)
        t_l = g['time'].shape[0]
        v_l = g['value'].shape[0]
        assert(
            (s_d == 1) and (t_d == 1) and (s_l == t_l) and (s_l == v_l)
            )
        return True
    else:
        return False

def populate_H5MD_data(g, name, shape, dtype, chunks=None):
    """Creates a step,time,value H5MD data group."""
    g.step = g.create_dataset('step', shape=(0,), dtype=np.int32, maxshape=(None,))
    g.time = g.create_dataset('time', shape=(0,), dtype=np.float64, maxshape=(None,))
    if shape==():
         maxshape=(None,)
    else:
        maxshape=(None, None)+shape[1:]
    g.value = g.create_dataset('value', shape=(0,)+shape, dtype=dtype, maxshape=maxshape, chunks=chunks)

class TimeData(h5py.Group):
    """Represents time-dependent data within a H5MD file."""
    def __init__(self, parent, name, shape=None, dtype=None, data=None, chunks=None, unit=None, time_unit = None):
        """Create a new TimeData object."""
        self.current_index = 0
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
                self['value'].attrs.create('unit',data=unit)
            if time_unit is not None:
                self['time'].attrs.create('unit',data=time_unit)

    def append(self, data, step, time, region=None):
        """Appends a time slice to the data group.

        region: tuple (start, stop, [step]) for the dimension 0 of the
        dataset. The resulting shape must be compatible with data.shape.
        """
        s = self['step']
        t = self['time']
        v = self['value']
        if not isinstance(data, np.ndarray):
            data = np.array(data, ndmin=0, dtype=v.dtype)
        assert s.shape[0]==t.shape[0] and t.shape[0]==v.shape[0]
        idx = v.shape[0]
        v.resize(idx+1,axis=0)
        if region is None:
            if len(v.shape)>1 and data.shape[0]>v.shape[1]:
                v.resize(data.shape[0], axis=1)
                sel = h5py._hl.selections.select(v.shape,
                                                 (slice(self.current_index,self.current_index+1),slice(0,min(data.shape[0],v.shape[1])),Ellipsis),
                                                 v.id)
            else:
                sel = self.current_index
        else:
            sel = h5py._hl.selections.select(v.shape,
                                             (slice(self.current_index,self.current_index+1),slice(*region),Ellipsis),
                                             v.id)
        v[sel] = data.reshape((1,)+data.shape)
        s.resize(idx+1, axis=0)
        s[self.current_index] = step
        t.resize(idx+1, axis=0)
        t[self.current_index] = time
        self.current_index+=1

class FixedData(h5py.Dataset):
    """Represents time-independent data within a H5MD file."""
    def __init__(self, parent, name, shape=None, dtype=None, data=None, unit=None):
        if name not in parent.keys():
            parent.create_dataset(name, shape, dtype, data)
        oid = h5py.h5o.open(parent.id, name)
        h5py.Dataset.__init__(self, oid)
        if unit is not None:
            self.attrs.create('unit',data=unit)
