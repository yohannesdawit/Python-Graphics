# run_rt.py -- raytrace a scene with a simple progress indicator
#    usage: pypy run_rt.py scene0 320 240

import sys
import time

from ren3d.scenedef import load_scene
from ren3d.render_ray import raytrace
from ren3d.image import Image


class Progress:

    def __init__(self, size):
        self.size = size
        self.count = 0

    def show(self):
        self.count += 1
        print(str(round(self.count/self.size*100, 1))+"%", end="\r")
        sys.stdout.flush()


def main():
    scene, scenename = load_scene(sys.argv[1])
    w, h = int(sys.argv[2]), int(sys.argv[3])
    img = Image((w, h))
    t1 = time.time()
    raytrace(scene, img, Progress(h).show)
    t2 = time.time()
    img.save("images/{}-rt-{:d}-{:d}.ppm".format(scenename, w, h))
    img.show()
    print(t2-t1, "seconds")
    input("Press <Enter> to quit")
    img.unshow()


if __name__ == "__main__":
    main()
