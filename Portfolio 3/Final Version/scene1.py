# scene1.py
# a bunch of spheres

from ren3d.scenedef import *

from random import random

camera.set_perspective(60, 4/3, 50)
scene.background = (1, 1, 1)
scene.ambient = (.2, .2, .2)

scene.add(Sphere(pos=(0, 300, -1200), radius=200, color=(.8, 0, 0)))
scene.add(Sphere(pos=(-80, 150, -1200), radius=200, color=(0, .8, 0)))
scene.add(Sphere(pos=(70, 100, -1200), radius=200, color=(0, 0, .8)))

for x in range(-2, 3):
    for z in range(2, 8):
        scene.add(Sphere(pos=(x*200, -300, z * -400),
                         radius=40,
                         color=(random()*.8, random()*.8, random()*.8)))
