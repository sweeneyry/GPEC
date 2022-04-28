import numpy as np
import matplotlib.pyplot as plt
import math
from BiotSavart_master import wire
from VacuumSeal import find_wires
from Analytic_dipole import analytic_dipole

# Define the R-Z plane at the chosen phi position    
disLen = 0.005 # m, length of current element  

x_min = 0.8
x_max = 1.5 
y_min = 0.3
y_max = 0.7
nPts = 10
xObs = np.linspace(x_min, x_max, num=nPts)
yObs = np.linspace(y_min, y_max, num=nPts)

XObs, YObs = np.meshgrid(xObs, yObs)
ZObs = XObs * 0
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
currents = [-1.5e4, 1.5e4]
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
ax1.set_ylabel('$R\phi$ (m)')
ax1.quiver(XObs, YObs, bObs[:,:,0], bObs[:,:,1], scale = 25e-4)
ax1.quiver(XObs, YObs, bObs_a[:,:,0], bObs_a[:,:,1], scale = 25e-4, color = 'blue')

# print(np.sqrt(bObs[:,:,0]**2 + bObs[:,:,1]**2))
# print()
# print(np.sqrt(bObs_a[:,:,0]**2 + bObs_a[:,:,1]**2))

plt.show()

