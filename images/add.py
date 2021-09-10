#
#  file:  add.py
#
#  Add a stack of images
#
#  RTK, 04-Jan-2020
#  Last update:  04-Jan-2020
#
################################################################

import os
import sys
import numpy as np
from PIL import Image

def main():
    """Add a stack of registered grayscale images"""

    if (len(sys.argv) == 1):
        print()
        print("add <src> <output>")
        print()
        print("  <src>     - source directory")
        print("  <output>  - output image file")
        print()
        return

    simgs = [os.path.abspath(sys.argv[1]+"/"+i) for i in os.listdir(sys.argv[1])]
    oname = sys.argv[2]

    img = np.array(Image.open(simgs[0]))
    x,y = img.shape

    oimg = np.zeros((x,y))

    for s in simgs:
        img = np.array(Image.open(s))
        oimg += img

    oimg = oimg / oimg.max()
    Image.fromarray((255.0*oimg).astype("uint8")).save(oname)


main()

