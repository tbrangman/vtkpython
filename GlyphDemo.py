import vtk

lut = vtk.vtkLookupTable()
lut.SetNumberOfColors(256)
lut.SetHueRange(0.0, 0.667)
lut.Build()

#read the data
reader = vtk.vtkStructuredGridReader()
reader.SetFileName("density.vtk")
reader.Update()

minx, maxx, miny, maxy, minz, maxz = reader.GetOutput().GetExtent()

#For lab 6 create a vtkExtractGrid here, then set the VOI extents and sample rate.
grid = vtk.vtkExtractGrid()
grid.SetInputConnection(reader.GetOutputPort())
grid.SetSampleRate(2, 8, 2) # 1/2, 1/8, 1/2 sample rate
grid.SetVOI(minx, maxx, miny, maxy/2, minz, maxz/2) # Set Volume of Interest

#create an arrow to use as a glyph source (must be an object inherited from vtkPolyData)
arrow = vtk.vtkArrowSource()
arrow.SetTipResolution(6)
arrow.SetTipRadius(0.1)
arrow.SetTipLength(0.35)
arrow.SetShaftResolution(6)
arrow.SetShaftRadius(0.03)

#create glyph object
glyph = vtk.vtkGlyph3D()

#Connect input connection to the data reader. The points in the 
# dataset define the locations for the glyphs.
glyph.SetInputConnection(grid.GetOutputPort())

#Connect source connection to the source object. The source vtkPolyData 
# object will be drawn at every point defined by the input connection.
glyph.SetSourceConnection(arrow.GetOutputPort())

#For lab 6, change glyph settings here.
glyph.SetScaleModeToScaleByVector()
glyph.ScalingOn()
glyph.SetScaleFactor(.007)
glyph.SetColorModeToColorByScalar()

glyphMapper = vtk.vtkPolyDataMapper()
glyphMapper.SetInputConnection(glyph.GetOutputPort())
glyphMapper.SetLookupTable(lut)
#Lookup table not being used now because scalar visibility is off
glyphMapper.ScalarVisibilityOn()
glyphMapper.SetScalarRange(reader.GetOutput().GetScalarRange())

glyphActor = vtk.vtkActor()
glyphActor.SetMapper(glyphMapper)

#create the outline for the dataset
outline = vtk.vtkStructuredGridOutlineFilter()
outline.SetInputConnection(reader.GetOutputPort())
outlineMapper = vtk.vtkPolyDataMapper()
outlineMapper.SetInputConnection(outline.GetOutputPort())
outlineActor = vtk.vtkActor()
outlineActor.SetMapper(outlineMapper)
	
ren = vtk.vtkRenderer()
renWin = vtk.vtkRenderWindow()
renWin.AddRenderer(ren)
iren = vtk.vtkRenderWindowInteractor()
iren.SetRenderWindow(renWin)

ren.AddActor(glyphActor)
ren.AddActor(outlineActor)

ren.SetBackground(0.5, 0.5, 0.5)
renWin.SetSize(500, 500)

iren.Initialize()
renWin.Render()
iren.Start()

