# -*- coding: utf-8 -*-
# Copyright 2012-2013 Pierre de Buyl
# Copyright 2013 Felix Hoëfling
# Copyright 2013 Konrad Hinsen
#
# This file is part of pyh5md
#
# pyh5md is free software and is licensed under the modified BSD license (see
# LICENSE file).

import numpy as np
import h5py
import time

from pyh5md.utils import create_compact_dataset
from pyh5md.module import module_dict
from pyh5md.box import Box
from pyh5md.base import VL_STR, TimeData, FixedData, is_h5md

TRAJECTORY_NAMES = ['position', 'image', 'velocity', 'force', 'mass', 'species', 'id']

class Walker(object):
    """Finds all HDF5 groups within a given group."""
    def __init__(self, f):
        self.f = f
        self.walk_list = []

    def walk(self, g=None):
        if g==None:
            g = self.f['/']
        if type(g)==h5py.Group:
            if is_h5md(g): self.walk_list.append(g)
            for k in g.keys():
                self.walk(g[k])

    def get_list(self):
        return self.walk_list

    def check(self):
        if len(self.walk_list)==0:
            raise Exception('Nothing to check')
        for g in self.walk_list:
            assert(is_h5md(g))

def particle_data(group, name=None, shape=None, dtype=None, data=None, time=True, chunks=None, unit=None, time_unit=None):
    """Returns particles data as a FixedData or TimeData."""
    if name is None:
        raise Exception('No name provided')
    if name in group.keys():
        item = group[name]
        if type(item)==h5py.Group:
            assert is_h5md(item)
            return TimeData(group, name)
        elif type(item)==h5py.Dataset:
            assert shape==dtype==data==None
            return FixedData(group, name)
        else:
            raise Exception('name does not provide H5MD data')
    else:
        if time:
            return TimeData(group, name, shape, dtype, data, chunks=chunks, unit=unit, time_unit=time_unit)
        else:
            return FixedData(group, name, shape, dtype, data, unit=unit)

class ParticlesGroup(h5py.Group):
    """Represents a particles group within a H5MD file."""
    def __init__(self, parent, name):
        """Create a new ParticlesGroup object."""
        if 'particles' not in parent.keys():
            parent.create_group('particles')
        p = parent['particles']
        if name in p.keys():
            self._id = h5py.h5g.open(p.id, name)
        else:
            self._id = h5py.h5g.create(p.id, name)
    def trajectory(self, name, shape=None, dtype=None, data=None, time=True, chunks=None, unit=None, time_unit=None):
        """Returns data as a TimeData or FixedData object."""
        return particle_data(self, name, shape, dtype, data, time, chunks=chunks, unit=unit, time_unit=time_unit)
    def box(self, dimension, boundary, edges=None, time=False,
                unit=None, time_unit=None):
        """Creates a box in the particles group. Returns the box group."""
        return Box(self, dimension, boundary, edges, time, unit, time_unit)

class H5MD_File(object):
    """Class to create and read H5MD compliant files."""
    def __init__(self,filename,mode,**kwargs):
        """Create or read an H5MD file, according to argument mode.
        mode should be 'r', 'r+' or 'w'"""
        if mode not in ['r','r+','w']:
            raise ValueError('unknown mode "%s" in H5MD_File' % mode)
        if mode=='w':
            kw = kwargs.keys()
            for key in ['creator', 'author', 'creator_version']:
                if key not in kw:
                    raise ValueError('missing argument "%s" in H5MDFile' % key)
        if 'driver' in kwargs:
            if kwargs['driver']=='mpio':
                if 'comm' in kwargs:
                    comm = kwargs['comm']
                    self.f = h5py.File(filename, mode, driver='mpio', comm=comm)
                    self.f.comm = comm
                else:
                    raise ValueError('Driver is %s but comm is not provided' % kwargs['driver'])
        else:
            self.f = h5py.File(filename, mode)
        self.modules = []
        if mode=='w':
            h5md_group = self.f.create_group('h5md')
            h5md_group.attrs['version'] = np.array([1,0])
            author_group = h5md_group.create_group('author')
            author_group.attrs.create('name', data=kwargs['author'])
            if 'author_email' in kwargs and kwargs['author_email'] is not None:
                author_group.attrs.create('email', data=kwargs['author_email'])
            creator_group = h5md_group.create_group('creator')
            creator_group.attrs.create('name', data=kwargs['creator'])
            creator_group.attrs.create('version', data=kwargs['creator_version'])
            if 'modules' in kwargs:
                modules = kwargs['modules']
                assert isinstance(modules, dict)
                module_group = h5md_group.create_group('modules')
                for module_name, version in modules.items():
                    if module_name not in module_dict:
                        raise ValueError('Unknown module "%s"' % module_name)
                    self.modules.append(module_dict[module_name](module_group, version))
        elif mode=='r':
            h5md_group = self.f['h5md']
            if type(h5md_group) == h5py.Group and 'modules' in h5md_group.keys():
                module_group = h5md_group['modules']
                for module_name in module_group.keys():
                    self.modules.append(module_dict[module_name](module_group))


    def close(self):
        """Closes the HDF5 file."""
        self.f.close()

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.close()
        return False

    def particles_group(self, group_name):
        """Adds or open a group in /particles. If /particles does not exist,
        it will be created."""
        return ParticlesGroup(self.f, group_name)

    def observable(self, obs_name, shape=None, dtype=None, data=None, time=True, chunks=None, unit=None, time_unit = None):
        """Returns observable data as a TimeData object."""
        if 'observables' in self.f.keys():
            group = self.f['observables']
        else:
            group = self.f.create_group('observables')
        if obs_name in self.f['observables'].keys():
            item = group[obs_name]
            if type(item)==h5py.Group:
                assert is_h5md(item)
                return TimeData(group, obs_name)
            elif type(item)==h5py.Dataset:
                assert shape==dtype==data==None
                return FixedData(group, obs_name)
            else:
                raise Exception('obs_name does not provide H5MD data')
        else:
            if time:
                return TimeData(self.f['observables'],obs_name, shape=shape, dtype=dtype, data=data, chunks=chunks, unit=unit, time_unit=time_unit)
            else:
                return FixedData(self.f['observables'],obs_name, shape=shape, dtype=dtype, data=data, unit=unit)
        
    def check(self):
        """Checks the file conformance."""
        # Checks the presence of the global attributes.
        assert(set(['version']) <= set(self.f['h5md'].attrs.keys()))
        assert(set(['name']) <= set(self.f['h5md/author'].attrs.keys()))
        assert(set(['name','version']) <= set(self.f['h5md/creator'].attrs.keys()))
        # Check that version is of appropriate shape.
        assert(self.f['h5md'].attrs['version'].shape==(2,))
        w = Walker(self.f)
        w.walk()
