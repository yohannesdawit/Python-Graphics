# scene3c.py

from ren3d.scenedef import *

camera.set_perspective(30, 1.3333, 5)
scene.background = (.5, .5, 1)
scene.ambient = (.3, .3, .3)
scene.set_light(pos=(-30, 50, 50), color=(.8, .8, .8))
scene.shadows = True

scene.add(Box(pos=(-3, -2, -20), size=(2, 2, 2), color=RED_PLASTIC))
scene.add(Sphere(pos=(2.5, -2, -20), radius=1, color=SILVER))
scene.add(Sphere(pos=(0, 0, -25), radius=3, color=BRASS))

scene.add(Box(pos=(0, -3.5, -20), size=(18, 1, 30), color=(.45, .4, .15)))
