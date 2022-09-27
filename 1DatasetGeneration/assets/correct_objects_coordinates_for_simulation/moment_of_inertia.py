import numpy as np
import matplotlib.pyplot as plt
import sys

coords = np.loadtxt('c0_visual_135x140x140.txt', unpack=True, delimiter=',', dtype=int)
#coords[[1, 2]] = coords[[2, 1]]
coords = coords/max(coords.ravel())
x, y, z  = coords[0:3]

x_mean, y_mean = np.mean(x), np.mean(y)
z_mean = np.mean(z)
z_max = max(z)
P0 = x0, y0, z0 = x_mean, y_mean, z_max
#coords[0] = coords[0] - np.ones(coords[0].shape)*x_mean
#coords[1] = coords[1] - np.ones(coords[1].shape)*y_mean
#coords[2] = coords[2] - np.ones(coords[2].shape)*z_mean
#coords = coords.T - P0
#coords = coords.T
x, y, z = coords[0:3]

fig = plt.figure()
ax = fig.add_subplot(projection='3d')
ax.scatter(x,y,z)
ax.view_init(elev=20)
plt.show()

N = coords.shape[1]
Ix = sum(coords[1]**2 + coords[2]**2)/N
Iy = sum(coords[0]**2 + coords[2]**2)/N
Iz = sum(coords[0]**2 + coords[1]**2)/N
Ixy = sum(coords[0]*coords[1])/N
Iyz = sum(coords[1]*coords[2])/N
Ixz = sum(coords[0]*coords[2])/N


I = np.array([[Ix, Ixy, Ixz],[Ixy, Iy, Iyz],[Ixz, Iyz, Iz]])
print(I)

#
