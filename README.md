
#Tools and middleware project

In this project we were assigned to try and use the coding language python to load up a web server and use it to convert and display an FBX image on the web server site. 
In this project we were in a group of three, Michael Craddock, Baggio Pereira and Eleni Paskali. To begin this project the first thing we looked up was setting up a server. We initially looked at using something along the lines of Amazon or google to host the service but we ended up choosing to host it locally so that we didn’t have to spend money on hosting costs and due to time constraints we never managed to switch over to using a proper online server.
Some initial testing was done early on trying to connect to Amazons service however at the time it proved tricky and to get the project moving we switched over to using a local hosted server so we could get something down. The server script does two assignments. The first is to host the directory, and the other is to run the main script (PythonFBX) which then creates the SVG file used and updates the HTML.
After creating a blank local hosted web page we began to work on creating different types of FBX models to try and convert and upload to the page itself. To start with we used a tea pot model to try and upload as it has quite a few distinct features to show and to recreate as well.
To begin with we start by setting all the global variables such as the file names, numbers, edges, depth etc. 
 
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
textureArray = fbx.FbxTextureArray()

After we’d done this we had to then find the path to the FBX files and once the location had be found have the script look for the all the FBX folders in the path. 

path = os.getcwd()
newpath=path+"\Fbx Files"
print(newpath)

os.chdir(newpath)
for file in glob.glob("*.fbx"):
    filenames.append(file)

print "number of files ", len(filenames)

filenum = len(filenames)

During this process we create an SVG element for later use as we’ll be converting all the FBX information into an SVG file.  Once we’ve searched through the FBX files location we load one of the files from the FBX list we got earlier.

doc = et.Element('svg', width='480', height='480', version='1.1', xmlns='http://www.w3.org/2000/svg', viewBox = '0,0,0,0', preserveAspectRatio = 'xMidYMid meet', onload='init(evt)')
script = et.SubElement(doc,'script', type='text/ecmascript')
data = '![CDATA[\n'
doc.text=("\n")

def clamp(x): 
    return max(0, min(x, 255))

for file in range(len(filenames)):
    sdk_manager, scene = FbxCommon.InitializeSdkObjects()
    if not FbxCommon.LoadScene(sdk_manager, scene, filenames[file]): 
        print str(filenames[file])
        print("Not found")      #print if unable to find/load

    rotation =  180
    rotation = rotation * 3.1415926 / 180

Once this has been done we get the root node of the file and begin getting all the information we need out of the file, such as the edge counts, poly counts, and make a list of all edges, faces, and to make a list of all depths in a string and then we also all the X, Y and Z coordinates.

    node = scene.GetRootNode()
    for i in range(node.GetChildCount()):
        child = node.GetChild(i)
        attr_type = child.GetNodeAttribute().GetAttributeType()
        edges = []
        vertices = []
        if attr_type==FbxCommon.FbxNodeAttribute.eMesh:          
            mesh = child.GetNodeAttribute()
            mesh.GetNode().GetMesh().RemoveBadPolygons()
            #Get the edge count
            edgecount = mesh.GetNode().GetMesh().GetMeshEdgeCount()
            #Get the polygon count
            polygoncount = mesh.GetNode().GetMesh().GetPolygonCount()
            #Make a list of all edges in a string
            contents = "edges = ["
            for edge in range(edgecount):
                start, end = mesh.GetNode().GetMesh().GetMeshEdgeVertices(edge)
                contents += "[" + str(start) + "," + str(end) + "],"
            contents = contents[:-1] +"]\n"
            #Make a list of all faces in a string
            contents += "faces = ["
            for polygon in range(polygoncount):
                contents += "["
                for size in range(mesh.GetNode().GetMesh().GetPolygonSize(polygon)):
                    contents +=str(mesh.GetNode().GetMesh().GetPolygonVertex(polygon,size))+","
                contents = contents[:-1] +"],"
            contents = contents[:-1] + "]\n"
            #Make a list of all depths
            contents += "depth =["
            depth = []
            for polygon in range(mesh.GetNode().GetMesh().GetPolygonCount()):
                contents += "0,"
            contents = contents[:-1] + "]\n"

Once we’ve gotten all that information we then start to build out our image by setting the smallest control points and then adding these to the list for the X, Y and Z coordinates. 
After this has been done we can finally start building by using functions

            data += "\n\ncentre_x = "+str(-smallestControlPointX)+";\ncentre_y = "+str(-smallestControlPointY)+";\ncentre_z = "+str(-smallestControlPointZ)+";\n\n\n\n\tvar minX = -999;\n\tvar minY = -999;\n\tvar maxX = -999;\n\tvar maxY = -999;\n\n"
            data += "function init(evt)\n{\n\tif ( window.svgDocument == null )\n\t{\n\t\tsvgDocument = evt.target.ownerDocument;\n\t}\n\trotateAboutY("+str((135*3.14/180))+");\n\trotateAboutX("+str(-(135*3.14/180))+");\n\tcalculateDepth()\n\tdrawBox();\n\tsetViewBox();\nif(minX < 0 || minY < 0)\n{\n\tfixCoords();\n\tdrawBox();\n\tsetViewBox();\n}}"

            data += "\n\n\nfunction setViewBox()\n{\n\tminX = -999;\n\tminY = -999;\n\tmaxX = -999;\n\tmaxY = -999;\n\t\n\tfor(var i = 0; i < x_coords.length; i++)\n\t{\n\t\tif(minX == -999 || x_coords[i] < minX)\n\t\t\tminX = x_coords[i];\n\t\tif(minY == -999 || y_coords[i] < minY)\n\t\t\tminY = y_coords[i];\n\t\tif(maxX == -999 || x_coords[i] > maxX)\n\t\t\tmaxX = x_coords[i];\n\t\tif(maxY == -999 || y_coords[i] > maxY)\n\t\t\tmaxY = y_coords[i];\n\t}\n\tshape = document.getElementsByTagName('svg')[0];\n\tshape.setAttribute('viewBox', minX+'" + str(file*50) + " '+ minY+' '+ maxX+'" + str(file*50) + " '+maxY);\n}"
            data += "\n\n\nfunction fixCoords()\n{\n\tif(minX < 0)\n\t{\n\t\tcentre_x += -minX;\n\t\tfor(var i = 0; i < x_coords.length;i++)\n\t\t{\n\t\t\tx_coords[i] += -minX;\n\t\t}\n\t}\n\tif(minY < 0)\n\t{\n\t\tcentre_y += -minY;\n\t\tfor(var i = 0; i < y_coords.length;i++)\n\t\t{\n\t\t\ty_coords[i] += -minY;\n\t\t}\n\t}\n}"            
            data += "\n\n\nfunction calculateDepth()\n{\n\tvar facesDepth = Array(faces.length);\n\tfor(var i = 0; i < faces.length; i++)\n\t{\n\t\tvar currentDepth = 0;\n\t\tfor(var u = 0; u < faces[i].length; u ++)\n\t\t{\n\t\t\tcurrentDepth += z_coords[faces[i][u]];\n\t\t}\n\t\tcurrentDepth /= faces[i].length;\n\t\tfacesDepth[i] = currentDepth;\n\t}\n\tfor(var i = 0; i < depth.length; i++)\n\t{\n\t\tvar smallest = -1;\n\t\tfor(var u = 0; u < facesDepth.length; u++)\n\t\t{\n\t\t\tif(facesDepth[u] != -99999 && (smallest == -1 || facesDepth[smallest] > facesDepth[u]))\n\t\t\t\tsmallest = u;\n\t\t}\n\t\tdepth[i] = smallest;\n\t\tfacesDepth[smallest] = -99999;\n\t}\n}"
            data += "\n\n\nfunction drawBox()\n{\n\tfor(var i=0; i<depth.length; i++)\n\t{\n\t\tface = svgDocument.getElementById('face-'+i);\n\t\tvar d = 'm'+x_coords[faces[depth[i]][0]]+' '+y_coords[faces[depth[i]][0]];\n\t\tfor(var u = 1; u < faces[depth[i]].length; u++)\n\t\t{\n\t\t\td+= ' ' + 'L'+x_coords[faces[depth[i]][u]]+' '+y_coords[faces[depth[i]][u]];\n\t\t}\n\t\td+= ' Z';\n\t\tface.setAttributeNS(null, 'd', d);\n\t}\n}"
            

            data += "\n\n\nfunction rotateAboutX(radians)\n{\n\tfor(var i=0; i<x_coords.length; i++)\n\t{\n\t\ty = y_coords[i] - centre_y;\n\t\tz = z_coords[i] - centre_z;\n\t\td = Math.sqrt(y*y + z*z);\n\t\ttheta  = Math.atan2(y, z) + radians;\n\t\ty_coords[i] = centre_y + d * Math.sin(theta);\n\t\tz_coords[i] = centre_z + d * Math.cos(theta);\n\t}\n}"
            data += "\n\n\nfunction rotateAboutY(radians)\n{\n\tfor(var i=0; i<x_coords.length; i++)\n\t{\n\t\tx = x_coords[i] - centre_x;\n\t\tz = z_coords[i] - centre_z;\n\t\td = Math.sqrt(x*x + z*z);\n\t\ttheta  = Math.atan2(x, z) + radians;\n\t\tx_coords[i] = centre_x + d * Math.sin(theta);\n\t\tz_coords[i] = centre_z + d * Math.cos(theta);\n\t}\n}"
            data += "\n\n\nfunction rotateAboutZ(radians)\n{\n\tfor(var i=0; i<x_coords.length; i++)\n\t{\n\t\tx = x_coords[i] - centre_x;\n\t\ty = y_coords[i] - centre_y;\n\t\td = Math.sqrt(x*x + y*y);\n\t\ttheta  = Math.atan2(x, y) + radians;\n\t\tx_coords[i] = centre_x + d * Math.sin(theta);\n\t\ty_coords[i] = centre_y + d * Math.cos(theta);\n\t}\n}"

            data += "\n]]"
            cdata = et.SubElement(script, data)

Once all of this has been done we then create the SVG file and then store all the data accumulated here and then we clean up the SVG and make sure it’s presentable.

            os.chdir(path)
            f = open(str(filenames[file]) + '.svg', 'w')
            f.write('<?xml version=\"1.0\" standalone=\"no\"?>\n')
            f.write('<!DOCTYPE svg PUBLIC \"-//W3C//DTD SVG 1.1//EN\"\n')
            f.write('\"http://www.w3.org/Graphics/SVG/1.1/DTD/svg11.dtd\">\n')
            f.write(et.tostring(doc))
            f.close()

            #Cleanup the svg file
            r = open(str(filenames[file]) + '.svg', 'r')
            filedata = r.read()
            r.close()

            newdata = filedata.replace("] />", "]>")

            f = open(str(filenames[file]) + '.svg', 'w')
            f.write(newdata)
            f.close()

Once all of this has been done, stored and cleaned up, we then update the HTML page to have the new names of the SVG file that was created. When the index.HTML page is being loaded it calls on the SVG file and then when that happens the SVG file runs its own script in its file to generate the image on the webpage.
To get all of this to display onto the HTML page we run the pythonFBX script in the server script, this’ll then get all the information and the final SVG file and display it on the page.
If we were to attempt this project again we’d try harder to try and get a non-local hosted server working via something like amazon or google and try and display it properly on an online server. Another possible thing we could look into adding further would be animated models and getting the SVG to display the animation of the model once loaded on the site.