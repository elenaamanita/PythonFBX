import FbxCommon
import fbx
import math
import sys
import webbrowser
import glob, os
from xml.etree import ElementTree as et

# global variables
filenames = []
filenum = 0
edges = []
depth = []
vertices = []
xPoints = []
yPoints = []
zPoints = []
centerX = 0
centerY = 0 
centerZ = 0
minX = 0 
minY = 0 
maxX = 0
maxY = 0
triangualtedMesh = fbx.FbxMesh

sdk_manager, scene = FbxCommon.InitializeSdkObjects()
converter = fbx.FbxGeometryConverter(sdk_manager)

path = os.getcwd()
newpath=path+"\Fbx Files"
print(newpath)

os.chdir(newpath)
for file in glob.glob("*.fbx"):
    filenames.append(file)

filenum = len(filenames)
doc = et.Element('svg', width='480', height='480', version='1.1', xmlns='http://www.w3.org/2000/svg', viewBox = '0,0,0,0', preserveAspectRatio = 'xMidYMid meet', onload='init(evt)'+'\n')
#script = et.SubElement(doc,'script', type='text/ecmascript')

#data = '![CDATA[\n'
doc.text=("\n")
#script.text =("\n")
def clamp(x): 
    return max(0, min(x, 255))

def calculatedepth():
    facesDepth = len(vertices)
    for i in range(facesDepth):
        currentDepth = 0
        for j in range(len(vertices[i])):
            currentDepth += zPoints[vertices[i][j]]
        currentDepth /= len(vertices[i])
        facesDepth[i] = currentDepth

    for i in range(len(depth)):
        smallest = -1
        for j in range(facesDepth):
            if facesDepth[j] != -99999 and (smallest ==-1 or facesDepth[smallest] > facesDepth[j]):
                smallest = j
        depth[i] = smallest
        facesDepth[smallest] = -99999

def rotateX(rads):
    for i in range(len(xPoints)):
        y = yPoints[i] - centerY
        z = zPoints[i] - centerZ
        d = math.sqrt(y*y + z*z)
        theta = math.atan2(y,z) + rads
        yPoints[i] = centerY + d + math.sin(theta)
        zPoints[i] = centerZ + d + math.sin(theta)

def rotateY(rads):
    for i in range(len(xPoints)):
        x = xPoints[i] - centerX
        z = zPoints[i] - centerZ
        d = math.sqrt(x*x + z*z)
        theta = math.atan2(x,z) + rads
        xPoints[i] = centerX + d + math.sin(theta)
        zPoints[i] = centerZ + d + math.sin(theta)

def rotateZ(rads):
    for i in range(len(xPoints)):
        y = yPoints[i] - centerY
        x = zPoints[i] - centerX
        d = math.sqrt(x*x + y*y)
        theta = math.atan2(x,y) + rads
        yPoints[i] = centerY + d + math.sin(theta)
        xPoints[i] = centerX + d + math.sin(theta)

def getInfo():
    for file in range(filenum):
        if not FbxCommon.LoadScene(sdk_manager, scene, filenames[file]):
            print("Not found")

        rotation =  180
        rotation = rotation * 3.1415926 / 180

        node = scene.GetRootNode()
        for i in range(node.GetChildCount()):
            child = node.GetChild(i)
            attr_type = child.GetNodeAttribute().GetAttributeType()
            edges = []
            vertices = []
            if attr_type==FbxCommon.FbxNodeAttribute.eMesh:          
                mesh = child.GetNodeAttribute()
                if not mesh.GetNode().GetMesh().IsTriangleMesh():
                    triangulateMesh=converter.Triangulate(mesh,False)
                    print("Triangulated")
                edgecount = triangulateMesh.GetNode().GetMesh().GetMeshEdgeCount()
                polygoncount = triangulateMesh.GetNode().GetMesh().GetPolygonCount()
                #contents = "edges = ["
                for edge in range(edgecount):
                    start, end = triangulateMesh.GetNode().GetMesh().GetMeshEdgeVertices(edge)
                    #contents += "[" + str(start) + "," + str(end) + "],"
                    edges.append([start,end])
                #contents = contents[:-1] +"]\n"
                #contents += "faces = ["
                for polygon in range(polygoncount):
                    #contents += "["
                    vertices.append([triangulateMesh.GetNode().GetMesh().GetPolygonVertex(polygon,0),triangulateMesh.GetNode().GetMesh().GetPolygonVertex(polygon,1),triangulateMesh.GetNode().GetMesh().GetPolygonVertex(polygon,2)])
                #    for size in range(triangulateMesh.GetNode().GetMesh().GetPolygonSize(polygon)):
                #        contents +=str(triangulateMesh.GetNode().GetMesh().GetPolygonVertex(polygon,size))+","
                #    contents = contents[:-1] +"],"
                #contents = contents[:-1] + "]\n"

                #contents += "depth =["
                depth = []
                for polygon in range(triangulateMesh.GetNode().GetMesh().GetPolygonCount()):
                    depth.append(0)
                #    contents += "0,"
                #contents = contents[:-1] + "]\n"

                xPoints = []
                yPoints = []
                zPoints = []
                smallestControlPointX = 0
                smallestControlPointY = 0
                smallestControlPointZ = 0
                for point in range(triangulateMesh.GetNode().GetMesh().GetControlPointsCount()):
                    if(smallestControlPointX > triangulateMesh.GetNode().GetMesh().GetControlPoints()[point][0]):
                        smallestControlPointX = triangulateMesh.GetNode().GetMesh().GetControlPoints()[point][0]
                        if(smallestControlPointY > triangulateMesh.GetNode().GetMesh().GetControlPoints()[point][1]):
                            smallestControlPointY = triangulateMesh.GetNode().GetMesh().GetControlPoints()[point][1]
                            if(smallestControlPointZ > triangulateMesh.GetNode().GetMesh().GetControlPoints()[point][2]):
                                smallestControlPointZ = triangulateMesh.GetNode().GetMesh().GetControlPoints()[point][2]

                for point in range(triangulateMesh.GetNode().GetMesh().GetControlPointsCount()):
                    xPoints.append(triangulateMesh.GetNode().GetMesh().GetControlPoints()[point][0] - smallestControlPointX)
                    yPoints.append(triangulateMesh.GetNode().GetMesh().GetControlPoints()[point][1] - smallestControlPointY)
                    zPoints.append(triangulateMesh.GetNode().GetMesh().GetControlPoints()[point][2] - smallestControlPointZ)

                centerX = -smallestControlPointX
                centerY = -smallestControlPointY
                centerZ = -smallestControlPointZ

                minX = -999
                minY = -999
                maxX = -999
                maxY = -999

                rotateX(rotation)
                rotateY(rotation)
                rotateZ(rotation)
                calculatedepth()

                #xPoints = xPoints[:-1] +"];\n"
                #yPoints = yPoints[:-1] +"];\n"
                #zPoints = zPoints[:-1] +"];\n"
                #contents = xPoints + yPoints + zPoints
                #data += contents
                #data += ']]'
                #cdata = et.SubElement(script, data)
                for polygon in range (triangulateMesh.GetNode().GetMesh().GetPolygonCount()):
                    poly = FbxCommon.FbxPropertyDouble3(triangulateMesh.GetNode().GetMesh().FindProperty("Color")).Get()
                    r = clamp(poly[0] * 255 - poly[0] * 0.4 * ((polygon+0.0) / child.GetMesh().GetPolygonCount()) * 255)
                    g = clamp(poly[1] * 255 - poly[1] * 0.4 * ((polygon+0.0) / child.GetMesh().GetPolygonCount()) * 255)
                    b = clamp(poly[2] * 255 - poly[2] * 0.4 * ((polygon+0.0) / child.GetMesh().GetPolygonCount()) * 255)
                    thisPath = 'M'+str(xPoints[vertices[polygon][0]]*8)+' '+str(yPoints[vertices[polygon][0]]*8)
                    for j in range(1, len(vertices[depth[polygon]])):
                        thisPath += ' ' + 'L'+str(xPoints[vertices[polygon][j]]*8) + ' ' + str(yPoints[vertices[polygon][j]]*8)
                    thisPath += ' Z'
                    svgPath = et.SubElement(doc, 'path', stroke = str('#%02x%02x%02x' % (r,g,b)), fill = str('#%02x%02x%02x' % (r,g,b)), id = "face-"+str(polygon), d = thisPath)
                    svgPath.text = "\n"
            
                #    vert = triangulateMesh.GetNode().GetMesh().GetPolygonVertex(i, j)
                #    vertexData = triangulateMesh.GetNode().GetMesh().GetControlPointAt(vert)
                #    vertx = vertexData[0]
                #    verty = vertexData[1]
                #    vertz = vertexData[2]
                #    x0 = vertx
                #    y0 = verty*math.cos(math.radians(0)) + vertz*math.sin(math.radians(0))
                #    z0 = vertz*math.cos(math.radians(0)) - verty*math.sin(math.radians(0))
                #    x1 = x0*math.cos(math.radians(45)) - z0*math.sin(math.radians(45))
                #    y1 = y0
                #    z1 = z0*math.cos(math.radians(45)) + x0*math.sin(math.radians(45))
                #    x2 = x1*math.cos(math.radians(0)) + y1*math.sin(math.radians(0))
                #    y2 = y1*math.cos(math.radians(0)) - x1*math.sin(math.radians(0))
                #    y2 = y2 * -1
                #    vertices.append([x2,y2])
                #point1 = vertices[0][0] * 8
                #point2 = vertices[0][1] * 8
                #point3 = vertices[1][0] * 8
                #point4 = vertices[1][1] * 8
                #point5 = vertices[2][0] * 8
                #point6 = vertices[2][1] * 8
                #point1 += 250
                #point2 += 250
                #point3 += 250
                #point4 += 250
                #point5 += 250
                #point6 += 250
                #string = str(point1) + (',') + str(point2) + (' ') + str(point3) + (',') + str(point4) + (' ') + str(point5) + (',') + str(point6)
                #polyline = et.SubElement(doc, 'polyline', points = string, stroke='lightblue', fill='blue')
                #polyline.text ="\n"

def init():
    getInfo()

init()
os.chdir(path)
f = open('sample.svg', 'w')
f.write('<?xml version=\"1.0\" standalone=\"no\"?>\n')
f.write('<!DOCTYPE svg PUBLIC \"-//W3C//DTD SVG 1.1//EN\"\n')
f.write('\"http://www.w3.org/Graphics/SVG/1.1/DTD/svg11.dtd\">\n')
f.write(et.tostring(doc))
f.close()

r = open('sample.svg', 'r')
filedata = r.read()
r.close()

newdata = filedata.replace("] />", "]>")

f = open('sample.svg', 'w')
f.write(newdata)
f.close()

f = open('index.html', 'w')
message = """<html>

<head><title> FBX Viewer </title></head>
<body><p>This is my FBX viewer!</p><object data="sample.svg" type="image/svg+xml"></object></body>

</html>"""

f.write(message)
f.close()

webbrowser.open_new_tab('index.html')