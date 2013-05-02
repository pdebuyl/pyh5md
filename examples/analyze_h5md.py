
import numpy as np
import pyh5md
import matplotlib.pyplot as plt

f = pyh5md.H5MD_File('particles_3d.h5', 'r')
com = f.observable('center_of_mass')
plt.plot(com.t, com.v)
plt.show()
