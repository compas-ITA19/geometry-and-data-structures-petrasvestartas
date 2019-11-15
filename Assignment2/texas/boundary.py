import os
from compas_fofin.datastructures import Cablenet
from compas_rhino.artists import MeshArtist
from compas_rhino.artists import FrameArtist
from compas_rhino.artists import PointArtist
from compas.datastructures import Mesh
from compas.geometry import add_vectors
from compas.geometry import scale_vector
from compas.geometry import Frame
from compas.geometry import Point
from compas.geometry import Box
from compas.geometry import Transformation
from compas.geometry import transform_points
from compas.geometry import cross_vectors
from compas.geometry import subtract_vectors 
from compas.geometry import bounding_box_xy
from compas.geometry import Polygon
from compas.geometry import offset_polygon
from compas.geometry import intersection_line_plane
from compas.geometry import length_vector
from compas.geometry import Translation
from compas.geometry import normalize_vector
# ==============================================================================
# Create a proxy for PCA
# ==============================================================================

from compas.rpc import Proxy
numerical = Proxy('compas.numerical')
pca_numpy = numerical.pca_numpy

# ==============================================================================
# Construct a cablenet
# ==============================================================================

HERE = os.path.dirname(__file__)
FILE_I = os.path.join(HERE, 'data', 'cablenet.json')

cablenet = Cablenet.from_json(FILE_I)

# ==============================================================================
# Parameters
# ==============================================================================

OFFSET = 0.200
PADDING = 0.020




# ==============================================================================
# GET PCS around min 3 points
# ==============================================================================




def GetBoundingBox(pca_numpy, intersections, PADDING, start, end, frame):

    points = intersections[start:end]
    width = 0.1

    bbox = []


    if( (end-start ==2)):

        #print("2Points")
         
        vector = subtract_vectors(points[0],points[1])
        vector90 = cross_vectors(frame.zaxis,vector)
        
        X0 =  Translation(scale_vector([vector90[0],vector90[1],vector90[2]],width) )
        X1 =  Translation(scale_vector([vector90[0],vector90[1],vector90[2]],-width))

        pointsMoved0 = [points[0],points[1]]
        pointsMoved0 = transform_points(pointsMoved0,X0)
        pointsMoved1 = [points[0],points[1]]
        pointsMoved1 = transform_points(pointsMoved1,X1)

         


        bbox = [pointsMoved0[0],pointsMoved0[1],pointsMoved1[1],pointsMoved1[0]] 
        
        poly = Polygon(bbox)
        #print(poly)
        offset=offset_polygon(poly.points,-PADDING)
        X =  Translation((0,0,0) )
        
        bbox_= transform_points(offset, X)
       # bbox = bbox_   
        #print(bbox)
        #print(bbox_)


        frame_1 = Frame(points[0],vector, vector90)
        vectorLen =  length_vector(vector)
        vectorSmall = subtract_vectors(bbox[1],bbox[2])
        vectorLenSmall =  length_vector(vectorSmall)

    else:

        #print("N+2Points")

        origin, axes, values = pca_numpy([list(point) for point in points])
        frame_1 = Frame(origin,axes[0], axes[1])

        X = Transformation.from_frame_to_frame(frame_1,Frame.worldXY())

        points2 = transform_points(points, X)
        bbox = bounding_box_xy(points2)
        bbox = offset_polygon(bbox,-PADDING)
        bbox = transform_points(bbox, X.inverse())


        vector = subtract_vectors(bbox[0],bbox[1])
        vectorLen =  length_vector(vector)
        vectorSmall = subtract_vectors(bbox[1],bbox[2])
        vectorLenSmall =  length_vector(vectorSmall)
        
    #Unify box
    pt0 = Point(bbox[0][0],bbox[0][1],bbox[0][2])
    pt1 = Point(bbox[1][0],bbox[1][1],bbox[1][2])
    pt2 = Point(bbox[2][0],bbox[2][1],bbox[2][2])
    pt3 = Point(bbox[3][0],bbox[3][1],bbox[3][2])

    pt03 = Point((bbox[0][0]+bbox[3][0])*0.5,(bbox[0][1]+bbox[3][1])*0.5,(bbox[0][2]+bbox[3][2])*0.5)
    pt12 = Point((bbox[1][0]+bbox[2][0])*0.5,(bbox[1][1]+bbox[2][1])*0.5,(bbox[1][2]+bbox[2][2])*0.5)

    
    vectorSmall=normalize_vector(vectorSmall)

    X0 =  Translation(scale_vector(vectorSmall, width*0.5))
    X1 =  Translation(scale_vector(vectorSmall, -width*0.5))

    pt01 = transform_points([pt03,pt12],X0)
    pt23 = transform_points([pt03,pt12],X1)
    bbox[0] = pt01[0]
    bbox[1] = pt01[1]
    bbox[2] = pt23[1]
    bbox[3] = pt23[0]


        
       
    
    bbox = Mesh.from_vertices_and_faces(bbox,[[0,1,2,3]])
    
    return [frame_1,bbox,vectorLen,vectorLenSmall]


# ==============================================================================
# GET Plank Meshes
# ==============================================================================
allIntersections = []
def GetPlanks(name):

    # ==============================================================================
    # BGet Vertices on the boundary based on the name
    # ==============================================================================

    SOUTH = list(cablenet.vertices_where({'constraint':name}))
    boundary = list(cablenet.vertices_on_boundary(ordered=True))
    SOUTH[:] = [key for key in boundary if key in SOUTH]

    # ==============================================================================
    # Boundary plane
    # ==============================================================================

    a = cablenet.vertex_coordinates(SOUTH[0])
    b = cablenet.vertex_coordinates(SOUTH[-1])

    xaxis = subtract_vectors(b,a)
    yaxis = [0,0,1.0]
    zaxis = cross_vectors(xaxis,yaxis)
    xaxis = cross_vectors(yaxis,zaxis)

    frame = Frame(a,xaxis,yaxis)

    point =  add_vectors( frame.point, scale_vector(frame.zaxis,OFFSET))
    normal = frame.zaxis
    plane = point, normal

    # ==============================================================================
    # Intersections
    # ==============================================================================

    intersections = []
    for key in SOUTH:
        a = cablenet.vertex_coordinates(key)
        r = cablenet.residual(key)
        b = add_vectors(a,r)
        x,y,z = intersection_line_plane((a,b),plane)

        intersections.append(Point(x,y,z))

    # ==============================================================================
    # Bounding boxes
    # ==============================================================================






    limitLength = 2
    limitSmall = 0.12
    frame_box_len_All = []

    start = 0
    end =  start+2#len(intersections)

    #print("start " + str(start))

    
    while end <= len(intersections):
      
        

        frame_box_len = []
        flag = True
        while (flag and end <= len(intersections)):

            #print((str)(start) + " " + (str)(end))
            #print("number of points " + str(start) + "-" + str(end) )

            

            frame_box_lenTemp = GetBoundingBox(pca_numpy, intersections, PADDING, start,end,frame)

            numOfPts = end-start
            """
            if(numOfPts==2):
                end+=1
                continue
            """
            #if(numOfPts==2):
            """
            print(frame_box_lenTemp)
            frame_box_len = frame_box_lenTemp
            end+=1
            break
            """

            """
            if(frame_box_lenTemp[2]>limitLength):
                flag = False
                print("end" + str(end))
                break
            """
            #Check the widht of the plank
            #print(frame_box_lenTemp[2])
            if(frame_box_lenTemp[3]>limitSmall or frame_box_lenTemp[2]>limitLength):
                flag = False
                #print("end" + str(end))
                break
            
            """
            if(frame_box_lenTemp[3]>limitSmall and frame_box_lenTemp[2]>limitLength):
                flag = False
                print("end" + str(end))
                break
            """
            
            
            frame_box_len = frame_box_lenTemp
            end+=1


        start = end-2
        end = start+2
        frame_box_len_All.append(frame_box_len)
        #print("start " + str(start))

    

    return [frame_box_len_All,intersections]



# ==============================================================================
# Get both sides
# ==============================================================================

frame_box_len_All_=[]
ptlist = []

southSide = GetPlanks('SOUTH')[0]

for i in southSide:
    frame_box_len_All_.append(i)

southSide = GetPlanks('NORTH')[0]
for i in southSide:
    frame_box_len_All_.append(i)





# ==============================================================================
# Visualization
# ==============================================================================





flag = False
for i in frame_box_len_All_:

    if(flag == False):
        flag = True
        #artist = FrameArtist(frame, layer="SOUTH::Frame", scale=0.3)
        #artist.clear_layer()
        #artist.draw()

        artist = FrameArtist(i[0], layer="SOUTH::Frame1", scale=0.3)
        artist.clear_layer()
        artist.draw()
        artist = MeshArtist(i[1], layer="SOUTH::Bbox1")
        artist.clear_layer()
        artist.draw_mesh()
        
    else:
        #artist = FrameArtist(frame, layer="SOUTH::Frame", scale=0.3)
        #artist.draw()
        if(len(i)>2):
            artist = FrameArtist(i[0], layer="SOUTH::Frame1", scale=0.3)
            artist.draw()
            artist = MeshArtist(i[1], layer="SOUTH::Bbox1")
            artist.draw_mesh()
            #artist.draw_vertexlabels()

#PointArtist.draw_collection(allIntersections,layer="SOUTH::Intersection", clear=True)
