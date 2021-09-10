import os
import numpy as np
from PIL import Image

os.system("rm -rf frames; mkdir frames")

d = np.load("fmri_images.npy")

for i in range(5,50):
    n = -10 + 20.0*np.random.random()
    im = Image.fromarray((255*(d[i]/(d[i].max()+5))).astype("uint8")).rotate(int(n), resample=Image.BICUBIC)
    x = int(-5 + 10*np.random.random())
    y = int(-5 + 10*np.random.random())
    im = im.transform(im.size, Image.AFFINE, (1, 0, x, 0, 1, y), resample=Image.BICUBIC)
    im.save("frames/frame_%04d.png" % (i-5))

