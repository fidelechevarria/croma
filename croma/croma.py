from scipy.spatial.transform import Rotation as R
import numpy as np
import time
import vtk

class vtkTimerCallback():
    def __init__(self, sources, mappers, actors, callbacks, interactor, camera):
        self.timer_count = 0
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
        maxAnimationTime = 0.0
        for i in range(len(self.callbacks)):
            if self.callbacks[i][3] > maxAnimationTime:
                maxAnimationTime = self.callbacks[i][3]
        self.steps = int(maxAnimationTime * 66.666) + 1

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
            cb = self.callbacks[i][0]
            prop = self.callbacks[i][1]
            idx = self.callbacks[i][2]
            if prop == 'center':
                center = cb(self.time)
                self.sources[idx].SetCenter(center[0], center[1], center[2])
            elif prop == 'radius':
                radius = cb(self.time)
                self.sources[idx].SetRadius(radius)
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

        self.sources = []
        self.mappers = []
        self.actors = []
        self.callbacks = []

    def render(self):
        self.renwin.Render()
        self.interactor.Start()
        self.animate()

    def add_sphere(self, center=[0, 0, 0], radius=0.2, color='AliceBlue', opacity=1.0, contours='latitude', theta_resolution=30, phi_resolution=30, edge_visibility=False, edge_color='SteelBlue'):
        
        if hasattr(radius[0], '__call__'):
            self.callbacks.append([radius[0], 'radius', len(self.sources), radius[1]])
            radius = radius[0](0.0)

        if hasattr(center[0], '__call__'):
            self.callbacks.append([center[0], 'center', len(self.sources), center[1]])
            center = center[0](0.0)

        sphere = vtk.vtkSphereSource()
        sphere.SetCenter(center[0], center[1], center[2])
        sphere.SetRadius(radius)
        sphere.SetThetaResolution(theta_resolution)
        sphere.SetPhiResolution(phi_resolution)
        sphere.SetLatLongTessellation(False)

        # mapper
        mapper = vtk.vtkPolyDataMapper()
        mapper.SetInputConnection(sphere.GetOutputPort())
        mapper.ScalarVisibilityOff()

        actor = vtk.vtkActor()
        actor.SetMapper(mapper)

        actor.GetProperty().SetEdgeVisibility(edge_visibility)
        actor.GetProperty().SetColor(self.colors.GetColor3d(color))
        actor.GetProperty().SetEdgeColor(self.colors.GetColor3d(edge_color))
        actor.GetProperty().SetOpacity(opacity)

        # Append elements
        self.sources.append(sphere)
        self.mappers.append(mapper)
        self.actors.append(actor)

        # add the actor
        self.renderer.AddActor(actor)

        # Initialize must be called prior to creating timer events.
        self.interactor.Initialize()

        return actor

    def add_ellipsoid(self, center=[0, 0, 0], orientation=[0, 0, 0], radius=5.2, color='blue', opacity=1.0, contours='latitude'):
        
        # create an ellipsoid using an implicit quadric
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
        
    def add_axes(self, origin=[0, 0, 2], orientation=[0, 0, 0], length=1, color='black', arrow_type='triangle_30'):

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

    def animate(self, *argv, time=np.inf):
        # Sign up to receive TimerEvent
        cb = vtkTimerCallback(self.sources, self.mappers, self.actors, self.callbacks, self.interactor, self.camera)
        self.interactor.AddObserver(vtk.vtkCommand.TimerEvent, cb.execute)
        cb.timerId = self.interactor.CreateRepeatingTimer(15) # Maximum is 60 Hz
        # start the interaction and timer
        self.renwin.Render()
        self.interactor.Start()

