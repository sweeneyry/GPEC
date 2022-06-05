#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue May 31 06:43:29 2022

@author: ryansweeney
"""

from write_GPEC_File import write_GPEC_File
import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
from read_sparc_coils_v3 import read_sparc_coils
from pathlib import Path

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
ax.set_ylabel('Y (m)')  
ax.set_zlabel('Z (m)')  

# read in the python dictionary produced from Steve's text file
filename = Path(__file__).parent / 'v1ecoils_curmult_single_005_coils.txt'
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


h = 1.5 ##Height shift 

tfPList = []

for i in range(0,ncoil):
    for j in range(0, npancake):
        for k in range(0,nradial):
            
            if i <= 8:
                x = xcrds[i,j,k,:] 
                y = ycrds[i,j,k,:]
                z = zcrds[i,j,k,:]
                
            if i > 8:
                 x = xcrds[i,j,k,:] 
                 y = ycrds[i,j,k,:]
                 z = zcrds[i,j,k,:] + h
            
            if Plot:
                ax.plot(x,y,z, 'b')
            
            path = np.array([np.squeeze(x), np.squeeze(y), np.squeeze(z)])
            tfPList.append(path)

fname = 'TFvs' + str(h) + '.dat'

write_GPEC_File('C:/Users/Rubie0/OneDrive/MIT 2022/Urop PSFC/Gpec/' 
                + 'sparc_' + fname, tfPList, Transpose=1)
