# test7.py
#   Draw barn scene with mesh

from ren3d.scenedef import *

# floor
g = Transformable(Box(color=Material((.3, .8, .2))))
g.scale(150, 5, 150)
scene.add(g)

# haystack
h = Transformable(Sphere(pos=(0, 0, 0), radius=1,
                         color=Material((.6, .7, .2), specular=(0, 0, 0))))
h.scale(15, 25, 15).translate(-40, 5, 40)
scene.add(h)

# the barn
b = Transformable(Mesh("barn.off", Material((.8, 0, 0))))
b.scale(40, 40, 40).rotate_y(-45)
scene.add(b)

# set up the view
camera.set_view((0, 75, 200), (0, 0, 0), (0, 1, 0))
camera.set_perspective(40, 1.0, 3)

scene.set_light((60, 200, 200), (1, 1, 1))
scene.ambient = (.5, .5, .5)
scene.background = (1, 1, 1)
