#Define a function for computing the cross products of two arrays of vectors
# a the input arrays have the same length (same number of vectors)
# prototype in a pure python (loop over the arrays)
# make numpy equivalent without loops
from compas.geometry import Vector
import numpy as np


array1 = [[5,0,1], [2,4,5], [3,0,5], [5,4,4], [2,4,5], [3,0,5], [5,4,4]]
array2 = [[5,0,7], [2,7,7], [-3,0,-5], [-4,-4,0], [-3,0,-5], [-4,-4,0], [-4,-4,0]]



#array of vector or lists of vectors

def arrays_cross(array1, array2):

    cross_list = []

    for i in range(len(array1)):

        u = Vector(array1[i][0], array1[i][1], array1[i][2])
        v = Vector(array2[i][0], array2[i][1], array2[i][2])
        cross_list.append(u.cross(v))

    return cross_list




print(arrays_cross(array1, array2))

    
# numpy
array1 = np.array(array1)
array2 = np.array(array2)

print(np.cross(array1, array2))