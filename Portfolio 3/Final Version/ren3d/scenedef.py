# scenedef.py
# by yohannes dawit
#    A scene is a collection of modeling elements.
#    This file is the basic "header" needed to define scenes

from __future__ import division, print_function

from ren3d.rgb import RGB
from ren3d.models import Sphere, Group, Box
from ren3d.camera import Camera
from ren3d.math3d import *
from ren3d.materials import *


# ----------------------------------------------------------------------
class Scene(object):

    def __init__(self):
        self.camera = Camera()
        self.surface = Group()
        self.background = (0, 0, 0)
        self.ambient = 0.0
        self.light = (Point([0, 0, 0]), RGB((1,1,1)))


    def add(self, surface):
        self.surface.add(surface)

    @property
    def background(self):
        return self._background

    @background.setter
    def background(self, color):
        self._background = RGB(color)

    @property
    def ambient(self):
        return self._ambient
    
    @ambient.setter
    def ambient(self, color):
        if type(color) == float:
            color = [color] * 3
        self._ambient = RGB(color)

    def set_light(self, pos = (0, 0, 0), color = (0, 1, 0)):
        light = (Point(pos), RGB(color))
        self.light = light

    def add_light(self, pos = (0, 0, 0), color = (0, 1, 0)):
        light = (Point(pos), RGB(color))
        self.light + (light)


# ----------------------------------------------------------------------
# global scene


scene = Scene()
camera = scene.camera


def load_scene(modname):
    if modname.endswith(".py"):
        modname = modname[:-3]
    scene = __import__(modname).scene
    return scene, modname

    

