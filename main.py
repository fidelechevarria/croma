import croma

fig1 = croma.figure3D(bgcolor='Silver')
sph = fig1.add_sphere(name='sphere1', center=[0, 0, 0], orientation=[0, 0, 0], radius=0.6, color='blue', transparency=0.8, contours='lat_lon')
# fig1.render()
fig1.add_ellipsoid(name='ellipsoid1', center=[0, 0, 0], orientation=[0, 0, 0], radius=0.6, color='blue', transparency=0.8, contours='lat_lon')
# fig1.render()
# fig1.add_axes(name='axes1', origin=[0, 0, 0], orientation=[0, 0, 0], length=1, color='black', arrow_type='triangle_30')
fig1.render()

from croma.callbacks import centerCallback

fig1.animate('sphere1', 'center', centerCallback,
             'ellipsoid1', 'center', centerCallback)

# fig1.animate('sphere1', 'center', centerCallback,
#              'sphere1', 'radius', radiusCallback, time=inf) # Los callbacks tienen que tener información de tiempo para poder hacer visualizaciones en tiempo real.
# fig1.animate('axes1', 'orientation', orientationCallback, time=5)

# fig1.update('sphere1', 'center', position,
#             'sphere1', 'radius', radius)
# fig1.update('axes1', 'orientation', orientation)