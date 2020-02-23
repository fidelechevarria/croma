import croma
from croma.animations import linear

# croma.set_backend('vtk')

fig1 = croma.figure3D(bgcolor='silver')
fig1.add_sphere(center=linear([[0.2, 0, 0], [0.3, 0.3, 0]], 3, 60), radius=linear([[0.2], [0.3]], 1, 60), color='blue', opacity=0.6, edge_visibility=True)
fig1.add_sphere(center=[0.2, 0, 0.3], radius=linear([[0.1], [0.2]], 2, 60), color='blue', opacity=1.0, edge_visibility=True)
fig1.add_ellipsoid(center=[0, 0, 0], orientation=[0, 0, 0], radius=0.6, color='blue', opacity=0.8, contours='latlon')
# fig1.set_camera(position=[10, 0, 0], focus=[0, 0, 0], roll=20)
fig1.render()
