#!/usr/bin/python3
# quick demo of matplotlib 3d visualisation

import mpl_toolkits.mplot3d as a3
import matplotlib.colors as colors
import pylab as pl
import numpy as np

ax = a3.Axes3D(pl.figure())
for i in range(10000):
    vtx = np.random.rand(3,3)
    tri = a3.art3d.Poly3DCollection([vtx])
    tri.set_color(colors.rgb2hex(np.random.rand(3)))
    tri.set_edgecolor('k')
    ax.add_collection3d(tri)
pl.show()
