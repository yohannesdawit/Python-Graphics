# ray3d.py
#   3D Rays and intervals
# by yohannes dawit


import math
from ren3d.math3d import Point, Vector


class Ray:

    def __init__(self, start, dir):
        """ A ray beginning at start going in direction dir.
        start is a point, and dir is a vector, both are represented
        using a Vector3 object.

        >>> r = Ray(Point([0,1,2]), Vector([1,2,1]))
        >>> r.start
        Point([0.0, 1.0, 2.0])
        >>> r.dir
        Vector([1.0, 2.0, 1.0])
        >>> r = Ray((1,2,3), (4,5,6))
        >>> r.start
        Point([1.0, 2.0, 3.0])
        >>> r.dir
        Vector([4.0, 5.0, 6.0])
        """
        self.start = Point(start)
        self.dir = Vector(dir)

    def __repr__(self):
        """ Returns printable and evalable representation of Ray

        >>> Ray(Point([0,1,2]), Vector([1,2,3]))
        Ray(Point([0.0, 1.0, 2.0]), Vector([1.0, 2.0, 3.0]))
        """

        return "Ray("+str(self.start)+", "+str(self.dir)+")"

    def point_at(self, t):
        """ returns point on ray at time t

        >>> r = Ray(Point([0,1,2]), Vector([1,2,3]))
        >>> r.point_at(0)
        Point([0.0, 1.0, 2.0])
        >>> r.point_at(1)
        Point([1.0, 3.0, 5.0])
        >>> r.point_at(3.75)
        Point([3.75, 8.5, 13.25])
        """
        return self.start + t*self.dir

# ----------------------------------------------------------------------


class Interval:

    """Simple representation of an open interval"""

    def __init__(self, low=0.0, high=math.inf):
        """
        >>> myInterval = Interval()
        >>> myInterval.low
        0.0
        >>> myInterval.high
        inf
        >>> myInterval = Interval(.001,200)
        >>> myInterval.low
        0.001
        >>> myInterval.high
        200.0
        """
        self.low = float(low)
        self.high = float(high)
        
    def __repr__(self):
        """
        >>> Interval()
        Interval(0.0, inf)
        >>> Interval(0.5, 200)
        Interval(0.5, 200.0)
        """
        return "Interval("+str(self.low)+", "+str(self.high)+")"

    def __contains__(self, t):
        """ returns True iff t is inside this interval (excluding endpoints)
        >>> inter = Interval(2,100)
        >>> 0 in inter
        False
        >>> 5 in inter
        True
        >>> 100 in inter
        False
        """
        return self.low < t < self.high

    def set(self, low, high):
        """ set endpoints of interval to low and high
        >>> inter = Interval()
        >>> inter.set(3.1, 4.5)
        >>> inter.low
        3.1
        >>> inter.high
        4.5
        """
        self.low = low
        self.high = high


if __name__ == "__main__":
    import doctest
    doctest.testmod()
