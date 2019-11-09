import numpy as np
from vispy import visuals, scene
from vispy.visuals.transforms import STTransform
from scipy.spatial.transform import Rotation as R

class figure3D():

    def __init__(self, bgcolor='white', size=(800, 600)):
        self.canvas = scene.SceneCanvas(keys='interactive', bgcolor=bgcolor, size=(800, 600), show=True)
        self.view = self.canvas.central_widget.add_view()
        self.view.camera = 'turntable'
        self.range = 4
        self.camera_range = [-self.range, self.range]
        self.view.camera.set_range(x=self.camera_range, y=self.camera_range, z=self.camera_range)

    def render(self):
        self.canvas.show(run=True)

    def add_sphere(self, name='sphere1', center=[0, 0, 0], orientation=[0, 0, 0], radius=5.2, color='blue', transparency=0.8, contours='latitude'):
        sphere = scene.visuals.Sphere(radius=radius, method='latitude', cols=30, rows=30, parent=self.view.scene, edge_color=color)
        sphere.transform = STTransform(translate=center)
        sphere.set_gl_state('translucent', depth_test=False)

    def add_axes(self, name='axes1', origin=[0, 0, 0], orientation=[0, 0, 0], length=1, color='black', arrow_type='triangle_30'):
        rot = R.from_euler('zyx', -np.array(orientation), degrees=True)
        dcm = rot.as_dcm()
        reference = np.eye(3) * length
        dcm = np.matmul(dcm, reference)
        pos = np.array([[origin[0], origin[1], origin[2]], [origin[0] + dcm[0, 0], origin[1] + dcm[0, 1], origin[2] + dcm[0, 2]],
                        [origin[0], origin[1], origin[2]], [origin[0] + dcm[1, 0], origin[1] + dcm[1, 1], origin[2] + dcm[1, 2]],
                        [origin[0], origin[1], origin[2]], [origin[0] + dcm[2, 0], origin[1] + dcm[2, 1], origin[2] + dcm[2, 2]]])
        arrows = np.array([[origin[0], origin[1], origin[2], origin[0] + dcm[0, 0], origin[1] + dcm[0, 1], origin[2] + dcm[0, 2]],
                        [origin[0], origin[1], origin[2], origin[0] + dcm[1, 0], origin[1] + dcm[1, 1], origin[2] + dcm[1, 2]],
                        [origin[0], origin[1], origin[2], origin[0] + dcm[2, 0], origin[1] + dcm[2, 1], origin[2] + dcm[2, 2]]])
        axes = scene.visuals.Arrow(pos=pos, color=color, parent=self.view.scene, width=4, connect='segments', method='gl', antialias=True, arrows=arrows, arrow_type=arrow_type, arrow_size=1, arrow_color=color)