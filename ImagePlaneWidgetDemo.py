import vtk
useDataRoot = False

from vtk.util.misc import vtkGetDataRoot
VTK_DATA_ROOT = vtkGetDataRoot() + "/"

if useDataRoot==False:
	VTK_DATA_ROOT = ""

# Start by loading some data.
v16 = vtk.vtkVolume16Reader()

#Image parameters (size and spacing) are being hardcoded, 
# but they could have been read from the header file.

# Set the size of each slice.
v16.SetDataDimensions(64, 64)
v16.SetDataByteOrderToLittleEndian()
v16.SetFilePrefix("VTKDATA/Data/headsq/quarter")

# the files are quarter.1 through quarter.93
v16.SetImageRange(1, 93)

# this is the spacing specified in the header (anisotropic voxels)
v16.SetDataSpacing(3.2, 3.2, 1.5)
v16.Update()

vtkSDDP = vtk.vtkStreamingDemandDrivenPipeline
xMin, xMax, yMin, yMax, zMin, zMax = v16.GetOutputInformation(0).Get(vtkSDDP.WHOLE_EXTENT())


spacing = v16.GetOutput().GetSpacing()
sx, sy, sz = spacing

origin = v16.GetOutput().GetOrigin()
ox, oy, oz = origin

# An outline is shown for visual context.
outline = vtk.vtkOutlineFilter()
outline.SetInputConnection(v16.GetOutputPort())

outlineMapper = vtk.vtkPolyDataMapper()
outlineMapper.SetInputConnection(outline.GetOutputPort())

outlineActor = vtk.vtkActor()
outlineActor.SetMapper(outlineMapper)


axes = vtk.vtkAxesActor()
#  The axes are positioned with a user transform
 
# properties of the axes labels can be set as follows
# this sets the x axis label to red
# axes->GetXAxisCaptionActor2D()->GetCaptionTextProperty()->SetColor(1,0,0);
 
# the actual text of the axis label can be changed:
# axes->SetXAxisLabelText("test");

# The shared picker enables us to use 3 planes at one time
# and gets the picking order right
picker = vtk.vtkCellPicker()
picker.SetTolerance(0.005)

# An image plane widgets is used to probe the dataset.
# See https://www.vtk.org/doc/nightly/html/classvtkImagePlaneWidget.html for more details
planeWidgetX = vtk.vtkImagePlaneWidget()
planeWidgetY = vtk.vtkImagePlaneWidget()
planeWidgetZ = vtk.vtkImagePlaneWidget()

#Interpolation technique to use when texturing the plane
planeWidgetX.SetResliceInterpolateToLinear()
planeWidgetY.SetResliceInterpolateToLinear()
planeWidgetZ.SetResliceInterpolateToLinear()

# Show image coordinates and transfer function parameters in the render window.
planeWidgetX.DisplayTextOn()
planeWidgetY.DisplayTextOn()
planeWidgetX.DisplayTextOn()

#Where to get the image data
planeWidgetX.SetInputConnection(v16.GetOutputPort())
planeWidgetY.SetInputConnection(v16.GetOutputPort())
planeWidgetZ.SetInputConnection(v16.GetOutputPort())

#Which imaging plane to use.
planeWidgetX.SetPlaneOrientationToXAxes() #Plane Orientation set to X axis
planeWidgetY.SetPlaneOrientationToYAxes() #Plane Orientation set to Y axis
planeWidgetZ.SetPlaneOrientationToZAxes() #Plane Orientation set to Z axis

#Which slice number from the image
planeWidgetX.SetSliceIndex(32) #initial slice index to 32
planeWidgetY.SetSliceIndex(32) #initial slice index to 32
planeWidgetZ.SetSliceIndex(46) #initial slice index to 46

#Connect to the mouse picker
planeWidgetX.SetPicker(picker)
planeWidgetY.SetPicker(picker)
planeWidgetZ.SetPicker(picker)

#Key used to activate the plane if it is inactive.
planeWidgetX.SetKeyPressActivationValue("x")
planeWidgetY.SetKeyPressActivationValue("y")
planeWidgetZ.SetKeyPressActivationValue("z")

#Set the color
prop1 = planeWidgetX.GetPlaneProperty()
prop1.SetColor(1, 0, 0)
prop2 = planeWidgetY.GetPlaneProperty()
prop2.SetColor(1, 1, 0)
prop3 = planeWidgetZ.GetPlaneProperty()
prop3.SetColor(0, 0, 1) 

# Create the RenderWindow and Renderer
ren = vtk.vtkRenderer()
renWin = vtk.vtkRenderWindow()
renWin.AddRenderer(ren)

# Add the outline actor to the renderer, set the background color and size
ren.AddActor(outlineActor)
renWin.SetSize(600, 600)
ren.SetBackground(0.3, 0.3, 0.4)

iact = vtk.vtkRenderWindowInteractor()
iact.SetRenderWindow(renWin)

planeWidgetX.SetInteractor(iact)
planeWidgetX.On()
planeWidgetY.SetInteractor(iact)
planeWidgetY.On()
planeWidgetZ.SetInteractor(iact)
planeWidgetZ.On()


# This function creates a texture containing text.
# Useful for creating textured buttons with text on them.
def textImage(text):
	buttonImage = vtk.vtkImageData()
	freeType = vtk.vtkFreeTypeStringToImage()
	textProperty = vtk.vtkTextProperty()
	textProperty.SetColor(1.0, 1.0, 1.0)
	textProperty.SetFontSize(64);
	textProperty.SetFontFamilyToTimes()
	freeType.RenderString(textProperty, text, 120, buttonImage);
	return buttonImage

def quit_program(obj, event):
	quit()

quit_image = textImage("Quit")
buttonRep1 = vtk.vtkTexturedButtonRepresentation2D()
buttonRep1.SetNumberOfStates(2);
buttonRep1.SetButtonTexture(0, quit_image);
buttonRep1.SetButtonTexture(1, quit_image);
buttonRep1.PlaceWidget([0, 100, 0, 50, 0, 50]);

buttonWidget1 = vtk.vtkButtonWidget()
buttonWidget1.SetInteractor(iact)
buttonWidget1.SetRepresentation(buttonRep1)
buttonWidget1.SetEnabled(True)
buttonWidget1.On()
buttonWidget1.AddObserver("StateChangedEvent", quit_program)
#end quit

#begin interp button
#toggle behavior booleon
interpolation_on = True 
def toggle_interpolation(obj, event):
	global interpolation_on #
	interpolation_on = not interpolation_on
	print interpolation_on
	x = planeWidgetX.GetSliceIndex()#prevent the plane from moving
	y = planeWidgetY.GetSliceIndex()#prevent the plane from moving
	z = planeWidgetZ.GetSliceIndex()#prevent the plane from moving
	if interpolation_on: #interpolate toggle on/off
		planeWidgetX.TextureInterpolateOn();
		planeWidgetX.SetInputConnection(v16.GetOutputPort())
		planeWidgetY.TextureInterpolateOn();
		planeWidgetY.SetInputConnection(v16.GetOutputPort())
		planeWidgetZ.TextureInterpolateOn();
		planeWidgetZ.SetInputConnection(v16.GetOutputPort())
	else:
		planeWidgetX.TextureInterpolateOff(); #toggle off
		planeWidgetX.SetInputConnection(v16.GetOutputPort())
		planeWidgetY.TextureInterpolateOff(); #toggle off
		planeWidgetY.SetInputConnection(v16.GetOutputPort())
		planeWidgetZ.TextureInterpolateOff(); #toggle off
		planeWidgetZ.SetInputConnection(v16.GetOutputPort())
	x = planeWidgetX.GetSliceIndex(x) #prevent the plane from moving
	y = planeWidgetY.GetSliceIndex(y) #prevent the plane from moving
	z = planeWidgetZ.GetSliceIndex(z) #prevent the plane from moving

interp_on_image = textImage("Interpolation On")
interp_off_image = textImage("Interpolation Off")
buttonRep2 = vtk.vtkTexturedButtonRepresentation2D()
buttonRep2.SetNumberOfStates(2);
buttonRep2.SetButtonTexture(0, interp_on_image);
buttonRep2.SetButtonTexture(1, interp_off_image);
buttonRep2.PlaceWidget([100, 300, 0, 50, 0, 50]);

buttonWidget2 = vtk.vtkButtonWidget()
buttonWidget2.SetInteractor(iact)
buttonWidget2.SetRepresentation(buttonRep2)
buttonWidget2.SetEnabled(True)
buttonWidget2.On()
buttonWidget2.AddObserver("StateChangedEvent", toggle_interpolation)



# Create an initial view.
#See https://www.vtk.org/doc/nightly/html/classvtkCamera.html for more details
ren.AddActor(axes)
cam1 = ren.GetActiveCamera()
cam1.Elevation(110)
cam1.SetViewUp(0, 0, -1)
cam1.Azimuth(45)

#point the camera at the center of the image
cx = ox+(0.5*(xMax-xMin))*sx
cy = oy+(0.5*(yMax-yMin))*sy
cz = oy+(0.5*(zMax-zMin))*sz
cam1.SetFocalPoint(cx, cy, cz)
ren.ResetCameraClippingRange()

iact.Initialize()
renWin.Render()
iact.Start()

