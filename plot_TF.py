#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue May 31 06:43:29 2022

@author: ryansweeney
"""


import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
from SPARC.Errors.read_sparc_coils_v3 import read_sparc_coils

'''
Read in the files produced by Steve and convert to the GPEC format.
'''

Plot=True
fig = plt.figure()
ax = plt.subplot(1,1,1,projection='3d')
ax.set_xlim([-3,3])
ax.set_ylim([-3,3])
ax.set_zlim([-3,3])
ax.set_xlabel('X (m)')
ax.set_xlabel('Y (m)')
ax.set_xlabel('Z (m)')

# read in the python dictionary produced from Steve's text file
filename = '/Users/ryansweeney/Google_Drive/Work/Python/SPARC/Errors/TF/aug28/v1ecoils_curmult_single_005_coils.txt'
fname = 'tfv1es5mm.dat'
aa_out = read_sparc_coils(filename)


ncoil = aa_out["ncoil"]  
npancake = aa_out["npancake"] 
nradial = aa_out["nradial"] 
nwire = aa_out["nwire"] 

xstarts = aa_out["xstarts"] 
ystarts = aa_out["ystarts"]
zstarts = aa_out["zstarts"]

xends = aa_out["xends"]
yends = aa_out["yends"] 
zends = aa_out["zends"]    


xcrds = np.concatenate((xstarts, np.expand_dims(xends[:,:,:,-1], axis=3)), axis=3)
ycrds = np.concatenate((ystarts, np.expand_dims(yends[:,:,:,-1], axis=3)), axis=3)
zcrds = np.concatenate((zstarts, np.expand_dims(zends[:,:,:,-1], axis=3)), axis=3)
# ------------------------------------------------------------------




tfPList = []

for i in range(0,ncoil):
    for j in range(0, npancake):
        for k in range(0,nradial):
            
            
            x = xcrds[i,j,k,:] 
            y = ycrds[i,j,k,:]
            z = zcrds[i,j,k,:]
            
            if Plot:
                ax.plot(x,y,z, 'b')
            
            path = np.array([np.squeeze(x), np.squeeze(y), np.squeeze(z)])
            tfPList.append(path)