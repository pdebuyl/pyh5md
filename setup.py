"""
pyh5md is a library to read and write easily H5MD files. H5MD is a file format
specification based on HDF5 to store molecular data (http://nongnu.org/h5md/).
pyh5md is built on top of h5py, the Python HDF5 library by Andrew Colette.
"""
from setuptools import setup

setup(name="pyh5md",
      version="1.0.0.dev1",
      description="pyh5md - Read and write H5MD files",
      long_description=__doc__,
      author="Pierre de Buyl",
      author_email="pdebuyl@pdebuyl.be",
      license="BSD",
      url="https://github.com/pdebuyl/pyh5md",
      packages=["pyh5md"],
      )
