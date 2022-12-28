# camera.py
# by yohannes dawit
from math import pi, sin, cos, tan, radians
from ren3d.math3d import *
from ren3d.trans3d import *
from ren3d.ray3d import *


class Camera:
    """Camera is used to specify the view of the scene.

	>>> c = Camera()
	>>> c.set_perspective(60, 1.333, 20)
	>>> c.set_view((1, 2, 3), (0, 0, -10))
	>>> c.trans[0]
	[0.9970544855015816, 0.0, -0.07669649888473705, -0.7669649888473704]
	>>> c.trans[1]
	[-0.01162869315077414, 0.9884389178158018, -0.15117301096006383, -1.5117301096006381]
	>>> c.trans[2]
	[0.07580980435789034, 0.15161960871578067, 0.9855274566525744, -3.335631391747175]
	>>> c.trans[3]
	[0.0, 0.0, 0.0, 1.0]
	>>> c.set_resolution(400, 300)
	>>> r = c.ij_ray(0, 0)
	>>> r.start
	Point([1.0, 2.0, 3.0])
	>>> r.dir
	Vector([-12.900010270830052, -11.566123962675615, -17.521989305329008])
	>>> r = c.ij_ray(100, 200)
	>>> r.start
	Point([1.0, 2.0, 3.0])
	>>> r.dir
	Vector([-7.277823674777881, -0.14976036620738498, -19.7108288275589])
	"""

    def __init__(self):
        self.eye = Point([0, 0, 0])
        self.window = -10.0, -10.0, 10.0, 10.0
        self.distance = 10
        

    def set_perspective(self, hfov, aspect, distance):
        """ Set up perspective view
        hfov is horizontal field of view (in degrees)
        aspect is the aspect ratio horizontal/vertical
        distance is distance from eye to focal plane.

        >>> c = Camera()
        >>> c.set_perspective(60, 1.333, 20)
        >>> c.eye
        Point([0.0, 0.0, 0.0])
        >>> c.distance
        20
        >>> c.window
        (-11.547005383792513, -8.662419642755074, 11.547005383792513, 8.662419642755074)
        """
        w = distance*tan(radians(hfov/2))
        h = w/aspect
        self.window = -w, -h, w, h
        self.distance = distance

    # ------------------------------------------------------------
    # These methods used for ray tracing
    def set_view(self, eye=(0,0,10), lookat=(0,0,0), up=(0,1,0)):
        eyept = Point(eye)
        self.n = (eyept - Point(lookat)).normalized()
        self.u = Vector(up).cross(self.n).normalized()
        self.v = self.n.cross(self.u)
        self.trans = to_uvn(self.u, self.v, self.n, eye)
        self.eye = eyept

    def set_resolution(self, width, height):
        """ Set resolution of pixel sampling across the window.
        """
        l, b, r, t = self.window
        self.dx = (r-l)/width
        self.dy = (t-b)/height

    def ij_ray(self, i, j):
        """ return the ray from the eye through the ijth pixel."""
        

        l, b, r, t = self.window
        x = l + (i+0.5)*self.dx
        y = b + (j+0.5)*self.dy
        start = Point((0, 0, 0))
        end = Point((x, y, -self.distance))
        return Ray(start, end-start)


    
        


if __name__ == "__main__":
    import doctest
    doctest.testmod()

