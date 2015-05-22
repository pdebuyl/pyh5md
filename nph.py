import numpy as np
import h5py

class Element(object):
    def append(self, *args, **kwargs):
        raise NotImplementedError

class FixedElement(Element, h5py.Dataset):
    def __init__(self, loc, name, **kwargs):
        loc.create_dataset(name, **kwargs)
    def append(self, v, step=None):
        pass

class LinearElement(h5py.Dataset, Element):
    def __init__(self, loc, name, **kwargs):
        attrs = {}
        attrs['step'] = kwargs.pop('step')
        for a in ('step0', 'time', 'time0'):
            val = kwargs.pop(a, None)
            if val is not None:
                attrs[a] = val
        d = loc.create_dataset(name, **kwargs)
        super(LinearElement, self).__init__(d._id)
        for a in ('step', 'step0', 'time', 'time0'):
            if a in attrs.keys():
                self.attrs[a] = attrs[a]
    def append(self, v, step=None):
        self.resize(self.shape[0]+1, axis=0)
        self[-1] = v

class TimeElement(Element, h5py.Group):
    def __init__(self, loc, name, **kwargs):
        g = loc.create_group(name)
        step_from = kwargs.pop('step_from', None)
        if step_from is not None:
            g['step'] = step_from.step
            self.step = step_from.step
            self.own_step = False
        else:
            self.step = g.create_dataset('step', dtype=int, shape=(0,), maxshape=(None,))
            self.own_step = True
        self.value = g.create_dataset('value', **kwargs)
    def append(self, v, step, time=None):
        self.value.resize(self.value.shape[0]+1, axis=0)
        self.value[-1] = v
        if self.own_step:
            self.step.resize(self.step.shape[0]+1, axis=0)
            self.step[-1] = step

def element(loc, name, **kwargs):
    time = kwargs.pop('time')
    if time=='fixed':
        return FixedElement(loc, name, **kwargs)
    data = kwargs.pop('data', None)
    if data is not None:
        if type(data) is not np.ndarray:
            data = np.asarray(data)
        kwargs['shape'] = (0,) + data.shape
        kwargs['maxshape'] = (None,) + data.shape
        kwargs['dtype'] = data.dtype
    if time=='linear':
        return LinearElement(loc, name, **kwargs)
    elif time=='time':
        return TimeElement(loc, name, **kwargs)
    else:
        raise ValueError
        
class File(h5py.File):
    def fill_h5md(self, a, c, c_v):
        g = self.create_group('h5md')
        g.attrs['version'] = np.array([1,0])
        g = self.create_group('h5md/author')
        g.attrs['name'] = a
        g = self.create_group('h5md/creator')
        g.attrs['name'] = c
        g.attrs['version'] = c_v

    def particles_group(self, name):
        return ParticlesGroup(self, name)

class ParticlesGroup(h5py.Group):
    """Represents a particles group within a H5MD file."""
    def __init__(self, parent, name):
        """Create a new ParticlesGroup object."""
        super(ParticlesGroup, self).__init__(parent.require_group('particles').require_group(name)._id)

    def create_box(self, dimension=None, boundary=None, **kwargs):
        self.box = self.require_group('box')
        if dimension is not None and boundary is not None:
            assert len(boundary)==dimension
            self.box.attrs['dimension'] = dimension
            self.box.attrs['boundary'] = boundary
        self.box.edges = element(self.box, 'edges', **kwargs)


