#Use the cross product to compute the area of a convex, 2D polygon
#Calculate the area of a convex 2D polygon
#Split a polygon into triangles within the center.


from compas.geometry import subtract_vectors
from compas.geometry import cross_vectors
from compas.geometry import length_vector
from compas.geometry import area_triangle
from compas.geometry import Vector
from compas.geometry import Polygon

myPolygon = Polygon([[0.0, 0.0, 0.0],[1.0, 0.0, 0.0],[0.0, 1.0, 0.0]])
myPolygon = Polygon([[-9.389057586,-32.9547945564,0],[-14.6396492493,-27.6499285715,0],[-12.7037845502,-21.1984902576,0],[-4.6363343871,-21.6574794887,0],[-0.9266189818,-25.981130889,0],[-3.2988089418,-30.8163579979,0]])

"""
ab = subtract_vectors(b, a)
ac = subtract_vectors(c, a)

L = length_vector(cross_vectors(ab, ac))
A = area_triangle([a, b, c])

print(0.5 * L == A)
"""



def GetConvexPolygonArea(polygon):

    center = [0.0,0.0,0.0]


    for p in polygon:
        center=[center[0]+p[0],center[1]+p[1],center[2]+p[2]]
   
    n = len(polygon.points)
    center=[center[0]/n,center[1]/n,center[2]/n]

    areaSum = 0.0



    for i in range(0, n):
        
        p0 = polygon[i]
        p1 = polygon[(i+1)%n]
        p2 = center
        u = subtract_vectors(p2,p1)
        v = subtract_vectors(p2,p0)
        area = length_vector(cross_vectors(u,v))*0.5
        areaSum+=area

    

    print(areaSum)

    return areaSum
 


        

 
   

GetConvexPolygonArea(myPolygon)
    
    
