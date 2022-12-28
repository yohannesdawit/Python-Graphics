# run_art.py -- raytrace a scene with a wireframe preview and animated
#   filling in. It's (much) slower, but more fun.
# usage: pypy run_art.py scene0 320 240


import sys
import time

from ren3d.image import Image
from ren3d.render_oo import render_wireframe
from ren3d.render_ray import raytrace
from ren3d.scenedef import load_scene


def main():
    scene, scenename = load_scene(sys.argv[1])
    w, h = int(sys.argv[2]), int(sys.argv[3])
    img = Image((w, h))
    t1 = time.time()
    render_wireframe(scene, img)
    t2 = time.time()
    raytrace(scene, img, img.show)
    t3 = time.time()
    img.save("images/{}-rt-{:d}-{:d}.ppm".format(scenename, w, h))
    print("time: {:0.1f} s\npreview: {:0.1f} s, raytrace: {:0.1f} s".format(
        t3-t1, t2-t1, t3-t2))
    input("Press <Enter> to quit")
    img.unshow()


if __name__ == "__main__":
    main()
