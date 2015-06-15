import numpy as np
import h5py

class Element(object):
    def append(self, *args, **kwargs):
        raise NotImplementedError

class FixedElement(h5py.Dataset, Element):
    def __init__(self, loc, name, **kwargs):
        d = loc.create_dataset(name, **kwargs)
        super(FixedElement, self).__init__(d._id)
    def append(self, v, step=None, time=None):
        pass

class LinearElement(h5py.Group, Element):
    def __init__(self, loc, name, **kwargs):
        g = loc.create_group(name)
        step = kwargs.pop('step')
        step_offset = kwargs.pop('step_offset', None)
        time = kwargs.pop('time', None)
        time_offset = kwargs.pop('time_offset', None)
        self.value = g.create_dataset('value', **kwargs)
        super(LinearElement, self).__init__(g._id)
        self.step = g.create_dataset('step', data=int(step))
        if step_offset is not None:
            self.step.attrs['offset'] = int(step_offset)
            self.step_offset = int(step_offset)
        if time is not None:
            self.time = g.create_dataset('time', data=time)
            if time_offset is not None:
                self.time.attrs['offset'] = time_offset
                self.time_offset = time_offset
    def append(self, v, step=None, time=None):
        self.value.resize(self.value.shape[0]+1, axis=0)
        self.value[-1] = v

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
        time = kwargs.pop('time', None)
        if time is not None:
            if self.own_step:
                if time==True:
                    self.time = g.create_dataset('time', dtype=float, shape=(0,), maxshape=(None,))
                else:
                    self.time = g.create_dataset('time', data=time)
            else:
                g['time'] = self.time = step_from.time
        else:
            self.time = None
        self.value = g.create_dataset('value', **kwargs)
    def append(self, v, step, time=None):
        self.value.resize(self.value.shape[0]+1, axis=0)
        self.value[-1] = v
        if self.own_step:
            self.step.resize(self.step.shape[0]+1, axis=0)
            self.step[-1] = step
            if self.time and len(self.time.shape)==1:
                self.time.resize(self.time.shape[0]+1, axis=0)
                self.time[-1] = time


def element(loc, name, **kwargs):
    store = kwargs.pop('store')
    if store=='fixed':
        return FixedElement(loc, name, **kwargs)
    data = kwargs.pop('data', None)
    if data is not None:
        if type(data) is not np.ndarray:
            data = np.asarray(data)
        kwargs['shape'] = (0,) + data.shape
        kwargs['maxshape'] = (None,) + data.shape
        kwargs['dtype'] = data.dtype
    if store=='linear':
        return LinearElement(loc, name, **kwargs)
    elif store=='time':
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
