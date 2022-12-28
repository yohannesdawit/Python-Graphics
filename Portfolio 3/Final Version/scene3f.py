# scene3f.py
#   * materials
#   * moveable light
#   * multiple lights
#   * shadows
#   * box texture map

from ren3d.scenedef import *

camera.set_perspective(30, 1.3333, 5)
scene.background = (0, 0, 0)
scene.ambient = (.2, .2, .2)
scene.set_light(pos=(-150, 200, 50), color=(.8, .8, .8))
scene.add_light(pos=(150, 50, 50), color=(.5, .5, .5))

scene.shadows = True
#scene.reflections = 3
scene.textures = True

scene.add(Box(pos=(-3, -2, -20), size=(2, 2, 2),
              color=RED_PLASTIC,
              texture=Boxtexture("textures/wartburg.ppm")))

rsilver = Material(*SILVER)
rsilver.reflect = (.5, .5, .5)
rsilver.diffuse *= .5
rsilver.ambient *= .5
scene.add(Sphere(pos=(2.5, -2, -20), radius=1,
                 color=rsilver))

rbrass = Material(*BRASS)
rbrass.reflect = (.2, .2, .2)
scene.add(Sphere(pos=(0, 0, -25), radius=3,
                 color=rbrass,
                 texture=Boxtexture("textures/globe.ppm")))

bmat = Material((.4, .4, .4), reflect=(.4, .4, .4))
scene.add(Box(pos=(0, -3.5, -20), size=(18, 1, 30),
              color=bmat, texture=Boxtexture("textures/wood.ppm")))
