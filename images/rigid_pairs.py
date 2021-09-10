#
#  file:  rigid_pairs.py
#
#  Apply rigid registration to pairs of images
#
#  RTK, 10-Sep-2020
#  Last update:  10-Sep-2020
#
################################################################

import os
import sys
import time
import pickle
import numpy as np
from PIL import Image
from scipy.ndimage import rotate, shift

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
from Bounds import *
from LinearInertia import *


################################################################
#  NMI
#
def NMI(a,b):
    """Normalized mutual information between two grayscale images"""
    
    h = np.histogram2d(a.ravel(),b.ravel(), bins=20)[0]
    pxy = h / h.sum() 
    px = pxy.sum(axis=0)
    py = pxy.sum(axis=1)
    hx = -(px*np.log2(px+1e-9)).sum()
    hy = -(py*np.log2(py+1e-9)).sum()
    hxy= -(pxy*np.log2(pxy+1e-9)).sum()
    return (hx+hy) / hxy


################################################################
#  Objective
#
class Objective:
    """Objective function"""

    def __init__(self, dname, sname):
        """Constructor"""
        
        self.dst = np.array(Image.open(dname).convert("L"))
        self.src = np.array(Image.open(sname).convert("L"))
        self.x, self.y = self.dst.shape

    def Evaluate(self, p):
        """Evaluate a rotation and translation"""
        
        angle, xshift, yshift = p
        img = rotate(shift(self.src, (xshift,yshift)), angle).astype("uint8")
        x,y = img.shape
        img = img[(x//2-self.x//2):(x//2+self.x//2),(y//2-self.y//2):(y//2+self.y//2)]
        if (img.shape[0] != self.dst.shape[0]) or (img.shape[1] != self.dst.shape[1]):
            return 1e9
        return -NMI(self.dst, img)


################################################################
#  ApplyRegistration
#
def ApplyRegistration(dname, sname, p):
    """Apply a registration"""

    dst = np.array(Image.open(dname).convert("L"))
    X,Y = dst.shape
    src = np.array(Image.open(sname).convert("L"))
    angle, xshift, yshift = p
    img = rotate(shift(src, (xshift,yshift)), angle).astype("uint8")
    x,y = img.shape
    img = img[(x//2-X//2):(x//2+X//2),(y//2-Y//2):(y//2+Y//2)]
    return img


################################################################
#  main
#
def main():
    """Register images together"""

    if (len(sys.argv) == 1):
        print()
        print("rigid <src0> <src1> <output> <npart> <niter> <alg> RI|SI|QI")
        print()
        print("  <src0>, <src1> - source directories of image pairs (sorted alphabetically)")
        print("  <output> - output images and files directory (overwritten)")
        print("  <npart>  - number of particles")
        print("  <niter>  - number of iterations (max)")
        print("  <alg>    - algorithm: PSO,DE,RO,GWO,JAYA,GA")
        print("  RI|SI|QI - initializer type")
        print()
        return

    sdir0= sys.argv[1]
    sdir1= sys.argv[2]
    outdir = sys.argv[3]
    npart = int(sys.argv[4])
    ndim = 3 # (angle, x shift, y shift)
    niter = int(sys.argv[5])
    alg = sys.argv[6].upper()
    itype = sys.argv[7].upper()

    simgs0 = [os.path.abspath(sdir0+"/"+i) for i in os.listdir(sdir0) if (i.find(".png") != -1)]
    simgs0.sort()
    simgs1 = [os.path.abspath(sdir1+"/"+i) for i in os.listdir(sdir1) if (i.find(".png") != -1)]
    simgs1.sort()

    os.system("rm -rf %s; mkdir %s" % (outdir,outdir))
    os.system("mkdir %s/frames0" % outdir)
    os.system("mkdir %s/frames1" % outdir)
    os.system("mkdir %s/merged" % outdir)

    x,y = np.array(Image.open(simgs0[0]).convert("L")).shape
    b = Bounds([-180,-x//2,-y//2], [180,x//2,y//2], enforce="resample")

    results = []

    s  = "\nRegistration results:\n"
    print(s, flush=True, end="")

    for k in range(len(simgs0)):
        if (itype == "QI"):
            i = QuasirandomInitializer(npart, ndim, bounds=b)
        elif (itype == "SI"):
            i = SphereInitializer(npart, ndim, bounds=b)
        else:
            i = RandomInitializer(npart, ndim, bounds=b)

        obj = Objective(simgs0[k], simgs1[k])

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
        else:
            raise ValueError("Unknown algorithm: %s" % alg)

        st = time.time()
        swarm.Optimize()
        en = time.time()

        res = swarm.Results()
        results.append(res)
        aligned = ApplyRegistration(simgs0[k], simgs1[k], res["gpos"][-1])
        Image.fromarray(aligned).save(outdir+"/frames1/"+os.path.basename(simgs1[k]))
        im = Image.open(simgs0[k]).convert("L")
        im.save(outdir+"/frames0/"+os.path.basename(simgs0[k]))
        img = np.zeros((aligned.shape[0],aligned.shape[1],3), dtype="uint8")
        img[:,:,0] = aligned
        img[:,:,1] = np.array(im)
        Image.fromarray(img).save(outdir+"/merged/"+os.path.basename(simgs0[k]))
        
        angle, xshift, yshift = res["gpos"][-1]
        t = "  %3d: (NMI=%0.6f)  theta=%10.5f, x=%10.5f, y=%10.5f\n" % (k, -res["gbest"][-1], angle, xshift, yshift)
        print(t, flush=True, end="")
        s += t

    s += "\n"
    print()

    #  Overall registration results
    pickle.dump(results, open(outdir+"/results.pkl","wb"))

    with open(outdir+"/README.txt","w") as f:
        f.write(s)


if (__name__ == "__main__"):
    main()

