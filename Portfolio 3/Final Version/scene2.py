# scene2.py

# A single red cube against a gray background. Note: the cube
#     is offset to the left and down to show top and side

from ren3d.scenedef import *

camera.set_perspective(60, 1.3333, 5)
scene.background = (.8, .8, .8)
scene.ambient = (.1, .1, .1)

scene.add(Box(pos=(-3, -2, -10), size=(2, 2, 2), color=(1, 0, 0)))
