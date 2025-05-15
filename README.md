pyh5md : Read and write H5MD files
==================================

Copyright 2012-2017,2025 Pierre de Buyl and contributors  
*License:* BSD

pyh5md is a library to read and write easily H5MD files. [H5MD][] is a file
format specification based on [HDF5][] to store molecular data. pyh5md is built
on top of [h5py][], the HDF5 for Python library by Andrew Colette.

[H5MD]: http://nongnu.org/h5md/
[HDF5]: http://www.hdfgroup.org/HDF5/
[h5py]: http://h5py.org/

pyh5md used to define a complex class structure. Since version 1.0.0.dev1, a light
subclassing of h5py's classes is used instead.

Install
-------

It is recommended to install in a virtual environment. Then,

    pip install pyh5md

installs pyh5md in that virtual environment. To install from the git repository:

    pip install .

Examples
--------

Once pyh5md is installed:

    cd examples
    python random_walk_1d.py

executes an example program that generates the H5MD file `walk_1d.h5`.

Usage
-----

To write data to a particles group named "atoms", with a fixed set of positions:

```
from pyh5md import File, element
kwargs = {'creator': 'pyh5md README example',
	      'author': 'Pierre de Buyl',
          }
with File('new_file.h5', 'w', **kwargs) as f:
    g = f.particles_group('atoms')
    g.create_box(dimension=3, boundary=['none']*3)
    element(g, 'position', store='fixed', data=np.random.random(size=(32, 3)))
```

To read data from a H5MD file created with, for instance, LAMMPS:

```
from pyh5md import File, element
with File('dump_3d.h5', 'r') as f:
    g = f.particles_group('all')
    box_edges = element(g, 'box/edges').value[0]
    position = element(g, 'position').value[:]
```
