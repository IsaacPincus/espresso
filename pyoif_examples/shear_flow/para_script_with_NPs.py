# trace generated using paraview version 5.6.3
#
# To ensure correct image size when batch processing, please search 
# for and uncomment the line `# renderView*.ViewSize = [*,*]`

#### import the simple module from the paraview
from paraview.simple import *
#### disable automatic camera reset on 'Show'
paraview.simple._DisableFirstRenderCameraReset()

# create a new 'Legacy VTK Reader'
cell_ = LegacyVTKReader(FileNames=['/home/ipincus/pyoip/espresso/pyoif_examples/shear_flow/output/sim_with_NPs/cell_0.vtk', '/home/ipincus/pyoip/espresso/pyoif_examples/shear_flow/output/sim_with_NPs/cell_1.vtk', '/home/ipincus/pyoip/espresso/pyoif_examples/shear_flow/output/sim_with_NPs/cell_2.vtk', '/home/ipincus/pyoip/espresso/pyoif_examples/shear_flow/output/sim_with_NPs/cell_3.vtk', '/home/ipincus/pyoip/espresso/pyoif_examples/shear_flow/output/sim_with_NPs/cell_4.vtk', '/home/ipincus/pyoip/espresso/pyoif_examples/shear_flow/output/sim_with_NPs/cell_5.vtk', '/home/ipincus/pyoip/espresso/pyoif_examples/shear_flow/output/sim_with_NPs/cell_6.vtk', '/home/ipincus/pyoip/espresso/pyoif_examples/shear_flow/output/sim_with_NPs/cell_7.vtk', '/home/ipincus/pyoip/espresso/pyoif_examples/shear_flow/output/sim_with_NPs/cell_8.vtk', '/home/ipincus/pyoip/espresso/pyoif_examples/shear_flow/output/sim_with_NPs/cell_9.vtk'])

# get animation scene
animationScene1 = GetAnimationScene()

# update animation scene based on data timesteps
animationScene1.UpdateAnimationUsingDataTimeSteps()

# create a new 'Legacy VTK Reader'
nP_ = LegacyVTKReader(FileNames=['/home/ipincus/pyoip/espresso/pyoif_examples/shear_flow/output/sim_with_NPs/NP_0.vtk', '/home/ipincus/pyoip/espresso/pyoif_examples/shear_flow/output/sim_with_NPs/NP_1.vtk', '/home/ipincus/pyoip/espresso/pyoif_examples/shear_flow/output/sim_with_NPs/NP_2.vtk', '/home/ipincus/pyoip/espresso/pyoif_examples/shear_flow/output/sim_with_NPs/NP_3.vtk', '/home/ipincus/pyoip/espresso/pyoif_examples/shear_flow/output/sim_with_NPs/NP_4.vtk', '/home/ipincus/pyoip/espresso/pyoif_examples/shear_flow/output/sim_with_NPs/NP_5.vtk', '/home/ipincus/pyoip/espresso/pyoif_examples/shear_flow/output/sim_with_NPs/NP_6.vtk', '/home/ipincus/pyoip/espresso/pyoif_examples/shear_flow/output/sim_with_NPs/NP_7.vtk', '/home/ipincus/pyoip/espresso/pyoif_examples/shear_flow/output/sim_with_NPs/NP_8.vtk', '/home/ipincus/pyoip/espresso/pyoif_examples/shear_flow/output/sim_with_NPs/NP_9.vtk'])

# get active view
renderView1 = GetActiveViewOrCreate('RenderView')
# uncomment following to set a specific view size
# renderView1.ViewSize = [1080, 770]

# show data in view
cell_Display = Show(cell_, renderView1)

# trace defaults for the display properties.
cell_Display.Representation = 'Surface'
cell_Display.ColorArrayName = [None, '']
cell_Display.OSPRayScaleFunction = 'PiecewiseFunction'
cell_Display.SelectOrientationVectors = 'None'
cell_Display.ScaleFactor = 1.2000000000000002
cell_Display.SelectScaleArray = 'None'
cell_Display.GlyphType = 'Arrow'
cell_Display.GlyphTableIndexArray = 'None'
cell_Display.GaussianRadius = 0.06
cell_Display.SetScaleArray = [None, '']
cell_Display.ScaleTransferFunction = 'PiecewiseFunction'
cell_Display.OpacityArray = [None, '']
cell_Display.OpacityTransferFunction = 'PiecewiseFunction'
cell_Display.DataAxesGrid = 'GridAxesRepresentation'
cell_Display.SelectionCellLabelFontFile = ''
cell_Display.SelectionPointLabelFontFile = ''
cell_Display.PolarAxes = 'PolarAxesRepresentation'

# init the 'PiecewiseFunction' selected for 'OSPRayScaleFunction'
cell_Display.OSPRayScaleFunction.Points = [0.7362177978134756, 0.0, 0.5, 0.0, 3.040108122666924, 1.0, 0.5, 0.0]

# init the 'PiecewiseFunction' selected for 'ScaleTransferFunction'
cell_Display.ScaleTransferFunction.Points = [0.7362177978134756, 0.0, 0.5, 0.0, 3.040108122666924, 1.0, 0.5, 0.0]

# init the 'PiecewiseFunction' selected for 'OpacityTransferFunction'
cell_Display.OpacityTransferFunction.Points = [0.7362177978134756, 0.0, 0.5, 0.0, 3.040108122666924, 1.0, 0.5, 0.0]

# init the 'GridAxesRepresentation' selected for 'DataAxesGrid'
cell_Display.DataAxesGrid.XTitleFontFile = ''
cell_Display.DataAxesGrid.YTitleFontFile = ''
cell_Display.DataAxesGrid.ZTitleFontFile = ''
cell_Display.DataAxesGrid.XLabelFontFile = ''
cell_Display.DataAxesGrid.YLabelFontFile = ''
cell_Display.DataAxesGrid.ZLabelFontFile = ''

# init the 'PolarAxesRepresentation' selected for 'PolarAxes'
cell_Display.PolarAxes.PolarAxisTitleFontFile = ''
cell_Display.PolarAxes.PolarAxisLabelFontFile = ''
cell_Display.PolarAxes.LastRadialAxisTextFontFile = ''
cell_Display.PolarAxes.SecondaryRadialAxesTextFontFile = ''

# reset view to fit data
renderView1.ResetCamera()

# show data in view
nP_Display = Show(nP_, renderView1)

# trace defaults for the display properties.
nP_Display.Representation = 'Surface'
nP_Display.ColorArrayName = [None, '']
nP_Display.OSPRayScaleFunction = 'PiecewiseFunction'
nP_Display.SelectOrientationVectors = 'None'
nP_Display.ScaleFactor = 0.2
nP_Display.SelectScaleArray = 'None'
nP_Display.GlyphType = 'Arrow'
nP_Display.GlyphTableIndexArray = 'None'
nP_Display.GaussianRadius = 0.01
nP_Display.SetScaleArray = [None, '']
nP_Display.ScaleTransferFunction = 'PiecewiseFunction'
nP_Display.OpacityArray = [None, '']
nP_Display.OpacityTransferFunction = 'PiecewiseFunction'
nP_Display.DataAxesGrid = 'GridAxesRepresentation'
nP_Display.SelectionCellLabelFontFile = ''
nP_Display.SelectionPointLabelFontFile = ''
nP_Display.PolarAxes = 'PolarAxesRepresentation'

# init the 'PiecewiseFunction' selected for 'OSPRayScaleFunction'
nP_Display.OSPRayScaleFunction.Points = [0.7362177978134756, 0.0, 0.5, 0.0, 3.040108122666924, 1.0, 0.5, 0.0]

# init the 'PiecewiseFunction' selected for 'ScaleTransferFunction'
nP_Display.ScaleTransferFunction.Points = [0.7362177978134756, 0.0, 0.5, 0.0, 3.040108122666924, 1.0, 0.5, 0.0]

# init the 'PiecewiseFunction' selected for 'OpacityTransferFunction'
nP_Display.OpacityTransferFunction.Points = [0.7362177978134756, 0.0, 0.5, 0.0, 3.040108122666924, 1.0, 0.5, 0.0]

# init the 'GridAxesRepresentation' selected for 'DataAxesGrid'
nP_Display.DataAxesGrid.XTitleFontFile = ''
nP_Display.DataAxesGrid.YTitleFontFile = ''
nP_Display.DataAxesGrid.ZTitleFontFile = ''
nP_Display.DataAxesGrid.XLabelFontFile = ''
nP_Display.DataAxesGrid.YLabelFontFile = ''
nP_Display.DataAxesGrid.ZLabelFontFile = ''

# init the 'PolarAxesRepresentation' selected for 'PolarAxes'
nP_Display.PolarAxes.PolarAxisTitleFontFile = ''
nP_Display.PolarAxes.PolarAxisLabelFontFile = ''
nP_Display.PolarAxes.LastRadialAxisTextFontFile = ''
nP_Display.PolarAxes.SecondaryRadialAxesTextFontFile = ''

# update the view to ensure updated data information
renderView1.Update()

#### saving camera placements for all active views

# current camera placement for renderView1
renderView1.CameraPosition = [13.05509970535002, 5.50496213253089, 40.630264909431865]
renderView1.CameraFocalPoint = [7.9999999999999964, 11.999850273132319, 7.9999999999999964]
renderView1.CameraViewUp = [0.0020133465107568323, 0.980818083669683, 0.19491493832530732]
renderView1.CameraParallelScale = 8.709834992677555

#### uncomment the following to render all views
# RenderAllViews()
# alternatively, if you want to write images, you can use SaveScreenshot(...).