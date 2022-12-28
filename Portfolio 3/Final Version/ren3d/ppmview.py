#!/usr/bin/python3
# ppmview.py
# by: John Zelle

"""Simple general purpose ppm image viewer

Can be launched as a stand-alone viewer to inspect a file:
    python ppmview.py [filename]
If no filename is given a filedialog is provided.

Can also be invoked through the PPMViewer class, which allows remote
control of a viewing window to display image sent as ppm data.

The viewer runs tkinter in a separate process so non graphical
applications can display an image or sequence of images without being
tkinter aware.

"""

import multiprocessing as mp
import sys


class PPMViewer:

    """Player for a stream of images. The image is updated each time that
    show() is called.
    """

    def __init__(self, title):
        """ spawn separate process for viewing image
        A separate process is necessary so tk calls can be in the main thread

        """

        self.pipe, childconn = mp.Pipe()
        self.process = mp.Process(target=viewer_process,
                                  args=(childconn, title))
        self.process.start()
        childconn.close()

    def show(self, imgdata):
        """ display ppm image from file fname"""
        self.pipe.send(imgdata)

    def isalive(self):
        """return Boolean indicating status of viewer window"""
        return self.process.is_alive()

    def close(self):
        """close viewer window"""
        if self.process.is_alive():
            self.pipe.send("")
            self.process.join()

    def wait(self):
        """wait for viewer to be closed"""
        self.process.join()


def viewer_process(pipe, title):
    # Display image in tk root window
    import tkinter as tk
    root = tk.Tk()
    root.title(title)
    data = pipe.recv()
    img = tk.PhotoImage(format="ppm", data=data, master=root)
    panel = tk.Label(root, image=img)
    panel.pack(side="bottom", fill="both", expand="yes")

    def check_for_update():
        # see if new image data has been sent and display it
        global img
        if pipe.poll():
            data = pipe.recv()
            if data == "":
                sys.exit()
            img = tk.PhotoImage(format='ppm', data=data, master=root)
            panel.configure(image=img)
        root.after(100, check_for_update)

    root.after(0, check_for_update)
    root.mainloop()


if __name__ == "__main__":

    # get filename from command line
    try:
        fname = sys.argv[1]
    except IndexError:
        print("Usage: ppmview.py filename")
        sys.exit()

    # create viewer and display the chosen file
    v = PPMViewer(fname)
    with open(fname, "rb") as infile:
        v.show(infile.read())
