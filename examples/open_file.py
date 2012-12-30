import numpy as np
import pyh5md

f = pyh5md.H5MD_File('poc.h5', 'r')

at = f.trajectory('atoms')

at_pos = at.data('position')

r = at_pos.v.value

print r

f.f.close()
