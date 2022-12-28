# models.py
#   Objects used for constructing scenes
# by: John Zelle

from math import sin, cos, pi, sqrt, tau, acos, atan, atan2
from ren3d.math3d import Point, Vector
from ren3d.rgb import RGB
from ren3d.materials import *


# Surfaces for Scene Modeling
# ----------------------------------------------------------------------
class Box:

    def __init__(self, pos=(0.0, 0.0, 0.0), size=(1, 1, 1), color=(0,0,0)):
        self.planes = [(pos[i]-size[i]/2, pos[i]+size[i]/2) for i in range(3)]
        self.color = make_material(color)

    def iter_polygons(self):
        ijseq = [(0, 0), (1, 0), (1, 1), (0, 1)]
        xs, ys, zs = self.planes
        yield Record(points=[Point((xs[0], ys[i], zs[j])) for i, j in ijseq],
                     normals=[Vector((-1, 0, 0))]*4, color=self.color)
        yield Record(points=[Point((xs[1], ys[i], zs[j])) for i, j in ijseq],
                     normals=[Vector((1, 0, 0))]*4, color=self.color)
        yield Record(points=[Point((xs[i], ys[0], zs[j])) for i, j in ijseq],
                     normals=[Vector((0, -1, 0))]*4, color=self.color)
        yield Record(points=[Point((xs[i], ys[1], zs[j])) for i, j in ijseq],
                     normals=[Vector((0, 1, 0))]*4, color=self.color)
        yield Record(points=[Point((xs[i], ys[j], zs[0])) for i, j in ijseq],
                     normals=[Vector((0, 0, -1))]*4, color=self.color)
        yield Record(points=[Point((xs[i], ys[j], zs[1])) for i, j in ijseq],
                     normals=[Vector((0, 0, 1))]*4, color=self.color)

    def intersect(self, ray, interval, info):
        s, d = ray.start, ray.dir
        planes = self.planes
        hit = False
        for axis in range(3):
            if d[axis] == 0.0:
                continue
            for lh in range(2):
                t = (planes[axis][lh] - s[axis])/d[axis]
                if t not in interval:
                    continue
                p = ray.point_at(t)
                if self._inrect(p, axis):
                    hit = True
                    interval.high = t
                    info.t = t
                    info.point = p
                    info.normal = Vector([0]*3)
                    info.normal[axis] = (-1.0, 1.0)[lh]
                    info.color = self.color
        return hit

    def _inrect(self, p, axis):
        axes = [0, 1, 2]
        axes.remove(axis)
        for a in axes:
            low, high = self.planes[a]
            if not low <= p[a] <= high:
                return False
        return True


class Sphere:
    """ Model of a sphere shape
    """

    def __init__(self, pos=(0, 0, 0), radius=1,
                 color=(0, 1, 0), nlat=15, nlong=15):
        """ create a sphere
        """
        self.pos = Point(pos)
        self.radius = radius
        self.color = make_material(color)
        self.nlat = nlat
        self.nlong = nlong
        self._make_bands(nlat, nlong)
        axis = Vector((0, radius, 0))
        self.northpole = self.pos + axis
        self.southpole = self.pos - axis

    def _make_bands(self, nlat, nlong):
        # helper method that creates a list of "bands" where each band consists
        #  of a list of points encircling the sphere at a latitude. There
        #  are nlat evenly (angularly) spaced bands each with nlong points
        #  evenly spaced around the band.

        def circle2d(c, r, n):
            cx, cy = c
            dt = tau/n
            points = [(r*cos(i*dt)+cx, r*sin(i*dt)+cy) for i in range(n)]
            points.append(points[0])  # complete the loop back to first
            return points

        cx, cy, cz = self.pos
        bands = []
        theta = pi/2
        dtheta = -pi/(nlat+1)
        for i in range(nlat):
            theta += dtheta
            r = self.radius*cos(theta)
            y = self.radius*sin(theta) + cy
            band = [Point((x, y, z))
                    for x, z in circle2d((cx, cz), r, nlong)]
            bands.append(band)
        self.bands = bands

    def iter_polygons(self):
        bands = self.bands
        # arctic
        b = bands[0]
        for i in range(self.nlong):
            points = (self.northpole, b[i], b[i+1])
            yield Record(points=points, color=self.color,
                         normals=[self.normal_at(p) for p in points])
        # inter-latitudes
        for b in range(len(bands)-1):
            b0 = bands[b]
            b1 = bands[b+1]
            for i in range(self.nlong):
                quad = b0[i], b1[i], b1[i+1], b0[i+1]
                yield Record(points=quad, color=self.color,
                             normals=[self.normal_at(p) for p in quad])
        # antarctic
        b = bands[-1]
        for i in range(self.nlong):
            points = (self.southpole, b[i+1], b[i])
            yield Record(points=points, color=self.color,
                         normals=[self.normal_at(p) for p in points])

    def normal_at(self, pt):
        n = (pt-self.pos)
        n.normalize()
        return n

    def intersect(self, ray, interval, info):
        """ returns a True iff ray intersects the sphere within the

        given time interval. The approriate intersection information
        is recorded into info, which is a Record containing:
          point: the point of intersection
          t: the time of the intersection
          normal: the surface normal at the point
          color: the color at the point.
        """

        dir = ray.dir
        r = self.radius
        s_p = ray.start-self.pos

        a = dir.mag2()
        b = 2 * dir.dot(s_p)
        c = s_p.mag2() - r*r
        discrim = b*b - 4 * a * c
        if discrim <= 0:
            return False

        discrt = sqrt(discrim)
        t = (-b - discrt)/(2*a)
        if t in interval:
            self._setinfo(ray, t, info)
            return True
        else:
            t = (-b + discrt)/(2*a)
            if t in interval:
                self.setinfo(ray, t, info)
                return True
        return False

    def _setinfo(self, ray, t, info):
        # helper method to fill in the info record
        p = ray.point_at(t)
        info.point = p
        info.t = t
        info.color = self.color
        info.normal = self.normal_at(p)


class Group:
    """ Model comprised of a group of other models.
    The contained models may be primitives (such as Sphere) or other groups.
    """

    def __init__(self):
        self.objects = []

    def add(self, model):
        """Add model to the group
        """
        self.objects.append(model)

    def iter_polygons(self):
        for obj in self.objects:
            for poly in obj.iter_polygons():
                yield poly

    def intersect(self, ray, interval, info):
        """Returns True iff ray intersects some object in the group

        If so, info is the record of the first (in time) object hit, and
        interval.max is set to the time of the first hit.
        """
        hit = False
        for obj in self.objects:
            if obj.intersect(ray, interval, info):
                interval.high = info.t
                hit = True
        return hit


# ----------------------------------------------------------------------
class Record(object):
    """ conveience for bundling a bunch of info together. Basically
    a dictionary that can use dot notatation

    >>> info = Record()
    >>> info.point = Point([1,2,3])
    >>> info
    Record(point=Point([1.0, 2.0, 3.0]))
    >>> info.t = 3.245
    >>> info
    Record(point=Point([1.0, 2.0, 3.0]), t=3.245)
    >>> info.update(point=Point([-1,0,0]), t=5)
    >>> info.t
    5
    >>> info
    Record(point=Point([-1.0, 0.0, 0.0]), t=5)
    >>> info2 = Record(whatever=53, whereever="Iowa")
    >>> info2.whereever
    'Iowa'
    >>> 
    """

    def __init__(self, **items):
        self.__dict__.update(items)

    def update(self, **items):
        self.__dict__.update(**items)

    def __repr__(self):
        d = self.__dict__
        fields = [k+"="+str(d[k]) for k in sorted(d)]
        return "Record({})".format(", ".join(fields))


if __name__ == "__main__":
    import doctest
    doctest.testmod()
