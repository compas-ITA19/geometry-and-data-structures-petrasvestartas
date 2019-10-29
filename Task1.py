#Task get orthonormal vector  - do 2x cross-product.

from compas.geometry import Vector

u = Vector(1.1, 0.0, 0.0)
v = Vector(0.0, 1.05, 0.0)

uxv = u.cross(v)

#print(u.angle(v))
#print(v.angle(u))




def GetOrthonormalVectors(u,v):
    w = u.cross(v)
    v_ = u.cross(w)
    u_ = u

    u_.unitize()
    v_.unitize()
    w.unitize()

    return [u_,v_,w]

orthonormalV = GetOrthonormalVectors(u,v)

print( orthonormalV[0] )
print( orthonormalV[1] )
print( orthonormalV[2] )
print( orthonormalV[0].length )
print( orthonormalV[1].length )
print( orthonormalV[2].length )
