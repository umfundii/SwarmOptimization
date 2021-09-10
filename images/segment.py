#
#  file:  segment.py
#
#  Use the image histogram to learn cluster centers.
#
#  RTK, 03-Jan-2020
#  Last update:  03-Jan-2020
#
################################################################

import os
import sys
import time
import pickle
import numpy as np
import matplotlib.pylab as plt
from PIL import Image
from sklearn.metrics import silhouette_score

sys.path.append("../")

from PSO import *
from DE import *
from RO import *
from GWO import *
from Jaya import *
from GA import *

from RandomInitializer import *
from SphereInitializer import *
from QuasirandomInitializer import *
from LinearInertia import *
from Bounds import *


################################################################
#  Objective
#
class Objective:
    """Objective function"""

    def __init__(self, img):
        """Constructor"""
        x,y = img.shape
        self.h = np.bincount(img.reshape(x*y), minlength=256)
        self.h = self.h / self.h.sum()
        self.h[0] = self.h[255] = 0
        self.fcount = 0

    def Evaluate(self, p):
        """Evaluate a set of Gaussians"""
        
        self.fcount += 1
        n = len(p) // 3
        c = p.reshape((n,3))
        y = np.zeros(256)
        for x in range(256):
            t = 0.0
            for i in range(n):
                t += c[i,0] * np.exp(-(x-c[i,1])**2/c[i,2]**2)
            y[x] = t
        y = y / y.sum()
        return np.sqrt(((self.h-y)**2).sum())


################################################################
#  PlotFit
#
def PlotFit(p):
    """Plot the Gaussian fit"""

    n = len(p) // 3
    c = p.reshape((n,3))
    y = np.zeros(256)
    for x in range(256):
        t = 0.0
        for i in range(n):
            t += c[i,0] * np.exp(-(x-c[i,1])**2/c[i,2]**2)
        y[x] = t
    y = y / y.sum()
    return y


################################################################
#  SegmentedImage
#
def SegmentedImage(src, p):
    """Return the segmented image and cluster labels"""

    x,y = src.shape
    n = len(p) // 3
    c = p.reshape((n,3))
    labels = np.zeros(x*y, dtype="uint8")
    seg = np.zeros(x*y, dtype="uint8")
    k = 0
    for i in range(x):
        for j in range(y):
            d = np.abs(src[i,j] - c[:,1])
            l = np.argmin(d)
            seg[k] = int(c[l,1])
            labels[k] = l
            k += 1
    return seg.reshape(x,y), labels


################################################################
#  main
#
def main():
    """Cluster grayscale images"""

    if (len(sys.argv) == 1):
        print()
        print("segment <image> <nclusters> <npart> <niter> <alg> RI|SI|QI <output>")
        print()
        print("  <output> - output directory (overwritten)")
        print()
        return

    img = np.array(Image.open(sys.argv[1]).convert("L"))
    nclusters = int(sys.argv[2])
    ndim = nclusters * 3
    npart = int(sys.argv[3])
    niter = int(sys.argv[4])
    alg = sys.argv[5].upper()
    itype = sys.argv[6].upper()
    outdir = sys.argv[7]

    os.system("rm -rf %s; mkdir %s" % (outdir,outdir))

    b = Bounds([0,0,0]*nclusters, [1.0,255,200]*nclusters, enforce="resample")
    if (itype == "QI"):
        i = QuasirandomInitializer(npart, ndim, bounds=b)
    elif (itype == "SI"):
        i = SphereInitializer(npart, ndim, bounds=b)
    else:
        i = RandomInitializer(npart, ndim, bounds=b)

    obj = Objective(img)

    if (alg == "PSO"):
        swarm = PSO(obj=obj, npart=npart, ndim=ndim, init=i, bounds=b, max_iter=niter, inertia=LinearInertia())
    elif (alg == "DE"):
        swarm = DE(obj=obj, npart=npart, ndim=ndim, init=i, bounds=b, max_iter=niter)
    elif (alg == "RO"):
        swarm = RO(obj=obj, npart=npart, ndim=ndim, init=i, bounds=b, max_iter=niter)
    elif (alg == "GWO"):
        swarm = GWO(obj=obj, npart=npart, ndim=ndim, init=i, bounds=b, max_iter=niter)
    elif (alg == "JAYA"):
        swarm = Jaya(obj=obj, npart=npart, ndim=ndim, init=i, bounds=b, max_iter=niter)
    elif (alg == "GA"):
        swarm = GA(obj=obj, npart=npart, ndim=ndim, init=i, bounds=b, max_iter=niter)

    st = time.time()
    swarm.Optimize()
    en = time.time()

    res = swarm.Results()
    pickle.dump(res, open(outdir+"/results.pkl","wb"))

    seg,labels = SegmentedImage(img, res["gpos"][-1])
    Image.fromarray(seg).save(outdir+"/segmented.png")
    Image.fromarray(img).save(outdir+"/original.png")

    y = PlotFit(res["gpos"][-1])
    plt.plot(obj.h)
    plt.plot(y)
    plt.xlabel("Gray Level")
    plt.ylabel("Probability")
    plt.tight_layout(pad=0, w_pad=0, h_pad=0)
    plt.savefig(outdir+"/histogram_plot.png", dpi=300)

    t = img.reshape((img.shape[0]*img.shape[1],1))
    idx = np.argsort(np.random.random(t.shape[0]))
    idx = idx[:int(0.25*len(idx))]
    score = silhouette_score(t[idx], labels[idx], metric="euclidean") 

    s  = "\nSegmentation results:\n\n"
    s += "Optimization minimum squared error %0.6f (time = %0.3f)\n" % (res["gbest"][-1], en-st)
    s += "(%d best updates, %d function evaluations)\n\n" % (len(res["gbest"]), obj.fcount)
    s += "Silhouette score = %0.6f\n\n" % score
    s += "Cluster centers:\n"
    s += np.array2string(res["gpos"][-1].reshape((nclusters,3))) + "\n\n"

    print(s)
    with open(outdir+"/README.txt","w") as f:
        f.write(s)


if (__name__ == "__main__"):
    main()

