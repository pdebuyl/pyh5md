# -*- coding: utf-8 -*-
# Copyright 2013 Pierre de Buyl
# Copyright 2013 Konrad Hinsen
#
# This file is part of pyh5md
#
# pyh5md is free software and is licensed under the modified BSD license (see
# LICENSE file).

# This file is based on code from the h5py project. The complete h5py license is
# available at licenses/h5py.txt, in the distribution root directory.

import numpy

import h5py
import h5py.version
from h5py import h5s, h5t, h5r, h5d
from h5py._hl import dataset
from h5py._hl.base import HLObject, py3
from h5py._hl import filters
from h5py._hl import selections as sel
from h5py._hl import selections2 as sel2


def create_compact_dataset(loc, name, shape=None, dtype=None, data=None,
                           chunks=None, compression=None, shuffle=None,
                           fletcher32=None, maxshape=None,
                           compression_opts=None, fillvalue=None,
                           scaleoffset=None, track_times=None):
    """Create a new HDF5 dataset with a compact storage layout."""

    # Convert data to a C-contiguous ndarray
    if data is not None:
        import h5py._hl.base
        data = numpy.asarray(data, order="C", dtype=h5py._hl.base.guess_dtype(data))

    # Validate shape
    if shape is None:
        if data is None:
            raise TypeError("Either data or shape must be specified")
        shape = data.shape
    else:
        shape = tuple(shape)
        if data is not None and (numpy.product(shape) != numpy.product(data.shape)):
            raise ValueError("Shape tuple is incompatible with data")

    if isinstance(dtype, h5py.Datatype):
        # Named types are used as-is
        tid = dtype.id
        dtype = tid.dtype  # Following code needs this
    else:
        # Validate dtype
        if dtype is None and data is None:
            dtype = numpy.dtype("=f4")
        elif dtype is None and data is not None:
            dtype = data.dtype
        else:
            dtype = numpy.dtype(dtype)
        tid = h5t.py_create(dtype, logical=1)

    # Legacy
    if any((compression, shuffle, fletcher32, maxshape,scaleoffset)) and chunks is False:
        raise ValueError("Chunked format required for given storage options")

    # Legacy
    if compression is True:
        if compression_opts is None:
            compression_opts = 4
        compression = 'gzip'

    # Legacy
    if compression in range(10):
        if compression_opts is not None:
            raise TypeError("Conflict in compression options")
        compression_opts = compression
        compression = 'gzip'

    if h5py.version.version_tuple >= (2, 2, 0, ''):
        dcpl = filters.generate_dcpl(shape, dtype, chunks, compression,
                                     compression_opts, shuffle, fletcher32,
                                     maxshape, None)
    else:
        dcpl = filters.generate_dcpl(shape, dtype, chunks, compression,
                                     compression_opts, shuffle, fletcher32,
                                     maxshape)

    if fillvalue is not None:
        fillvalue = numpy.array(fillvalue)
        dcpl.set_fill_value(fillvalue)

    if track_times in (True, False):
        dcpl.set_obj_track_times(track_times)
    elif track_times is not None:
        raise TypeError("track_times must be either True or False")

    dcpl.set_layout(h5d.COMPACT)

    if maxshape is not None:
        maxshape = tuple(m if m is not None else h5s.UNLIMITED for m in maxshape)
    sid = h5s.create_simple(shape, maxshape)


    dset_id = h5d.create(loc.id, None, tid, sid, dcpl=dcpl)

    if data is not None:
        dset_id.write(h5s.ALL, h5s.ALL, data)

    dset = dataset.Dataset(dset_id)
    if name is not None:
        loc[name] = dset
    return dset
