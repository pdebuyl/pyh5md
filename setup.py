from distutils.core import setup

setup(name="pyh5md",
      version="0.1",
      description="pyh5md - Read and write H5MD files",
      author="Pierre de Buyl",
      author_email="pdebuyl at ulb dot ac dot be",
      maintainer="Pierre de Buyl",
      maintainer_email="pdebuyl at ulb dot ac dot be",
      license="BSD",
      url="http://github.com/pdebuyl/pyh5md",
      packages=["pyh5md"],
      install_requires=['h5py'],
)

