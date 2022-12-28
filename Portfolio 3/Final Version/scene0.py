# scene0.py

# A single green sphere against a white background

from ren3d.scenedef import *

camera.set_perspective(60, 1.3333, 5)
scene.background = (1, 1, 1)

scene.add(Sphere(pos=(0, 0, -10), radius=2, color=(0, .8, 0)))
