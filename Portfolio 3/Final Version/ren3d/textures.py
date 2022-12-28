# texture.py
# by yohannes dawit
# simple implementation of texture mapping.

from math import atan2, tau, pi, asin

from ren3d.image import Image
from ren3d.rgb import RGB

def _pixrbg(img, loc):
    return RGB([v/255 for v in img[loc]])

def lerp(v, low0, high0, low1, high1):
    return low1 + (v-low0)*(high1-low1)/(high0-low0)

class Boxtexture:

    def __init__(self, imagefile):
        self.image = Image(imagefile)

    def __call__(self, uvn):
        # skip largest value (mapping to nearest plane)
        coords = list(uvn)
        coords.remove(max(uvn, key=abs))
        u, v = coords
        w, h = self.image.size
        pixel = round((w-1) * (u+1)/2), round((h-1) * (v+1)/2)
        # print("texture pixel", uvn, u, v, pixel)
        return _pixrbg(self.image, pixel)


class Spheretexture:

    def __init__(self, imagefile):
        self.image = Image(imagefile)

    def __call__(self, uvn):
        theta,phi = self._theta_phi(uvn)
        w,h = self.image.size
        x = lerp(phi, 0, tau, 0, w-1)
        y = lerp(theta, -pi/2, pi/2, 0, h-1)
        return _pixrbg(self.image, (round(x), round(y)))

    def _theta_phi(self,uvn):
        x,y,z = uvn
        theta = asin(y)
        phi = -atan2(z,x)
        if z > 0:
            phi += tau
        return theta, phi

