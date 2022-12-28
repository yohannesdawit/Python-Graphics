# trans3d.py
# yohannes dawit
"""matrices for performing 3D transformations in homogeneous coordinates"""

from math import radians, sin, cos, tan
from ren3d.math3d import Point, Vector
import ren3d.matrix as mat


def translate(dx=0., dy=0., dz=0.):
    """ returns matrix that translates by dx, dy, dz

    >>> translate(2,1,3)
    [[1.0, 0.0, 0.0, 2.0], [0.0, 1.0, 0.0, 1.0], [0.0, 0.0, 1.0, 3.0], [0.0, 0.0, 0.0, 1.0]]
    """
    trans_mat = mat.unit(4)
    trans_mat[0][3] = float(dx)
    trans_mat[1][3] = float(dy)
    trans_mat[2][3] = float(dz)

    return trans_mat


def scale(sx=1., sy=1., sz=1.):
    """ returns matrix that scales by sx, sy, sz

    >>> scale(2,3,4)
    [[2.0, 0.0, 0.0, 0.0], [0.0, 3.0, 0.0, 0.0], [0.0, 0.0, 4.0, 0.0], [0.0, 0.0, 0.0, 1.0]]
    >>>
    """
    scale_mat = mat.unit(4)
    scale_mat[0][0] = float(sx)
    scale_mat[1][1] = float(sy)
    scale_mat[2][2] = float(sz)

    return scale_mat


def rotate_x(angle):
    """ returns matrix that rotates angle degrees about X axis

    >>> rotate_x(30)
    [[1.0, 0.0, 0.0, 0.0], [0.0, 0.8660254037844387, -0.49999999999999994, 0.0], [0.0, 0.49999999999999994, 0.8660254037844387, 0.0], [0.0, 0.0, 0.0, 1.0]]
    """
    rot_mat = mat.unit(4)
    rot_mat[1][1], rot_mat[1][2] = cos(radians(angle)), -sin(radians(angle))
    rot_mat[2][1], rot_mat[2][2] = sin(radians(angle)), cos(radians(angle))

    return rot_mat


def rotate_y(angle):
    """ returns matrix that rotates by angle degrees around the Y axis

    >>> rotate_y(30)
    [[0.8660254037844387, 0.0, 0.49999999999999994, 0.0], [0.0, 1.0, 0.0, 0.0], [-0.49999999999999994, 0.0, 0.8660254037844387, 0.0], [0.0, 0.0, 0.0, 1.0]]
    """
    rot_mat = mat.unit(4)
    rot_mat[0][0], rot_mat[0][2] = cos(radians(angle)), sin(radians(angle))
    rot_mat[2][0], rot_mat[2][2] = -sin(radians(angle)), cos(radians(angle))

    return rot_mat

def rotate_z(angle):
    """returns a matrix that rotates by angle degrees around Z axis

    >>> rotate_z(30)
    [[0.8660254037844387, -0.49999999999999994, 0.0, 0.0], [0.49999999999999994, 0.8660254037844387, 0.0, 0.0], [0.0, 0.0, 1.0, 0.0], [0.0, 0.0, 0.0, 1.0]]
    """
    rot_mat = mat.unit(4)
    rot_mat[0][0], rot_mat[0][1] = cos(radians(angle)), -sin(radians(angle))
    rot_mat[1][0], rot_mat[1][1] = sin(radians(angle)), cos(radians(angle))

    return rot_mat


def to_uvn(u, v, n, eye):
    """returns a matrix that transforms a point to UVN coordinates

    >>> to_uvn(Vector([1.0, 2.0, 3.0]), Vector([4.0, 5.0, 6.0]), Vector([7.0, 8.0, 9.0]), Vector([10.0, 11.0, 12.0]))
    [[1.0, 2.0, 3.0, -68.0], [4.0, 5.0, 6.0, -167.0], [7.0, 8.0, 9.0, -266.0], [0, 0, 0, 1]]
    """
    rot_mat = mat.unit(4)
    rot_mat[0][0],rot_mat[0][1],rot_mat[0][2],rot_mat[0][3] = u.x, u.y, u.z, -u.dot(eye)
    rot_mat[1][0],rot_mat[1][1],rot_mat[1][2],rot_mat[1][3] = v.x, v.y, v.z, -v.dot(eye)
    rot_mat[2][0],rot_mat[2][1],rot_mat[2][2],rot_mat[2][3] = n.x, n.y, n.z, -n.dot(eye)
    
    return rot_mat


if __name__ == '__main__':
    import doctest
    doctest.testmod()
