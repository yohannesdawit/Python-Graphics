# scene6.py A Triangle test scene
#     This is only for testing the rendering of the (models internal primitive)
#     Triangles are not scene primitives.


from ren3d.scenedef import *

# these imports necessary to test Triangle object
from ren3d.mesh import Triangle
from ren3d.math3d import Point, Vector


points = [Point((-5, 0, -10)), Point((5, 0, -10)), Point((0, 8, -10))]
face_normals = [Vector((0, 0, 1))]*3
vertex_normals = [(p-Point((p.x, 4, -11))).normalized() for p in points]
color = Material((.8, .3, .3))

# uncomment one of the "t = ... "lines to test different normal modes

# This is a flat shaded triangle
#t = Triangle(points, color)

# Also flat
t = Triangle(points, color, face_normals)

# This one should be "bulgy" (like wrapped around a pipe)
#t = Triangle(points, Material((.8, .2, .2), shininess=5), vertex_normals)

scene.add(t)
scene.set_light(pos=(0, 4, 5), color=(.7, .7, .7))
scene.ambient = (.3, .3, .3)

camera.set_perspective(60, 1, 3)
camera.set_view((0, 4, 0), (0, 4, -15))
