import os
import numpy as np
from PIL import Image

f = [i for i in os.listdir("test_images")]

for t in f:
    for n in [4,6,8]:
        img = np.zeros((2*256,3*256), dtype="uint8")
        k = 0
        for alg in ["RO","DE","PSO"]:
            fname = "segmentations/%s_20_2000_%s_%d/segmented.png" % (t[:-4],alg,n)
            im = np.array(Image.open(fname))
            img[:256,k:(k+256)] = im
            k += 256
        k = 0
        for alg in ["GWO","JAYA","GA"]:
            fname = "segmentations/%s_20_2000_%s_%d/segmented.png" % (t[:-4],alg,n)
            im = np.array(Image.open(fname))
            img[256:,k:(k+256)] = im
            k += 256
        fname = "segmentations/%s_merged_%d.png" % (t[:-4],n)
        Image.fromarray(img).save(fname)

