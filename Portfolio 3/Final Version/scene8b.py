# scene8a.py

from ren3d.scenedef import *

g = Transformable(Box(color=Material((.3, .2, .4)))).scale(150, 2, 150)
scene.add(g)

tp = Transformable(Mesh("teapot.off", SILVER,
                        smooth=True, recenter=True))
tp.scale(50, 50, 50).rotate_x(-90).translate(0, 25, 0)
scene.add(tp)

camera.set_perspective(40, 1.0, 3)
camera.set_view((0, 75, 200), (0, 0, 0), (0, 1, 0))

scene.set_light((60, 100, 100), (1, 1, 1))
scene.ambient = (.5, .5, .5)
scene.background = (0, 0, 0)
scene.shadows = True
