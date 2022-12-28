# render_ray.py
# by yohannes dawit



from math import * 
from ren3d.ray3d import *
from ren3d.math3d import *
from ren3d.models import *
from ren3d.rgb import RGB


def raytrace(scene, img, updatefn=None):
    """basic raytracing algorithm to render scene into img
    """
    camera = scene.camera
    w, h = img.size
    camera.set_resolution(w, h)
    for j in range(h):
        for i in range(w):
            ray = camera.ij_ray(i, j)
            color = raycolor(scene, ray, Interval())
            img[i, j] = color.quantize(255)
        if updatefn:
            updatefn()


def raycolor(scene, ray, interval):
    """returns the color of ray in the scene
    """

    info = Record()
    lpos, lcol = scene.light
    if scene.surface.intersect(ray, interval, info):
        color = scene.ambient.times(info.color.ambient)
        if not shadow(scene, info.point, lpos):
            lvec = (scene.camera.eye-info.point).normalized()
            lambert = max(0, lvec.dot(info.normal))
            color += info.color.diffuse.times(lcol) * lambert

            v = -ray.dir.normalized()
            h = (lvec + v).normalized()
            specular = (max(0, h.dot(info.normal)))**info.color.exponent
            color += info.color.specular.times(lcol) * specular
        return scene.ambient + lambert * info.color
    else:
        return scene.background

def shadow(scene, hitpt, light):
    r_start = hitpt
    r_dir = (light - hitpt)
    r_inter = Interval(EPSILON, 1)
    return scene.surface.intersect(Ray(r_start,r_dir), r_inter, Record()) 


    
