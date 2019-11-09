import croma

fig1 = croma.figure3D(bgcolor='white')
fig1.add_sphere(name='sphere1', center=[0, 0, 0], orientation=[0, 0, 0], radius=0.6, color='blue', transparency=0.8, contours='lat_lon')
fig1.add_axes(name='axes1', origin=[0, 0, 2], orientation=[0, 0, 0], length=1, color='black', arrow_type='triangle_30')
fig1.render()
