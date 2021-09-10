#
#  file:  cell.py
#
#  Optimize "cell tower" placement.
#
#  RTK, 02-Oct-2020
#  Last update:  06-Oct-2020
#
################################################################

import pickle
import time
import os
import sys
import numpy as np
from PIL import Image

sys.path.append("../")

from DE import *
from RO import *
from PSO import *
from GWO import *
from Jaya import *
from GA import *

from Bounds import *
from RandomInitializer import *
from QuasirandomInitializer import *
from SphereInitializer import *
from LinearInertia import *


################################################################
#  CoverageMap
#
def CoverageMap(image, xy, radii):
    """Create a coverage map"""

    im = image.copy()
    R,C = im.shape

    #  Apply the towers to the map
    for k in range(len(radii)):
        x,y = xy[k]
        for i in range(x-radii[k],x+radii[k]):
            for j in range(y-radii[k],y+radii[k]):
                if ((i-x)**2 + (j-y)**2) <= (radii[k]*radii[k]):
                    if i < 0 or j < 0:
                        continue
                    if i >= R or j >= C:
                        continue
                    im[i,j] += 0.5*(k+1)/len(radii)
    
    imax = im.max()
    for k in range(len(radii)):
        x,y = xy[k]
        im[x,y] = 1.4*imax

    return im


################################################################
#  Objective
#
class Objective:
    """Determine coverage area"""

    def __init__(self, image, towers, radius):
        """Constructor"""

        self.image = image.copy()
        self.R, self.C = image.shape
        self.radii = (towers*radius).astype("int32")
        self.fcount = 0

    def Collisions(self, xy):
        """Any towers on roads?"""

        n = 0
        for i in range(xy.shape[0]):
            x,y = xy[i]
            if (self.image[x,y] != 0):
                n += 1
        return n

    def Evaluate(self, p):
        """Evaluate a set of positions"""

        self.fcount += 1
        n = p.shape[0]//2
        xy = p.astype("uint32").reshape((n,2))
        if (self.Collisions(xy) != 0):
            return 1.0
        empty = np.zeros((self.R, self.C))
        cover = CoverageMap(empty, xy, self.radii)
        zeros = len(np.where(cover == 0)[0])
        uncovered = zeros / (self.R*self.C) 
        return uncovered


################################################################
#  CellBounds
#
class CellBounds(Bounds):
    """Enforce discrete tower positions"""

    def __init__(self, lower, upper, enforce):
        """Constructor"""

        super().__init__(lower, upper, enforce)

    def Validate(self, p):
        """Make discrete"""

        return np.floor(p)


################################################################
#  main
#
def main():
    """Cover a map with cell towers"""

    if (len(sys.argv) == 1):
        print()
        print("cell <map> <towers> <npart> <niter> <alg> RI|QI|SI <outdir> [frames]")
        print()
        print("  <map>     -  map image (.png)")
        print("  <towers>  -  text file w/towers and ranges")
        print("  <npart>   -  number of swarm particles")
        print("  <niter>   -  number of swarm iterations")
        print("  <alg>     -  DE|RO|PSO|GWO|JAYA|GA")
        print("  RI|QI|SI  -  initializer type")
        print("  <outdir>  -  output directory (overwritten)")
        print("  frames    -  'frames' ==> output frame per iteration")
        print()
        return

    map_image = 0.9*np.array(Image.open(sys.argv[1]).convert("L"))/255
    towers = np.array([float(i[:-1]) for i in open(sys.argv[2])])
    npart = int(sys.argv[3])
    niter = int(sys.argv[4])
    alg = sys.argv[5].upper()
    itype = sys.argv[6].upper()
    outdir = sys.argv[7]

    frames = False
    if (len(sys.argv) > 8):
        frames = True

    os.system("rm -rf %s; mkdir %s" % (outdir,outdir))
    if (frames):
        os.system("mkdir %s/frames" % outdir)

    #  Dimensions and bounds
    x,y = map_image.shape
    lower = [0,0]*len(towers)
    upper = [x,y]*len(towers)
    b = CellBounds(lower, upper, enforce="resample")
    ndim = 2*len(towers)
    
    #  Max radius
    w = x if (x>y) else y
    radius = w//2

    if (itype == "QI"):
        i = QuasirandomInitializer(npart, ndim, bounds=b)
    elif (itype == "SI"):
        i = SphereInitializer(npart, ndim, bounds=b)
    else:
        i = RandomInitializer(npart, ndim, bounds=b)

    obj = Objective(map_image, towers, radius)

    if (alg == "PSO"):
        swarm = PSO(obj=obj, npart=npart, ndim=ndim, init=i, bounds=b, max_iter=niter, tol=1e-9, inertia=LinearInertia())
    elif (alg == "DE"):
        swarm = DE(obj=obj, npart=npart, ndim=ndim, init=i, bounds=b, max_iter=niter, tol=1e-9)
    elif (alg == "RO"):
        swarm = RO(obj=obj, npart=npart, ndim=ndim, init=i, bounds=b, max_iter=niter, tol=1e-9)
    elif (alg == "GWO"):
        swarm = GWO(obj=obj, npart=npart, ndim=ndim, init=i, bounds=b, max_iter=niter, tol=1e-9)
    elif (alg == "JAYA"):
        swarm = Jaya(obj=obj, npart=npart, ndim=ndim, init=i, bounds=b, max_iter=niter, tol=1e-9)
    elif (alg == "GA"):
        swarm = GA(obj=obj, npart=npart, ndim=ndim, init=i, bounds=b, max_iter=niter, tol=1e-9)

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
        if (frames):
            p = res["gpos"][-1]
            n = p.shape[0]//2
            xy = p.astype("uint32").reshape((n,2))
            radii = (towers*radius).astype("int32")
            cover = CoverageMap(map_image, xy, radii)
            img = Image.fromarray((255*cover/cover.max()).astype("uint8"))
            img.save(outdir+"/frames/"+("frame_%05d.png" % k))
    en = time.time()

    res = swarm.Results()
    pickle.dump(res, open(outdir+"/results.pkl","wb"))

    s += "\nSearch results: %s, %d particles, %d iterations, %s\n\n" % (alg, npart, niter, itype)
    s += "Optimization minimum %0.8f (time = %0.3f)\n" % (res["gbest"][-1], en-st)
    s += "(%d best updates, %d function evaluations)\n\n" % (len(res["gbest"]), obj.fcount)

    print(s)
    with open(outdir+"/README.txt","w") as f:
        f.write(s)

    #  Generate the output map image
    p = res["gpos"][-1]
    n = p.shape[0]//2
    xy = p.astype("uint32").reshape((n,2))
    radii = (towers*radius).astype("int32")
    cover = CoverageMap(map_image, xy, radii)
    c2 = (cover/cover.max())**(0.5)
    c2 = c2/c2.max()
    img = Image.fromarray((255*c2).astype("uint8"))
    img.save(outdir+"/coverage.png")
    img = Image.fromarray((255*map_image).astype("uint8"))
    img.save(outdir+"/map.png")


if (__name__ == "__main__"):
    main()

