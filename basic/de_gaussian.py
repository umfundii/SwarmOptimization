#
#  file:  de_gaussian.py
#
#  Gaussian function example for testing swarm algorithms.
#
#  RTK, 09-Mar-2020
#  Last update:  13-Jul-2020
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
from DE import *

from Bounds import *
from RandomInitializer import *
from QuasirandomInitializer import *
from SphereInitializer import *

class Objective:
    def Evaluate(self, p):
        return -5.0*np.exp(-0.5*((p[0]+2.2)**2/0.4+(p[1]-4.3)**2/0.4)) +  \
               -2.0*np.exp(-0.5*((p[0]-2.2)**2/0.4+(p[1]+4.3)**2/0.4))

def main():
    if (len(sys.argv) == 1):
        print()
        print("de_gaussian.py <npart> <max> <RI|QI|SI> <mode> <cmode> [frames]")
        print()
        print("  <npart>  - number of particles")
        print("  <max>    - max iterations")
        print("  RI|QI|SI - type of initializer")
        print("  <mode>   - mode: 'rand', 'best', or 'toggle'")
        print("  <cmode>  - cmode: 'bin' or 'GA'")
        print("  frames   - frames directory (overwritten)")
        print()
        return

    npart = int(sys.argv[1])
    miter = int(sys.argv[2])
    itype = sys.argv[3].upper()
    mode = sys.argv[4].lower()
    cmode= sys.argv[5].lower()
    fdir = sys.argv[6] if (len(sys.argv)==7) else ""

    #np.random.seed(8675309)
    b = Bounds([-6,-6],[6,6],enforce="resample")
    obj = Objective()

    if (itype == "QI"):
        i = QuasirandomInitializer(npart=npart, ndim=2, bounds=b)
    elif (itype == "SI"):
        i = SphereInitializer(npart=npart, ndim=2, bounds=b)
    else:
        i = RandomInitializer(npart=npart, ndim=2, bounds=b)

    swarm = DE(obj=obj, npart=npart, ndim=2, max_iter=miter, init=i, bounds=b,
               mode=mode, cmode=cmode)

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

