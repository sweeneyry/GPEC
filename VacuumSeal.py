from cgitb import reset
import numpy as np
import matplotlib.pyplot as plt
import math
import pdb
from BiotSavart_master import wire
from write_GPEC_File import *

def find_segments(x_values, y_values):
    length = len(x_values)
    result = []    # slope, intercept

    for i in range(-1, length - 1):
        x = [x_values[i], x_values[i+1]]
        y = [y_values[i], y_values[i+1]]

        if x[1] == x[0]:
            m = math.inf
            b = x[0]             # document the x intercept
        else:
            m = (y[1] - y[0])/(x[1] - x[0])
            b = y[0] - m*x[0]
        
        result.append([m, b])

    return result

        
# if shift is positive, shift in
# if shift is negative, shift out
def move_segments(segments, shift):
    result = []

    for i in range(len(segments)):
        m = segments[i][0]
        b = segments[i][1]
        theta = np.arctan(m)

        # i love hardcoding
        if i in range(0, 4) or i in range(22, 25):
            b += shift
        elif i in range(4, 7):
            b -= shift/(np.cos(theta))
        elif i in range(7, 9):
            b -= shift
        elif i == 9:
            b -= shift/(np.cos(theta))
        elif i == 10:
            b -= shift
        elif i == 11:
            b -= shift/(np.cos(theta))
        elif i in range(12, 14):
            b -= shift
        elif i == 14:
            b += shift/(np.cos(theta))
        elif i == 15:
            b += shift
        elif i == 16:
            b += shift/(np.cos(theta))
        elif i in range(17, 19):
            b -= shift
        elif i in range(19, 22):
            b += shift/(np.cos(theta))
        
        result.append([m, b])

    # remove duplicates
    res = []
    [res.append(x) for x in result if x not in res]

    return res

def find_points(segments):
    x_values, y_values = [],[]

    for i in range(-1, len(segments) - 1):
        m1 = segments[i][0]
        b1 = segments[i][1]
        m2 = segments[i+1][0]
        b2 = segments[i+1][1]

        if m1 == math.inf:
            x = b1
            y = m2 * b1 + b2
        elif m2 == math.inf:
            x = b2
            y = m1 * b2 + b1
        else:
            x = (b2 - b1)/(m1 - m2)
            y = m1* x + b1
    
        x_values.append(x)
        y_values.append(y)


    
    return x_values, y_values
    
def reflect(r, z):
    pos_r, pos_z = [], []
    for i in range(len(z)):
        if z[i] > 0:
            pos_r.append(r[i])
            pos_z.append(z[i])
    
    ref_z = [-1* j for j in pos_z]  # reflection
    ref_z = ref_z[::-1]   # reverse the positive list

    pos_z += ref_z
    pos_r += pos_r[::-1]

    return pos_r, pos_z

def find_wires(r, z, shift):
    segments = find_segments(r, z)
    inner_segments = move_segments(segments, shift)
    outer_segments = move_segments(segments, -1*shift)

    inner_r, inner_z = reflect(find_points(inner_segments)[0], find_points(inner_segments)[1])
    inner_r.append(inner_r[0])
    inner_z.append(inner_z[0])

    outer_r, outer_z = reflect(find_points(outer_segments)[0], find_points(outer_segments)[1])
    outer_r.append(outer_r[0])
    outer_z.append(outer_z[0])

    length = len(inner_r)
    inner_wire = np.column_stack((inner_r, [0]*length, inner_z))
    outer_wire = np.column_stack((outer_r, [0]*length, outer_z))

    inner_wire_fl = np.column_stack(([element * -1 for element in inner_r], [0]*length, inner_z))
    outer_wire_fl = np.column_stack(([element * -1 for element in outer_r], [0]*length, outer_z))

    inner_wire = wire.Wire(path = inner_wire).discretized_path()
    outer_wire = wire.Wire(path = outer_wire).discretized_path()
    inner_wire_fl = wire.Wire(path = inner_wire_fl).discretized_path()
    outer_wire_fl = wire.Wire(path = outer_wire_fl).discretized_path()

    return inner_wire, outer_wire, inner_wire_fl, outer_wire_fl

fn = 'python_files/vesselRZv2In[1]'
rz = np.loadtxt(fn)
r = rz[:,0]
z = rz[:,1]
shift = 5e-3

inner_wire, outer_wire, inner_wire_fl, outer_wire_fl = find_wires(r, z, shift)

ax = plt.axes()
ax.plot(r, z)

ax.set_xlabel('R (m)')
ax.set_ylabel('Z (m)')
ax.plot(inner_wire[:,0], inner_wire[:,2])
ax.plot(outer_wire[:,0], outer_wire[:,2])
ax.plot(inner_wire_fl[:,0], inner_wire_fl[:,2])
ax.plot(outer_wire_fl[:,0], outer_wire_fl[:,2])

ax.set_aspect('equal')
plt.show()

# new_file = "GPEC_Files\sparc_VV_weld.dat"
# write_GPEC_File(new_file, [inner_wire, outer_wire])

# new_file = "GPEC_Files\sparc_VV_weld_fl.dat"
# write_GPEC_File(new_file, [inner_wire, outer_wire, inner_wire_fl, outer_wire_fl])

write_GPEC_File("GPEC_Files\sparc_i_VV_weld.dat", [inner_wire])
write_GPEC_File("GPEC_Files\sparc_o_VV_weld.dat", [outer_wire])
write_GPEC_File("GPEC_Files\sparc_i_VV_weld_fl.dat", [inner_wire_fl])
write_GPEC_File("GPEC_Files\sparc_o_VV_weld_fl.dat", [outer_wire_fl])