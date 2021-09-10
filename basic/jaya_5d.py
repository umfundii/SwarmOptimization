#
#  file:  jaya_5d.py
#
#  5D Gaussian function example for Jaya.
#
#  RTK, 17-Jul-2020
#  Last update:  17-Jul-2020
#
################################################################

import time
import os
import sys
sys.path.append("../")

import numpy as np
import matplotlib.pylab as plt
from Jaya import *

from Bounds import *
from RandomInitializer import *

class Objective:
    def Evaluate(self, p):
        return -5.0*np.exp(-0.5*((p[0]+2.2)**2/0.4+(p[1]-4.3)**2/0.4+(p[2]+3.1)**2/0.4+(p[3]-1.2)**2/0.4+(p[4]+0.7)**2/0.4)) +  \
               -2.0*np.exp(-0.5*((p[0]-2.2)**2/0.4+(p[1]+4.3)**2/0.4+(p[2]-3.1)**2/0.4+(p[3]+1.2)**2/0.4+(p[4]-0.7)**2/0.4))

def wdist(x,y,z,a,b):
    return np.sqrt((2.2-x)**2+(-4.3-y)**2+(3.1-z)**2+(-1.2-a)**2+(0.7-b)**2)

def rdist(x,y,z,a,b):
    return np.sqrt((-2.2-x)**2+(4.3-y)**2+(-3.1-z)**2+(1.2-a)**2+(-0.7-b)**2)


def Run(alg, npart, mt, runs):
    bd = Bounds([-6,-6,-6,-6,-6],[6,6,6,6,6],enforce="resample")
    obj = Objective()
    m = []
    s = w = f = 0
    for i in range(runs):
        ri = RandomInitializer(npart=npart, ndim=5, bounds=bd)
        if (alg == "RO"):
            swarm = RO(obj=obj, npart=npart, ndim=5, max_iter=mt, init=ri, bounds=bd)
        elif (alg == "PSO"):
            swarm = PSO(obj=obj, npart=npart, ndim=5, max_iter=mt, init=ri, bounds=bd, inertia=LinearInertia())
        elif (alg == "Jaya"):
            swarm = Jaya(obj=obj, npart=npart, ndim=5, max_iter=mt, init=ri, bounds=bd)
        elif (alg == "GWO"):
            swarm = GWO(obj=obj, npart=npart, ndim=5, max_iter=mt, init=ri, bounds=bd)
        elif (alg == "GA"):
            swarm = GA(obj=obj, npart=npart, ndim=5, max_iter=mt, init=ri, bounds=bd)
        elif (alg == "DE"):
            swarm = DE(obj=obj, npart=npart, ndim=5, max_iter=mt, init=ri, bounds=bd)
        swarm.Optimize()
        res = swarm.Results()
        x,y,z,a,b = res["gpos"][-1]
        if (wdist(x,y,z,a,b) < 1):
            w += 1
        elif (rdist(x,y,z,a,b) < 1):
            m.append(res["gbest"][-1])
            s += 1
        else:
            f += 1
    m = np.array(m)
    print("%s (%4d, %4d) minimum= %0.7f +/- %0.7f (success=%3d, wrong=%3d, fail=%3d)" % (alg, npart, mt, m.mean(), m.std()/np.sqrt(m.shape[0]), s,w,f))


def main():
    nparts= [200]
    miter = [700, 1000, 1500, 2000, 2500, 5000, 10000, 20000, 40000, 80000, 160000]
    runs  = 12

    print()
    for npart in nparts:
        for mt in miter:
            Run("Jaya", npart, mt, runs)
    print()


if (__name__ == "__main__"):
    main()

