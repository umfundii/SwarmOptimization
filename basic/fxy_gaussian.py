#
#  file:  fxy_gaussian.py
#
#  Gaussian function example for testing swarm algorithms.
#
#  RTK, 09-Mar-2020
#  Last update:  26-May-2020
#
################################################################

import time
import os
import sys
sys.path.append("../")

import matplotlib.pylab as plt
def PlotSwarm(swarm, i, fdir):
    fname = fdir + ("/frame_%04d.png" % i)
    x = swarm.pos[:,0]
    y = swarm.pos[:,1]
    gx,gy = swarm.gpos[-1]
    sx,sy = [-2.2, 4.3]
    plt.plot(sx,sy,marker='s',fillstyle='none', markersize=12,color='k',linestyle='none')
    plt.plot(x,y,marker='o',color='b',linestyle='none')
    plt.plot(gx,gy,marker='*',markersize=12,color='r',linestyle='none')
    plt.xlim(-6,6)
    plt.ylim(-6,6)
    plt.gca().set_aspect('equal', adjustable='box')
    plt.tight_layout(pad=0.1, w_pad=0, h_pad=0)
    plt.savefig(fname, dpi=300)
    plt.close()

def Dispersion(swarm, i, d):
    x,y = swarm.pos[:,0], swarm.pos[:,1]
    dx = x.max() - x.min()
    dy = y.max() - y.min()
    d[i] = (dx + dy) / 2.0

import numpy as np
from RO import *
from PSO import *
from Jaya import *
from GWO import *
from DE import *
from GA import *

from Bounds import *
from RandomInitializer import *
from QuasirandomInitializer import *
from SphereInitializer import *
from LinearInertia import *
from RandomInertia import *

class Objective:
    def Evaluate(self, p):
        return -5.0*np.exp(-0.5*((p[0]+2.2)**2/0.4+(p[1]-4.3)**2/0.4)) +  \
               -2.0*np.exp(-0.5*((p[0]-2.2)**2/0.4+(p[1]+4.3)**2/0.4))

def main():
    if (len(sys.argv) == 1):
        print()
        print("fxy_gaussian.py <npart> <max> <alg> <RI|QI|SI> [frames]")
        print()
        print("  <npart>  - number of particles")
        print("  <max>    - max iterations")
        print("  <alg>    - RO,PSO,JAYA,GWO,DE,GA")
        print("  RI|QI|SI - type of initializer")
        print("  frames   - frames directory (overwritten)")
        print()
        return

    npart = int(sys.argv[1])
    miter = int(sys.argv[2])
    alg = sys.argv[3].upper()
    itype = sys.argv[4].upper()
    fdir = sys.argv[5] if (len(sys.argv)==6) else ""

    #np.random.seed(8675309)
    b = Bounds([-6,-6],[6,6],enforce="resample")
    obj = Objective()

    if (itype == "QI"):
        i = QuasirandomInitializer(npart=npart, ndim=2, bounds=b)
    elif (itype == "SI"):
        i = SphereInitializer(npart=npart, ndim=2, bounds=b)
    else:
        i = RandomInitializer(npart=npart, ndim=2, bounds=b)

    if (alg == "RO"):
        swarm = RO(obj=obj, npart=npart, ndim=2, max_iter=miter, init=i, bounds=b)
    elif (alg == "PSO"):
        swarm = PSO(obj=obj, npart=npart, ndim=2, max_iter=miter, init=i, bounds=b,
                    inertia=LinearInertia(), bare=False, bare_prob=0.5, ring=False, neighbors=4)
    elif (alg == "JAYA"):
        swarm = Jaya(obj=obj, npart=npart, ndim=2, max_iter=miter, init=i, bounds=b)
    elif (alg == "GWO2") or (alg == "GWO"):
        swarm = GWO(obj=obj, npart=npart, ndim=2, max_iter=miter, init=i, bounds=b, eta=2)
    elif (alg == "GWO4"):
        swarm = GWO(obj=obj, npart=npart, ndim=2, max_iter=miter, init=i, bounds=b, eta=4)
    elif (alg == "DE"):
        swarm = DE(obj=obj, npart=npart, ndim=2, max_iter=miter, init=i, bounds=b)
    elif (alg == "GA"):
        swarm = GA(obj=obj, npart=npart, ndim=2, max_iter=miter, init=i, bounds=b)
    else:
        raise ValueError("Unknown swarm algorithm: %s" % alg)

    if (fdir == ""):
        st = time.time()
        swarm.Optimize()
        en = time.time()
    else:
        os.system("rm -rf %s; mkdir %s" % (fdir,fdir))
        d = np.zeros(miter+1)
        st = time.time()
        swarm.Initialize()
        PlotSwarm(swarm,0,fdir)
        Dispersion(swarm,0,d)
        for i in range(miter):
            swarm.Step()
            PlotSwarm(swarm,i+1,fdir)
            Dispersion(swarm,i+1,d)
        en = time.time()
        np.save(fdir+"/dispersion.npy", d)
    res = swarm.Results()
    x,y = res["gpos"][-1]
    v = res["gbest"][-1]
    print()
    print("f(%0.8f, %0.8f) = %0.10f" % (x,y,v))
    print("(%d swarm best updates, time = %0.3f seconds)" % (len(res["gbest"]), en-st))
    print()


if (__name__ == "__main__"):
    main()

