# scene9.py

from ren3d.scenedef import *

camera.set_perspective(30, 1.3333, 5)
camera.set_view((-4, 3, 5), (-3, 0, -20))

scene.background = (.05, .05, .2)
scene.set_light(pos=(-30, 50, 5), color=(.8, .8, .8))
scene.add_light(pos=(0, 5, 5), color=(.4, .4, .4))
scene.ambient = (.5, .5, .5)
scene.shadows = True
scene.reflections = 5

white = Material((.9, .9, .9))
scene.add(Sphere(pos=(2.5, -2, -20), radius=1, color=white))

rbrass = Material(*BRASS)
rbrass.reflect = (.2, .2, .2)
scene.add(Sphere(pos=(0, 0, -25), radius=3,
                 color=rbrass))

scene.add(Box(pos=(0, -3.5, -20), size=(18, 1, 30),
              color=Material((.5, .5, .5), reflect=(.1, .1, .1))))

silver = Material(diffuse=(.2, .2, .2), specular=(.6, .6, .6),
                  shininess=100, reflect=(.4, .4, .4))
silver.diffuse = (.2,)*3
teapot = Transformable(
    Mesh("teapot.off", recenter=True, smooth=True, color=silver))
teapot.rotate_x(-90).scale(4, 4, 4).rotate_x(20).translate(-6, -1.1, -23)
scene.add(teapot)
