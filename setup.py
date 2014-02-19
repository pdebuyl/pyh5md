from distutils.core import setup

setup(name="pyh5md",
      version="0.1",
      description="pyh5md - Read and write H5MD files",
      long_desc = \
"""
pyh5md is built on top of h5py, the Python HDF5 library by Andrew Colette, to
read and write easily H5MD files. H5MD is a file format specification based
on HDF5 to store molecular data, see http://nongnu.org/h5md/
""",
      author="Pierre de Buyl",
      author_email="pdebuyl at ulb dot ac dot be",
      maintainer="Pierre de Buyl",
      maintainer_email="pdebuyl at ulb dot ac dot be",
      license="BSD",
      url="http://github.com/pdebuyl/pyh5md",
      packages=["pyh5md"],
      install_requires=['h5py'],
)

