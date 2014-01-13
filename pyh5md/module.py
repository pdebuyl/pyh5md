# -*- coding: utf-8 -*-
# Copyright 2013 Pierre de Buyl
# Copyright 2013 Konrad Hinsen
#
# This file is part of pyh5md
#
# pyh5md is free software and is licensed under the modified BSD license (see
# LICENSE file).

import numpy as np
import h5py

module_dict = dict()

class Module(object):
    """Base class to represent H5MD modules."""
    def __init__(self, loc, version=None):
        """Initializes a H5MD module from name and version.

        loc
            The ``h5md/modules`` group.
        version
            A tuple of two integers indicating the version of the
            module, when adding a module to a file. If version is
            absent (or set to None), it is read from the file.
        """
        if version is None:
            g = loc[self._name]
            self.version = tuple(g.attrs['version'])
            if self.version not in self.known_versions:
                raise ValueError("Module version %s not know for %s" % (str(self.version), self._name))
        else:
            assert len(version) == 2
            self.version = tuple(version)
            g = loc.create_group(self._name)
            g.attrs['version'] = self.version

    def __repr__(self):
        return "H5MD module '%s' v%i.%i" % (self._name, self.version[0], self.version[1])

def register_module(module_class):
    """Add a module to the list of recognized H5MD modules."""
    assert issubclass(module_class, Module)
    assert isinstance(module_class._name, basestring)
    module_dict[module_class._name] = module_class

class UnitsModule(Module):
    """The 'units' H5MD module."""
    _name = 'units'
    def __init__(self, loc, version=None):
        self.known_versions = [(0,1)]
        super(UnitsModule, self).__init__(loc, version)
register_module(UnitsModule)

class ThermodynamicsModule(Module):
    """The 'thermodynamics' H5MD module."""
    _name = 'thermodynamics'
    def __init__(self, loc, version=None):
        self.known_versions = [(0,1)]
        super(ThermodynamicsModule, self).__init__(loc, version)
register_module(ThermodynamicsModule)
