#Using face.obj
# a - define a function for traversing the mesh from boundary to boundary in a "straight" line
# b - visualize the result

#first found boundaries that has two faces connected

import os
import compas

from compas.datastructures import Mesh
from compas.utilities import i_to_red
from compas_plotters import MeshPlotter
from compas_plotters import Plotter
from compas.geometry import Line


HERE = os.path.dirname(__file__)
DATA = os.path.join(HERE, 'data')
FILE = os.path.join(DATA, 'faces.obj')

mesh = Mesh.from_obj(FILE)




#First get the corner
edges0=[]
edges1=[]
startEdge = -1
v = -1
f = -1

#Find first starting corner
for key in mesh.edges_on_boundary(False):
    if(len(mesh.vertex_faces(key[0])) == 1 or len(mesh.vertex_faces(key[1])) == 1 ):
        startEdge = key
        if(len(mesh.vertex_faces(key[0])) == 1):
            v = key[0]
            f = mesh.vertex_faces(key[0])[0]

        if(len(mesh.vertex_faces(key[1])) == 1):
            v = key[1]
            f = mesh.vertex_faces(key[0])[0]
        break



#Find two borners
flag0 = 0
safety = 0
while(flag0 < 2):

    if(safety < 100):

        vnext = mesh.face_vertex_descendant(f,v)

        if(flag0==0):
            edges0.append((v,vnext))
        else:
            edges1.append((v,vnext))

        vnextnext = mesh.face_vertex_descendant(f,vnext)
        ef = mesh.edge_faces(vnext,vnextnext)
        
        id = 0
        if(ef[0] ==f ) : id = 1
        fnext = ef[id] 

        if(fnext == None):
             id=abs((id-1))
             flag0 +=1
        fnext = ef[id]
        
        #For Next iteration
        v= vnext 
        if(len(ef)==1): v= vnext 
        f = fnext
        if(len(ef)==1): f= f 

    safety+=1

        
  



def traverse(mesh, start):



    vertices=[start]
    edges=[]
    faces=[mesh.vertex_faces(vertices[0])[0]]

    flag = True
    i = 0

    while(flag):

   
            if(faces[i]==None):
                flag = False
                break

            vnext = mesh.face_vertex_descendant(faces[i], vertices[i])
            vnextnext = mesh.face_vertex_descendant(faces[i], vnext)

            fn = mesh.edge_faces(vnext, vnextnext)
            if faces[i] == fn[0]: fnext = fn[1]
            else : fnext = fn[0]

            vertices.append(vnext)
            edges.append((vertices[i], vnext))
            faces.append(fnext)
            i+=1

    return edges

plotter = Plotter(figsize=(16, 10))
lines = []
pts = []
def draw_edges_on_plotter(edges, color, width ):

    for i in edges:
        lines.append({'start': mesh.vertex_coordinates(i[0]), 'end': mesh.vertex_coordinates(i[1]), 'color': color,'width': width})
        pts.append({
        'pos': mesh.vertex_coordinates(i[0]), 
        'radius': 0.01, 
        'edgecolor': (255,0,0), 
        'facecolor': (255,255,0)})

all_edges = mesh.edges()
draw_edges_on_plotter(all_edges, (0, 0, 0),1)

#drawing mesh and line and traversing
counter = 0
for i in edges0:
    if(counter>0):
        traversedEdges = traverse(mesh,i[0])
        draw_edges_on_plotter(traversedEdges,(255,0,0),counter+2)
    counter+=1

counter = 0
for i in edges1:
    if(counter>0):
        traversedEdges = traverse(mesh,i[0])
        draw_edges_on_plotter(traversedEdges,(100,100,255),counter+2)
    counter+=1


#draw_edges_on_plotter(edges1, (0, 255, 0),2)
plotter.draw_points(pts)
plotter.draw_lines(lines)
plotter.show()
