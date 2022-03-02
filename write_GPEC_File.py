#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue May 26 22:59:59 2020

@author: Ryan
"""


import numpy as np
import pdb
import os.path


def write_GPEC_File(filename, listCoilPaths, Transpose=0):
    '''
    Email from N. Logan 5/26/20
    
    First line: ncoil, s, nsec, nw in the fortran format '(3(1x,I4),1x,f7.2)' 
    (i.e. three 4 character wide integers and a 7 character wide float, all separated by one space). 
    Here, ncoil is the number of distinct coils (like 6 for the DIII-D c-coils, probably just 1 for 
    your spirals unless you want to separate them for a phasing scan). The s is the number of 
    "sections" per coil, which I think we used for the TBM since there were clearly distinct parts 
    but all of them were always wired in series (s=1 for every other case I know of).  The nsec is 
    the number of points in your coil. Finally, nw is the number of "windings" and is just a simple 
    multiplier of the vacuum calculation (for example, we represent the C coils as one winding and have nw=-4.0).

    Rest: 3 columns of x, y, z in the fortran format '(3(1x,e12.4))'
    
    
    '''
    
    
    # check the filename
    fnsplit = os.path.split(filename)
    fname = fnsplit[1]
    fpath = fnsplit[0]
    if fname[0:6] != 'sparc_':
        print('This filename does not start with sparc_')
        print('Type "cont" to append sparc_, or "exit" to stop')
        pdb.set_trace()
        filename = fpath + '/sparc_' + fname
    
    numPts = 0
    
    with open(filename, 'w') as f:
    
        numCoils = len(listCoilPaths)
        print('numCoils ', numCoils)
        
        for j in range(0, numCoils):
            
            coilPath = listCoilPaths[j]
            
            if Transpose:
                coilPath = coilPath.T            

            numPts = np.shape(coilPath)[0]
        
            if j == 0:
                           
                # file header
                # 
                spaceNumCoils = '    '
                spaceNumPts = ' '
                
                if numCoils >= 10:
                    spaceNumCoils = '   '
                if numCoils >= 100:
                    spaceNumCoils = '  '
                    
                if numPts < 1000:
                    spaceNumPts = '  '
                if numPts < 100:
                    spaceNumPts = '   '
                
                f.write(spaceNumCoils + str(numCoils) + '    1' + spaceNumPts +  str(numPts) + ' 1.00000\n') 
            
            for i in range(0,numPts):
            
                
                f.write("%12.4e %12.4e %12.4e\n" % (coilPath[i,0], coilPath[i,1], coilPath[i,2]))