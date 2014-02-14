pyh5md : Read and write H5MD files
==================================

Copyright © 2012-2014 Pierre de Buyl and contributors

pyh5md is a Python module that facilitate reading and writing
[H5MD](http://nongnu.org/h5md/) files. H5MD is a file format specification based
on [HDF5](http://www.hdfgroup.org/HDF5/) for storing molecular data. pyh5md
depends on [h5py](http://h5py.alfven.org/) to access HDF5 files.

pyh5md is developped by Pierre de Buyl (see also CONTRIBUTORS file) and is
released under the modified BSD license that can be found in the file LICENSE.

Install
-------

    python setup.py install --user

installs pyh5md for the current user

Examples
--------

Once pyh5md is installed:

    cd examples
    python random_walk_1d.py

executes an example program that generates the H5MD file `walk_1d.h5`.
