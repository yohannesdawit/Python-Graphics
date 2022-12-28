# image.py
#   Class for manipulation of simple raster images
# by: John Zelle


import array

# needed for img.show()
from ren3d import ppmview


class Image:

    r"""Simple raster image. Allows pixel-level access and saving
    and loading as PPM image files.

    Examples:
    >>> img = Image((320, 240))    # create a 320x240 image
    >>> img.size
    (320, 240)
    >>> img[200,200]  # get color at pixel (200,200)
    (0, 0, 0)
    >>> img[200, 100] = (255, 0, 0) # set pixel to bright red
    >>> img[200, 100]   # get color of the pixel back again
    (255, 0, 0)
    >>> img.save("reddot.ppm")    # save image to a ppm file
    >>> img = Image((2, 3))
    >>> img[0,0] = 148, 103, 82
    >>> img[1,2] = 13, 127, 255
    >>> img.getdata()
    b'P6\n2 3\n255\n\x00\x00\x00\r\x7f\xff\x00\x00\x00\x00\x00\x00\x94gR\x00\x00\x00'
    >>> img.load("wartburg.ppm")  # load a ppm image
    >>> img.size
    (640, 470)
    >>> img[350, 220]
    (148, 103, 82)
    >>> img.clear((255,255,255))  # make image all white
    >>> img.save("blank.ppm")     # blank.ppm is 640x470 all white
    """

    def __init__(self, fileorsize):
        """Create an Image from ppm file or create blank Image of given size.
        fileorsize is either a string giving the path to a ppm file or
        a tuple (width, height)
        """

        if type(fileorsize) == str:
            self.load(fileorsize)
        else:
            width, height = fileorsize
            self.size = (width, height)
            self.pixels = array.array("B", [0 for i in range(3*width*height)])
        self.viewer = None

    def _base(self, pos):
        px, py = pos
        w, h = self.size
        return 3*(w*(h-py-1) + px)

    def _legalpos(self, pos):
        i, j = pos
        w, h = self.size
        return 0 <= i < w and 0 <= j < h

    def __setitem__(self, pos, rgb):
        """ Set the color of a pixel.
        pos in a pair (x, y) giving a pixel location where (0, 0) is
            the lower-left pixel
        rgb is a triple of ints in range(256) representing
            the intensity of red, green, and blue for this pixel.
        """
        if self._legalpos(pos):
            r, g, b = rgb
            pixels = self.pixels
            base = self._base(pos)
            pixels[base] = r
            pixels[base+1] = g
            pixels[base+2] = b

    def __getitem__(self, pos):
        """ Get the color of a pixel
        pos is a pair (x, y) giving the pixel location--origin in lower left
        returns a triple (red, green, blue) for pixel color.
        """
        assert self._legalpos(pos)
        base = self._base(pos)
        return tuple(self.pixels[base:base+3])

    def save(self, fname):
        """ Save image as ppm in file called fname """
        with open(fname, "wb") as ofile:
            ofile.write(self.getdata())

    def getdata(self):
        """ Get image information as bytes in ppm format
        """ 
        s = b"P6\n"
        s += "{0} {1}\n".format(*self.size).encode()
        s += b"255\n"
        s += self.pixels.tobytes()
        return s

    def load(self, fname):
        """load raw PPM file from fname.
        Note 1: The width and height of the image will be adjusted
                to match what is found in the file.

        Note 2: This is not a general method for all PPM files, but works for most
        """

        infile = open(fname, "rb")
        magic_number = infile.readline()
        if magic_number != b"P6\n":
            raise ValueError("Not a PPM File: {}".format(fname))

        # get width height
        wstr, hstr = infile.readline().decode().split()
        width = int(wstr)
        height = int(hstr)

        infile.readline()  # skip the maxval

        # The data should be all that's left in fields
        self.pixels = array.array("B")
        self.pixels.fromfile(infile, width*height*3)
        self.size = (width, height)
        infile.close()

    def clear(self, rgb):
        """ set every pixel in Image to rgb
        rgb is a triple: (R, G, B) where R, G, & B are 0-255.
        """
        r, g, b = rgb
        pix = self.pixels
        for i in range(0, len(pix), 3):
            pix[i] = r
            pix[i+1] = g
            pix[i+2] = b

    def show(self):
        """ display image using ppmview """
        if not (self.viewer and self.viewer.isalive()):
            self.viewer = ppmview.PPMViewer("PPM Image")
        self.viewer.show(self.getdata())

    def unshow(self):
        """ close viewing window """
        if self.viewer:
            self.viewer.close()
            self.viewer = None

    def wait_to_close(self):
        if self.viewer:
            self.viewer.wait()


if __name__ == '__main__':
    import doctest
    doctest.testmod()
