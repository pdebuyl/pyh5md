
import numpy as np
import h5py
import time

TRAJECTORY_NAMES = ['position', 'velocity', 'force', 'species']

def populate_H5MD_data(g, name, shape, dtype):
    """Creates a step,time,value H5MD data group."""
    g.s = g.create_dataset('step', shape=(0,), dtype=np.int32, maxshape=(None,))
    g.t = g.create_dataset('time', shape=(0,), dtype=np.float64, maxshape=(None,))
    g.v = g.create_dataset('value', shape=(0,)+shape, dtype=dtype, maxshape=(None,)+shape)

class Trajectory(h5py.Group):
    """Represents a trajectory group within a H5MD file."""
    def __init__(self, parent, name, shape, dtype):
        """Create a new Trajectory object."""
        if name in TRAJECTORY_NAMES:
            self._id = h5py.h5g.create(parent.id, name)
            populate_H5MD_data(self,name,shape, dtype)
        else:
            raise Exception('Name not in TRAJECTORY_NAMES')
    def append(self, data, step, time):
        """Appends a time slice to the data group."""
        s = self['step']
        t = self['time']
        v = self['value']
        assert s.shape[0]==t.shape[0] and t.shape[0]==v.shape[0]
        if data.shape==v.shape[1:] and data.dtype==v.dtype:
            idx = v.shape[0]
            v.resize(idx+1,axis=0)
            v[-1] = data
            s.resize(idx+1, axis=0)
            s[-1] = step
            t.resize(idx+1, axis=0)
            t[-1] = time
            

class TrajectoryGroup(h5py.Group):
    """Represents the root trajectory group within a H5MD file."""
    def __init__(self, parent, name):
        """Create a new TrajectoryGroup object."""
        if 'trajectory' not in parent.keys():
            parent.create_group('trajectory')
        t = parent['trajectory']
        if name in t.keys():
            self._id = h5py.h5g.open(t.id, name)
        else:
            self._id = h5py.h5g.create(t.id, name)
    def add_data(self, name, shape, dtype):
        return Trajectory(self, name, shape, dtype)

class H5MD_File(object):
    """Class to create and read H5MD compliant files."""
    def __init__(self,filename,mode,**kwargs):
        """Create or read an H5MD file, according to argument mode.
        mode should be 'r', 'r+' or 'w'"""
        if mode not in ['r','r+','w']:
            print 'Unknown mode in H5MDFile'
            return
        if mode=='w':
            kw = kwargs.keys()
            for key in ['creator', 'author', 'creator_version']:
                if key not in kw:
                    print 'missing arguments in H5MDFile'
                    return
        self.f = h5py.File(filename, mode)
        if mode=='w':
            self.f.create_group('h5md')
            for key in ['creator', 'author', 'creator_version']:
                self.f['h5md'].attrs[key] = kwargs[key]
            self.f['h5md'].attrs['version'] = np.array([1,0])
            self.f['h5md'].attrs['creation_time'] = int(time.time())

    def trajectory(self, group_name):
        """Adds or open a group in /trajectory. If /trajectory does not exist,
        it will be created."""
        return TrajectoryGroup(self.f, group_name)


    
            
        
