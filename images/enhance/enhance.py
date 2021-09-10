#
#  file:  enhance.py
#
#  Use local image enhancement similar to:
#       "Gray-level Image Enhancement By Particle Swarm Optimization"
#       (Gorai and Ghosh, 2009)
#
#  with a different objective function based on sharpness
#  and entropy.
#
#  RTK, 02-Sep-2020
#  Last update:  08-Sep-2020
#
################################################################

import pickle
import os
import sys
import time
import numpy as np
from PIL import Image, ImageFilter
from skimage.exposure import rescale_intensity

sys.path.append("../../")

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
#  ApplyEnhancement
#
def ApplyEnhancement(g, a,b,c,k):
    """Enhance an image"""

    def val(a,b,r,c):
        if (a<0) or (a>=r) or (b<0) or (b>=c):
            return False
        return True

    def valid3(g,i,j):
        r,c = g.shape
        v = []
        if val(i-1,j-1,r,c):  v.append(g[i-1,j-1])
        if val(i-1,j,r,c):    v.append(g[i-1,j])
        if val(i-1,j+1,r,c):  v.append(g[i-1,j+1])
        if val(i,j-1,r,c):    v.append(g[i,j-1])
        if val(i,j,r,c):      v.append(g[i,j])
        if val(i,j+1,r,c):    v.append(g[i,j+1])
        if val(i+1,j-1,r,c):  v.append(g[i+1,j-1])
        if val(i+1,j,r,c):    v.append(g[i+1,j])
        if val(i+1,j+1,r,c):  v.append(g[i+1,j+1])
        return np.array(v)

    def mean(g,i,j):
        return valid3(g,i,j).mean()

    def sigma(g,i,j):
        return valid3(g,i,j).std(ddof=1)

    #  enhanced image
    rows,cols = g.shape
    dst = np.zeros((rows,cols))

    #  enhance
    for i in range(rows):
        for j in range(cols):
            m,s = mean(g,i,j), sigma(g,i,j)
            dst[i,j] = ((k*g.mean())/(s+b))*(g[i,j]-c*m)+m**a

    #  return enhanced image
    return rescale_intensity(dst, out_range=(0,255)).astype("uint8")


################################################################
#  Objective
#
class Objective:
    """Enhancement objective function"""

    def __init__(self, img):
        """Constructor"""

        self.img = img.copy()
        self.fcount = 0

    def F(self, dst):
        """Objective function from the paper"""
        
        r,c = dst.shape

        Is = Image.fromarray(dst).filter(ImageFilter.FIND_EDGES) 
        Is = np.array(Is)
        edgels = len(np.where(Is.ravel() > 20)[0])

        h = np.histogram(dst, bins=64)[0]
        p = h / h.sum()
        i = np.where(p != 0)[0]
        ent = -(p[i]*np.log2(p[i])).sum()
        
        F = np.log(np.log(Is.sum()))*(edgels/(r*c))*ent
        return F

    def Evaluate(self, p):
        """Apply a set of parameters"""

        self.fcount += 1
        a,b,c,k = p
        dst = ApplyEnhancement(self.img, a,b,c,k)
        return -self.F(dst)


################################################################
#  main
#
def main():
    """Learn a LUT"""

    if (len(sys.argv) == 1):
        print()
        print("enhance <src> <npart> <niter> <alg> RI|SI|QI <output>")
        print()
        print("  <src>    - source grayscale image")
        print("  <npart>  - number of particles")
        print("  <niter>  - number of iterations")
        print("  <alg>    - RO,DE,PSO,Jaya,GWO,GA")
        print("  RI|SI|QI - initializer type")
        print("  <output> - output directory (overwritten)")
        print()
        return

    src = sys.argv[1]
    npart = int(sys.argv[2])
    niter = int(sys.argv[3])
    alg = sys.argv[4].upper()
    itype = sys.argv[5].upper()
    outdir = sys.argv[6]

    orig = np.array(Image.open(src).convert("L"))
    img = orig / 256.0

    os.system("rm -rf %s; mkdir %s" % (outdir,outdir))

    ndim = 4  # a,b,c,k

    #  limits from the paper w/expanded b range
    b = Bounds([0.0,1.0,0.0,0.5], [1.5,22,1.0,1.5], enforce="resample")

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

    s = "\nIterations:\n\n"

    st = time.time()
    k = 0
    swarm.Initialize()
    while (not swarm.Done()):
        swarm.Step()
        res = swarm.Results()
        t = "    %5d: gbest = %0.8f" % (k,res["gbest"][-1])
        print(t, flush=True)
        s += t+"\n"
        k += 1
    en = time.time()

    res = swarm.Results()
    pickle.dump(res, open(outdir+"/results.pkl","wb"))

    s += "\nSearch results: %s, %d particles, %d iterations, %s\n\n" % (alg, npart, niter, itype)
    s += "Optimization minimum %0.8f (time = %0.3f)\n" % (res["gbest"][-1], en-st)
    s += "(%d best updates, %d function evaluations)\n\n" % (len(res["gbest"]), obj.fcount)

    print(s)
    with open(outdir+"/README.txt","w") as f:
        f.write(s)

    #  Apply the enhancement
    a,b,c,k = res["gpos"][-1]
    dst = ApplyEnhancement(img, a,b,c,k)
    Image.fromarray(dst).save(outdir+"/enhanced.png")
    Image.fromarray(orig).save(outdir+"/original.png")


if (__name__ == "__main__"):
    main()

