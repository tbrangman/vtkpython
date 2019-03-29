import vtk

# create a rendering window and renderer
ren = vtk.vtkRenderer()
renWin = vtk.vtkRenderWindow()
renWin.AddRenderer(ren)

renWin.SetSize(1000,1000)

for x in range (0,3): 
	for y in range (0,3):
		for z in range (0,3):
			# create source
			source = vtk.vtkCylinderSource()
			source.SetCenter(1*x,1*y,1*z)

			source.SetRadius(0.50)
			source.SetHeight(0.75)
			source.SetResolution(60)

			# mapper
			mapper = vtk.vtkPolyDataMapper()
			mapper.SetInputConnection(source.GetOutputPort())

			# actor
			actor = vtk.vtkActor()
			actor.SetMapper(mapper)
			actor.GetProperty().SetColor(0,1,1)

			# assign actor to the renderer
			ren.AddActor(actor)

# create a renderwindowinteractor
iren = vtk.vtkRenderWindowInteractor()
iren.SetRenderWindow(renWin)

# gradient background
ren.GradientBackgroundOn()
ren.SetBackground(0,1,0)
ren.SetBackground2(1,0,0)

# enable user interface interactor
iren.Initialize()
renWin.Render()
iren.Start()