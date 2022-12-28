# bbox.py
#   basic bounding box
# by: John Zelle

from math import inf
from ren3d.math3d import Point, Vector


class BoundingBox:
    """An axis-aligned box that provides a fast hit test along with
    convenient methods for transformation and expanding a box to
    encompass new objects.

    """

    def __init__(self, low=(inf, inf, inf), high=(-inf, -inf, -inf)):
        self.bounds = Vector(low), Vector(high)
        self.t = None

    def __repr__(self):
        return "BoundingBox({}, {})".format(
            tuple(self.bounds[0]), tuple(self.bounds[1]))

    def hit(self, ray, interval):
        low, high = self.bounds
        lowt, hight = -inf, inf
        s, d = ray.start, ray.dir
        for axis in range(3):
            if d[axis] == 0:
                if s[axis] < low[axis] or s[axis] > high[axis]:
                    return False
            else:
                t1 = ((low[axis] - s[axis]))/d[axis]
                t2 = ((high[axis] - s[axis]))/d[axis]
                if t1 > t2:
                    t1, t2 = t2, t1

                if t1 > lowt:
                    lowt = t1
                if t2 < hight:
                    hight = t2
        self.t = lowt  # save in case intersection time must be known

        # True iff intersection interval overlaps ray's interval of interest
        return (lowt <= hight
                and hight >= interval.low and lowt <= interval.high)

    def include_points(self, points):
        """expand bounds to include points """
      
        low, high = self.bounds
        for p in points:
            for axis in range(3):
                if p[axis] < low[axis]:
                    low[axis] = p[axis]
                if p[axis] > high[axis]:
                    high[axis] = p[axis]

    @property
    def corners(self):
        """ return a list of the corner Points"""
        xs, ys, zs = zip(*self.bounds)
        return [Point((x, y, z)) for x in xs for y in ys for z in zs]

    @property
    def midpoint(self):
        """ return the middle Point of the box """
        low, high = self.bounds
        return Point((low + high)*.5)

    def include_box(self, bbox):
        """expand to encompass bbox"""
        self.include_points(bbox.corners)

    def combine(self, other):
        """returns a new bbox the encloses self and other"""
        box = BoundingBox()
        box.include_box(self)
        box.include_box(other)
        return box

    def transform(self, trans):
        """returns a new bounding box that encloses the transform of this box
        """       
        transed_corners = [pt.transform(trans) for pt in self.corners]
        transed_box = BoundingBox()
        transed_box.include_points(transed_corners)
        return transed_box
