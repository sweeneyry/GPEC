import numpy as np
import pdb
import matplotlib.pyplot as plt

def unpack_string_float(string):

   elements = string.split()

   nn = len(elements)

   yy = np.zeros(nn)

   for ii in range(nn):
       yy[ii] = float(elements[ii])

   return yy

def unpack_string_int(string):

   elements = string.split()

   nn = len(elements)

   yy = np.zeros(nn, dtype=int)

   for ii in range(nn):
       yy[ii] = int(elements[ii])
   
   return yy


def plot_two_coils(aa):

   xstarts = aa['xstarts']
   zstarts = aa['zstarts']

   xends = aa['xends']
   zends = aa['zends']

   plt.plot(xstarts[0,0,0,:], zstarts[0,0,0,:], 'k-')
   plt.plot(  xends[0,0,0,:],   zends[0,0,0,:], 'k-')

   plt.plot(xstarts[0,0,1,:], zstarts[0,0,1,:], 'r-')
   plt.plot(  xends[0,0,1,:],   zends[0,0,1,:], 'r-')

   plt.show()
   
def read_sparc_coils(filename='wire_v1e_toroidal_a1_wires.txt'):
    """
    Usage:  aa = read_sparc_coils(filename)

    aa is a dictionary containing:

        ncoil     number of TF coils.  each TF coil is represented
                  by npancake x nradial loops. The pancakes
                  are separated toroidally and the other loops
                  are separated radiall.
        npancake  
        nradial
        nwire     number of wires in each loop

        xstarts[ncoil, npancake, nradial]  x-starting positions of straight wires
        ystarts[ncoil, npancake, nradial]  y-starting positions of straight wires
        zstarts[ncoil, npancake, nradial]  z-starting positions of straight wires

        xends[ncoil, npancake, nradial]  x-ending positions of straight wires
        yends[ncoil, npancake, nradial]  y-ending positions of straight wires
        zends[ncoil, npancake, nradial]  z-ending positions of straight wires

        currents[ncoil, npancake, nradial] current in each loop

    """
    ff = open(filename, "r")
    
    line = ff.readline()
    aa   = unpack_string_int(line)

    ncoil    = aa[0]
    npancake = aa[1]
    nradial  = aa[2]
    nwire    = aa[3]

    xstarts = np.zeros((ncoil, npancake, nradial, nwire))
    ystarts = np.zeros((ncoil, npancake, nradial, nwire))
    zstarts = np.zeros((ncoil, npancake, nradial, nwire))

    xends = np.zeros((ncoil, npancake, nradial, nwire))
    yends = np.zeros((ncoil, npancake, nradial, nwire))
    zends = np.zeros((ncoil, npancake, nradial, nwire))

    coil_currents = np.zeros((ncoil, npancake, nradial))
    
    for iradial in range(nradial):

       line    = ff.readline()
       iradial = unpack_string_int(line)

       for ic in range(ncoil):
          for jp in range(npancake):

             line = ff.readline()
             aa   = unpack_string_int(line)
             
             icoil    = aa[0]
             ipancake = aa[1]

             line = ff.readline()
             coil_currents[icoil, ipancake, iradial] = unpack_string_float(line)
             
             for iw in range(nwire):

                line = ff.readline()
                aa   = unpack_string_float(line)

                xstarts[icoil, ipancake, iradial, iw] = aa[0]
                ystarts[icoil, ipancake, iradial, iw] = aa[1]
                zstarts[icoil, ipancake, iradial, iw] = aa[2]

                xends[icoil, ipancake, iradial, iw] = aa[3]
                yends[icoil, ipancake, iradial, iw] = aa[4]
                zends[icoil, ipancake, iradial, iw] = aa[5]

    aa_out = {}
    
    aa_out["ncoil"]    = ncoil
    aa_out["npancake"] = npancake
    aa_out["nradial"]  = nradial
    aa_out["nwire"]    = nwire

    aa_out["xstarts"]  = xstarts
    aa_out["ystarts"]  = ystarts
    aa_out["zstarts"]  = zstarts
    
    aa_out["xends"]    = xends
    aa_out["yends"]    = yends
    aa_out["zends"]    = zends
    
    aa_out["coil_currents"] = coil_currents
    
    return aa_out
