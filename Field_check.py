import numpy as np
import matplotlib.pyplot as plt
import math
from BiotSavart_master import wire
from VacuumSeal import find_wires
from Analytic_dipole import analytic_dipole

# Define the R-Z plane at the chosen phi position    
disLen = 0.005 # m, length of current element  

x_min = 1
x_max = 3
z_min = -1
z_max = 1
nPts = 100
xObs = np.linspace(x_min, x_max, num=nPts)
zObs = np.linspace(z_min, z_max, num=nPts)

XObs, ZObs = np.meshgrid(xObs, zObs)
YObs = XObs * 0
CoordObs = np.dstack((XObs, YObs, ZObs))

iterCoord = CoordObs.reshape((-1,3))   
numCoords = np.shape(iterCoord)[0]  
bObs = np.zeros_like(iterCoord) 
bObs_a = np.zeros_like(iterCoord) 

fn = 'python_files/vesselRZv2In[1]'
rz = np.loadtxt(fn)
r = rz[:,0]
z = rz[:,1]
shift = 5e-3


inner_wire, outer_wire, inner_wire_fl, outer_wire_fl = find_wires(r, z, shift)

wires = [inner_wire, outer_wire]
disLen = 0.01
currents = [15e3, -15e3]
for i in range(2):
    thiswire = wire.Wire(path = wires[i], current = currents[i], discretization_length = disLen)  
    for k in range(numCoords):
        thisr = iterCoord[k,:]
        bObs[k,:] += thiswire.calculate_Field_Wire(thisr)  

for i in range(numCoords):
    thisr = iterCoord[i,:]
    bObs_a[i, 0:2] = analytic_dipole(thisr[0], thisr[1], 1.25, 0, 12.2, 1.2, 5e-3)

bObs = bObs.reshape((nPts,nPts,3))
bObs_a = bObs_a.reshape((nPts,nPts,3))

fig = plt.figure()
ax1 = plt.axes()
ax1.set_aspect('equal')
ax1.set_xlabel('R (m)')
ax1.set_ylabel('Z (m)')

c = ax1.contourf(XObs, ZObs, bObs[:,:,1], levels = np.linspace(1e-4, 10e-4, 20))
fig.colorbar(c, label = 'toroidal field (T)')
#ax1.contourf(XObs, YObs, bObs_a[:,:,0], bObs_a[:,:,1], scale = 25e-4, color = 'blue')

plt.show()

