import pyh5md
import os.path
import numpy as np


def test_open_file(tmpdir):
    f = pyh5md.File(str(tmpdir.join('test.h5')), mode='w',
                    author='Pierre de Buyl', creator='pyh5md test_create_file',
                    creator_version='N/A')
    assert 'h5md' in f.keys()
    assert np.all(f['h5md'].attrs['version'][:] == np.array((1, 1)))
    f.close()


def test_particles_group(tmpdir):
    f = pyh5md.File(str(tmpdir.join('test.h5')), mode='w',
                    author='Pierre de Buyl', creator='pyh5md test_create_file',
                    creator_version='N/A')
    name = 'atoms'
    particles_group = f.particles_group(name)
    assert 'particles' in f
    assert name in f.require_group('particles')
    f.close()


def test_fixed_element(tmpdir):
    f = pyh5md.File(str(tmpdir.join('test.h5')), mode='w',
                    author='Pierre de Buyl', creator='pyh5md test_create_file',
                    creator_version='N/A')
    name = 'atoms'
    N = 91
    particles_group = f.particles_group(name)
    mass = pyh5md.element(particles_group, 'mass', store='fixed',
                          data=np.ones(N))
    assert type(mass) is pyh5md.FixedElement
    assert mass.value.shape == (N,)
    f.close()


def test_context_manager(tmpdir):
    with pyh5md.File(str(tmpdir.join('test.h5')), mode='w',
                     author='Pierre de Buyl',
                     creator='pyh5md test_create_file',
                     creator_version='N/A') as f:
        assert 'h5md' in f.keys()
