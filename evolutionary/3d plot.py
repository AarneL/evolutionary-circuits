'''
======================
3D surface (color map)
======================

Demonstrates plotting a 3D surface colored with the coolwarm color map.
The surface is made opaque by using antialiased=False.

Also demonstrates using the LinearLocator and custom formatting for the
z axis tick labels.
'''

from mpl_toolkits.mplot3d import Axes3D
import matplotlib.pyplot as plt
from matplotlib import cm
from matplotlib.ticker import LinearLocator, FormatStrFormatter
import numpy as np
import pandas as pd
from scipy.interpolate import griddata

values = []
R1s = []
R2s = []
with open('Results.txt','r') as myFile:
    for line in myFile:
        parts = line.split(':')
        values.append(float(parts[0]))
        R1s.append(float(parts[1]))
        R2s.append(float(parts[2]))

values = np.array(values)
R1s = np.array(R1s)
R2s = np.array(R2s)
xyz = {'x': R1s, 'y': R2s, 'z': values}
df = pd.DataFrame(xyz, index=range(len(xyz['x']))) 
x1 = np.linspace(df['x'].min(), df['x'].max(), len(df['x'].unique()))
y1 = np.linspace(df['y'].min(), df['y'].max(), len(df['y'].unique()))
x2, y2 = np.meshgrid(x1, y1)
z2 = griddata((df['x'], df['y']), df['z'], (x2, y2), method='cubic')

fig = plt.figure()
ax = fig.gca(projection='3d')
surf = ax.plot_surface(x2, y2, z2, rstride=1, cstride=1, cmap=cm.coolwarm,
    linewidth=0, antialiased=False)
ax.set_zlim(1000, 1100)

ax.zaxis.set_major_locator(LinearLocator(10))
ax.zaxis.set_major_formatter(FormatStrFormatter('%.02f'))
m = cm.ScalarMappable(cmap=surf.cmap, norm=surf.norm)
m.set_array(z2)
fig.colorbar(m)
plt.title('Meshgrid Created from 3 1D Arrays')


plt.show()

