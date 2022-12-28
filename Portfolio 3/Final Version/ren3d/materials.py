# materials.py
# by yohannes dawit

from __future__ import division, print_function

from ren3d.rgb import RGB


class Material(object):

    def __init__(self, diffuse,         # diffuse (Lambert) coefficients (req.)
                 ambient=None,           # ambient coefficients
                 specular=(.5, .5, .5),  # specular reflection coefficients
                 exponent=30,            # shinyness exponent, higher = shinier
                 reflect=None
                 ):
        if ambient:           # if ambient is not supplied, use diffuse
            self.ambient = ambient
        else:
            self.ambient = diffuse
        self.diffuse = diffuse
        self.specular = specular
        self.exponent = exponent
        self.reflect = reflect

    def __repr__(self):
        return "Material({}, {}, {}, {})".format(*self)

    @property
    def diffuse(self):
        return self._diffuse

    @diffuse.setter
    def diffuse(self, value):
        self._diffuse = RGB(value)

    @property
    def ambient(self):
        return self._ambient

    @ambient.setter
    def ambient(self, value):
        self._ambient = RGB(value)

    @property
    def specular(self):
        return self._specular

    @specular.setter
    def specular(self, value):
        self._specular = RGB(value)

    @property
    def exponent(self):
        return self._exponent

    @exponent.setter
    def exponent(self, value):
        self._exponent = value

    @property
    def reflect(self):
        return self._reflect

    @reflect.setter
    def reflect(self, value):
        self._reflect = RGB(value) if value else None
        

    def __iter__(self):
        yield self.diffuse
        yield self.ambient
        yield self.specular
        yield self.exponent
        yield self.reflect


# ------------------------------------------------------------
# example materials from Computer Graphics Using OpenGL, by F.S. Hill

BLACK_PLASTIC = Material(diffuse=(.01, .01, .01), ambient=(0, 0, 0),
                         specular=(.5, .5, .5), exponent=32)

RED_PLASTIC = Material(diffuse=(.6, 0, 0), ambient=(.3, 0, 0),
                       specular=(.8, .6, .6), exponent=32)

BRASS = Material((.780392, .568627, .113725), (.329412, .223529, .027451),
                 (.992157, .941176, .807843), 27.8974)

COPPER = Material((.7038, .27048, .0828), (.19125, .0735, .0225),
                  (.256777, .137622, .086014), 12.8)

GOLD = Material((.75164, .60648, .22648), (.24725, .1995, .0745),
                (.628281, .555802, .366065), 51.2)

SILVER = Material((.50754,)*3, (.19225,)*3, (.508273,)*3, 51.2)

# ----------------------------------------------------------------------
# use make_material to allow default material for scenes that only
# specify colors


def make_material(color):
    if type(color) == Material:
        return color
    else:
        return Material(color)
