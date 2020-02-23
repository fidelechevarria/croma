import croma
from croma.animation import animation

# croma.set_backend('vtk')

fig1 = croma.figure3D(bgcolor='silver')
fig1.add_sphere(center=animation(trajectory=[[0.2, 0, 0], [0.3, 0.3, 0], [0.2, 0, 0]], time=[0, 2, 3], method='linear'),
                radius=animation(trajectory=[[0.2], [0.3]], time=[0, 1]),
                color='AliceBlue',
                opacity=1.0,
                edge_visibility=True)
fig1.add_sphere(center=[0.2, 0, 0.3],
                radius=animation(trajectory=[[0.1], [0.2]], time=[0, 2]),
                color='AliceBlue',
                opacity=1.0,
                edge_visibility=True)
fig1.add_ellipsoid(center=[0, 0, 0],
                   orientation=[0, 0, 0],
                   radius=0.6,
                   color='blue',
                   opacity=0.8,
                   contours='latlon')
# fig1.set_camera(position=[10, 0, 0], focus=[0, 0, 0], roll=20)
fig1.render()
