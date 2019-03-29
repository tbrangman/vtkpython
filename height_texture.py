import vtk

#The heightmap for the terrain
heightfile = "gcanyon_height.png" # to load from current directory

#The coor image of the terrain
colorfile = "gcanyon_color.png" # to load from current directory


# create a rendering window and renderer
ren = vtk.vtkRenderer()
renWin = vtk.vtkRenderWindow()
renWin.AddRenderer(ren)

# create a renderwindowinteractor
iren = vtk.vtkRenderWindowInteractor()
iren.SetRenderWindow(renWin)

createReader = vtk.vtkImageReader2Factory()
reader = createReader.CreateImageReader2(heightfile)
reader.SetFileName(heightfile)

geom = vtk.vtkImageDataGeometryFilter()
geom.SetInputConnection(reader.GetOutputPort())

#Compute texture coordinates for the geometry
toplane = vtk.vtkTextureMapToPlane()
toplane.SetInputConnection(geom.GetOutputPort())

#create a reader for the color image
colorreader = createReader.CreateImageReader2(colorfile)
colorreader.SetFileName(colorfile)

#create a texture from the color image
texture = vtk.vtkTexture()
texture.SetInputConnection(colorreader.GetOutputPort())

warp = vtk.vtkWarpScalar()
warp.SetInputConnection(toplane.GetOutputPort())
warp.SetScaleFactor(1.0)

mapper = vtk.vtkPolyDataMapper()
mapper.SetInputConnection(warp.GetOutputPort())
mapper.ImmediateModeRenderingOff()

actor = vtk.vtkActor()
actor.SetMapper(mapper)
#Apply the loaded texture to the actor
actor.SetTexture(texture)

# assign actor to the renderer
ren.AddActor(actor)

#create a new light to brighten the scene
light = vtk.vtkLight()
light.SetLightTypeToSceneLight();
light.SetPositional(False); 
light.SetDiffuseColor(2,2,2);
light.SetAmbientColor(1,1,1);
ren.AddLight(light)

# enable user interface interactor
iren.Initialize()
renWin.Render()
iren.Start()