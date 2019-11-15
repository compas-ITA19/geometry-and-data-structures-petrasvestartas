#Generate over all
#And make offset

import os
import sys
from compas_fofin.datastructures import Cablenet
from compas_rhino.artists import MeshArtist
from compas.datastructures import Mesh
from compas.geometry import add_vectors
from compas.geometry import scale_vector
from compas.datastructures import mesh_flip_cycles
from compas.geometry import offset_polygon
from compas.geometry import Polygon
import json
HERE = os.path.dirname(__file__)

FILE_I = os.path.join(HERE, 'data', 'cablenet.json')

cablenet = Cablenet.from_json(FILE_I)

#FILE_O = os.path.join(HERE, 'data', 'blocks.json')

mesh_flip_cycles(cablenet)

# ==============================================================================
# Parameters
# ==============================================================================

OFFSET = 0.100

# ==============================================================================
# Make block
# ==============================================================================

blocks = []

for fkey in cablenet.faces():

    
    #fkey = cablenet.get_any_face()

    vertices = cablenet.face_vertices(fkey)
    points = cablenet.get_vertices_attributes('xyz',keys=vertices)
    normals = [cablenet.vertex_normal(key) for key in vertices]


    bottom = points[:]
    top = []
    for point, normal in zip(points,normals):
        xyz = add_vectors(point,scale_vector(normal,OFFSET))
        top.append(xyz)



    bottom = offset_polygon(bottom,0.01)
    top = offset_polygon(top,0.05)


    vertices = bottom+top
    faces = [ [0,3,2,1],[4,5,6,7],[3,0,4,7],[0,1,5,4],[1,2,6,5],[1,2,6,5],[2,3,7,6]]

    block = Mesh.from_vertices_and_faces(vertices,faces )
    blocks.append(block)



# ==============================================================================
# Visualize
# ==============================================================================




flag = False
for i in blocks:

    if(flag == False):
        flag = True
        artist = MeshArtist(i, layer="Boxes::Test")
        artist.clear_layer()
    else:
        artist = MeshArtist(i, layer="Boxes::Test")
        artist.draw_faces(join_faces=True,color=(0,255,255))
        #artist.draw_vertexlabels()


#Write Meshes To Json
# put all the mesh.data from all meshes in one dictionary
meshes_data = {}
for index, mesh in enumerate(blocks):
	meshes_data[index] = mesh.data

# save the dictionary to a json file
with open('blocks.json', 'w+') as fp:
	json.dump(meshes_data, fp, sort_keys=True, indent=4)