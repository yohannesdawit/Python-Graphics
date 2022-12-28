# scene3.py

# 3 objects on a table, against a light yellow background

from random import random
from ren3d.scenedef import *

camera.set_perspective(30, 1.3333, 5)
scene.background = (.8, .8, .7)

scene.add(Box(pos=(-3, -2, -20), size=(2, 2, 2), color=(.8, 0, 0)))
scene.add(Sphere(pos=(2.5, -2, -20), radius=1, color=(0, .8, 0)))
scene.add(Sphere(pos=(0, 0, -25), radius=3,
                 color=(random(), random(), random())))

scene.add(Box(pos=(0, -3.5, -20), size=(18, .5, 18), color=(.9, .8, .3)))
