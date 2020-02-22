from scipy.spatial.transform import Rotation as R
import numpy as np
import time
import vtk

class vtkTimerCallback():
    def __init__(self, steps, sources, mappers, actors, callbacks, interactor, camera):
        self.timer_count = 0
        self.steps = steps
        self.sources = sources
        self.mappers = mappers
        self.actors = actors
        self.callbacks = callbacks
        self.interactor = interactor
        self.camera = camera
        self.timerId = None
        self.state = np.array([0., 0., 0., 0., 0., 0., 1., 1., 1.])
        self.state_dot = np.array((0.001, 0.001, -0.001, 0.001, 0.001, 0., 0.001, -0.001, 0.001))
        self.time_start = 0
        self.time_end = 0
        self.time = 0

    def execute(self, obj, event):
        # Aquí debería acceder a los nuevos estados (ya generados o generados aquí con un generador).
        self.state = self.state + self.state_dot 
        self.time_end = time.time()
        if self.timer_count == 0:
            dt = 0
        else:
            dt = self.time_end - self.time_start
        if dt > 0.05:
            dt = 0 # Avoids time to keep counting during user interaction
        self.time += dt
        for i in range(len(self.callbacks)):
            radius = self.callbacks[0](self.time)
            print(f'Radius: {radius:.2f} Time: {self.time:.2f}')
            self.sources[0].SetRadius(radius)
        self.time_start = self.time_end

        # self.camera.Elevation(0)
        # self.camera.Roll(0)

        # self.actors[0].SetScale(rd[6])
        # self.actors[1].SetPosition(-rd[2], -rd[3], 0)
        # self.actors[1].SetScale(rd[7])
        
        # #  The axes are positioned with a user transform
        # transform = vtk.vtkTransform()
        # transform.Translate(rd[4], 0.0, 0.0)
        # self.actors[2].SetUserTransform(transform)
        # También se puede hacer un self.actors[0].SetPosition() ó SetScale()
        interactor = obj
        interactor.GetRenderWindow().Render()
        self.timer_count += 1

        if self.timer_count == self.steps:
            if self.timerId:
                interactor.DestroyTimer(self.timerId)

class figure3D():

    def __init__(self, bgcolor='Silver', size=(800, 600)):

        self.colors = vtk.vtkNamedColors()

        # Camera
        self.camera = vtk.vtkCamera()
        self.camera.SetPosition(0, 0, 0)
        self.camera.SetFocalPoint(0, 0, 0)

        # A renderer and render window
        self.renderer = vtk.vtkRenderer()
        self.renderer.SetBackground(self.colors.GetColor3d(bgcolor))
        # self.renderer.SetActiveCamera(self.camera)
        
        # self.camera = self.renderer.GetActiveCamera()


        # render window
        self.renwin = vtk.vtkRenderWindow()
        self.renwin.SetWindowName("Croma - Visualization Tool")
        self.renwin.AddRenderer(self.renderer)
        self.renwin.SetSize(size[0], size[1])

        # An interactor
        self.interactor = vtk.vtkRenderWindowInteractor()
        self.interactor.SetRenderWindow(self.renwin)
        style = vtk.vtkInteractorStyleTerrain()
        self.interactor.SetInteractorStyle(style)

        self.interactor.Initialize()

        self.names = {}
        self.sources = []
        self.mappers = []
        self.actors = []
        self.callbacks = []

    def render(self):
        self.renwin.Render()
        self.interactor.Start()
        self.animate()

    def add_sphere(self, name='sphere1', center=[0, 0, 0], orientation=[0, 0, 0], radius=0.2, color='blue', transparency=0.8, contours='latitude'):
        
        if hasattr(radius, '__call__'):
            self.callbacks.append(radius)
            radius = radius(0.0)

        sphere = vtk.vtkSphere()
        sphere.SetCenter(center[0], center[1], center[2])
        print(radius)
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
        self.names[name] = len(self.sources)
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
        self.names[name] = len(self.sources)        
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
        self.names[name] = len(self.sources)
        self.sources.append(None)
        self.mappers.append(None)
        self.actors.append(axes)

        self.renderer.AddActor(axes)

        # Initialize must be called prior to creating timer events.
        self.interactor.Initialize()

    def animate(self, *argv, time=np.inf):
        # type = 0
        # object_names = []
        # object_ids = []
        # object_properties = []
        # object_callbacks = []
        # for arg in argv:
        #     if type == 0:
        #         object_names.append(arg)
        #         object_ids.append(self.names[arg])
        #     elif type == 1:
        #         object_properties.append(arg)
        #     elif type == 2:
        #         object_callbacks.append(arg)
        #         type = -1
        #     type += 1
        # # Sign up to receive TimerEvent
        # print(object_ids)
        # TODO: Reorder all inputs using requested ids
        cb = vtkTimerCallback(200, self.sources, self.mappers, self.actors, self.callbacks, self.interactor, self.camera)
        self.interactor.AddObserver(vtk.vtkCommand.TimerEvent, cb.execute)
        cb.timerId = self.interactor.CreateRepeatingTimer(15) # Maximum is 60 Hz
        # start the interaction and timer
        self.renwin.Render()
        self.interactor.Start()

