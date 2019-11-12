import numpy as np
import vtk
from scipy.spatial.transform import Rotation as R

class vtkTimerCallback():
    def __init__(self, steps, sources, mappers, actors, iren):
        self.timer_count = 0
        self.steps = steps
        self.sources = sources
        self.mappers = mappers
        self.actors = actors
        self.iren = iren
        self.timerId = None
        self.state = np.array([0., 0., 0., 0., 0., 0., 1., 1., 1.])
        self.state_dot = np.array((0.001, 0.001, -0.001, 0.001, 0.001, 0., 0.001, -0.001, 0.001))

    def execute(self, obj, event):
        # Aquí debería acceder a los nuevos estados (ya generados o generados aquí con un generador).
        self.state = self.state + self.state_dot 
        rd = self.state
        self.actors[0].SetPosition(rd[0], rd[1], 0)
        self.actors[0].SetScale(rd[6])
        self.actors[1].SetPosition(-rd[2], -rd[3], 0)
        self.actors[1].SetScale(rd[7])
        
        #  The axes are positioned with a user transform
        transform = vtk.vtkTransform()
        transform.Translate(rd[4], 0.0, 0.0)
        self.actors[2].SetUserTransform(transform)
        
        # También se puede hacer un self.actors[0].SetPosition() ó SetScale()
        iren = obj
        iren.GetRenderWindow().Render()
        self.timer_count += 1

        if self.timer_count == self.steps:
            if self.timerId:
                iren.DestroyTimer(self.timerId)

class figure3D():

    def __init__(self, bgcolor='Silver', size=(800, 600)):

        self.colors = vtk.vtkNamedColors()

        # A renderer and render window
        self.renderer = vtk.vtkRenderer()
        self.renderer.SetBackground(self.colors.GetColor3d(bgcolor))

        # render window
        self.renwin = vtk.vtkRenderWindow()
        self.renwin.AddRenderer(self.renderer)
        self.renwin.SetSize(size[0], size[1])

        # An interactor
        self.interactor = vtk.vtkRenderWindowInteractor()
        self.interactor.SetRenderWindow(self.renwin)
        style = vtk.vtkInteractorStyleTerrain()
        self.interactor.SetInteractorStyle(style)

        self.interactor.Initialize()

        self.sources = []
        self.mappers = []
        self.actors = []

    def render(self):
        self.renwin.Render()
        self.interactor.Start()

    def add_sphere(self, name='sphere1', center=[0, 0, 0], orientation=[0, 0, 0], radius=5.2, color='blue', transparency=0.8, contours='latitude'):
        
        sphere = vtk.vtkSphere()
        sphere.SetCenter(center[0], center[1], center[2])
        sphere.SetRadius(radius)

        # The sample function generates a distance function from the implicit
        # function. This is then contoured to get a polygonal surface.
        sample = vtk.vtkSampleFunction()
        sample.SetImplicitFunction(sphere)
        sample.SetModelBounds(-.5, .5, -.5, .5, -.5, .5)
        sample.SetSampleDimensions(20, 20, 20)
        sample.ComputeNormalsOff()

        # contour
        surface = vtk.vtkContourFilter()
        surface.SetInputConnection(sample.GetOutputPort())
        surface.SetValue(0, 0.0)

        # mapper
        mapper = vtk.vtkPolyDataMapper()
        mapper.SetInputConnection(surface.GetOutputPort())
        mapper.ScalarVisibilityOff()

        actor = vtk.vtkActor()
        actor.SetMapper(mapper)
        actor.GetProperty().EdgeVisibilityOn()
        actor.GetProperty().SetColor(self.colors.GetColor3d('AliceBlue'))
        actor.GetProperty().SetEdgeColor(self.colors.GetColor3d('SteelBlue'))

        # Append elements
        self.sources.append(sphere)
        self.mappers.append(mapper)
        self.actors.append(actor)

        # add the actor
        self.renderer.AddActor(actor)

        # Initialize must be called prior to creating timer events.
        self.interactor.Initialize()

        return actor

    def add_ellipsoid(self, name='ellipsoid1', center=[0, 0, 0], orientation=[0, 0, 0], radius=5.2, color='blue', transparency=0.8, contours='latitude'):
        
        # create an ellipsoid using a implicit quadric
        quadric = vtk.vtkQuadric()
        quadric.SetCoefficients(0.5, 1, 0.2, 0, 0.1, 0, 0, 0.2, 0, 0)

        # The sample function generates a distance function from the implicit
        # function. This is then contoured to get a polygonal surface.
        sample = vtk.vtkSampleFunction()
        sample.SetImplicitFunction(quadric)
        sample.SetModelBounds(-0.5, 0.5, -0.5, 0.5, -0.5, 0.5)
        sample.SetSampleDimensions(40, 40, 40)
        sample.ComputeNormalsOff()

        # contour
        surface = vtk.vtkContourFilter()
        surface.SetInputConnection(sample.GetOutputPort())
        surface.SetValue(0, 0.0)

        # mapper
        mapper = vtk.vtkPolyDataMapper()
        mapper.SetInputConnection(surface.GetOutputPort())
        mapper.ScalarVisibilityOff()

        actor = vtk.vtkActor()
        actor.SetMapper(mapper)
        actor.GetProperty().EdgeVisibilityOn()
        actor.GetProperty().SetColor(self.colors.GetColor3d('AliceBlue'))
        actor.GetProperty().SetEdgeColor(self.colors.GetColor3d('SteelBlue'))

        # Append elements
        self.sources.append(quadric)
        self.mappers.append(mapper)
        self.actors.append(actor)

        # add the actor
        self.renderer.AddActor(actor)

        # Initialize must be called prior to creating timer events.
        self.interactor.Initialize()
        
    def add_axes(self, name='axes1', origin=[0, 0, 2], orientation=[0, 0, 0], length=1, color='black', arrow_type='triangle_30'):

        transform = vtk.vtkTransform()
        transform.Translate(1.0, 0.0, 0.0)

        axes = vtk.vtkAxesActor()
        #  The axes are positioned with a user transform
        axes.SetUserTransform(transform)

        # properties of the axes labels can be set as follows
        # this sets the x axis label to red
        axes.GetXAxisCaptionActor2D().GetCaptionTextProperty().SetColor(self.colors.GetColor3d("Red"))

        # the actual text of the axis label can be changed:
        axes.SetXAxisLabelText("test")

        # Append elements
        self.sources.append(None)
        self.mappers.append(None)
        self.actors.append(axes)

        self.renderer.AddActor(axes)

        # Initialize must be called prior to creating timer events.
        self.interactor.Initialize()

    def animate(self):
        # Sign up to receive TimerEvent
        cb = vtkTimerCallback(10000, self.sources, self.mappers, self.actors, self.interactor)
        self.interactor.AddObserver('TimerEvent', cb.execute)
        cb.timerId = self.interactor.CreateRepeatingTimer(5)
        # start the interaction and timer
        self.renwin.Render()
        self.interactor.Start()

