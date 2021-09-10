#
#  file:  fxy_gaussian_ga_multi.py
#
#  5D Gaussian function example for GA.
#
#  RTK, 19-Jun-2020
#  Last update:  22-Jun-2020
#
################################################################

import time
import os
import sys
sys.path.append("../")

import numpy as np
import matplotlib.pylab as plt
from GA import *
from PSO import *
from LinearInertia import *

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


def main():
    nparts= [20, 100, 500, 1000, 2000]
    miter = [100, 500, 1000, 1500, 2000]
    runs  = 50

    bd = Bounds([-6,-6,-6,-6,-6],[6,6,6,6,6],enforce="resample")
    obj = Objective()

    print()
    for npart in nparts:
        for mt in miter:
            m = []
            s = w = f = 0
            for i in range(runs):
                ri = RandomInitializer(npart=npart, ndim=5, bounds=bd)
                #swarm = GA(obj=obj, npart=npart, ndim=5, max_iter=mt, init=ri, bounds=bd, CR=0.3, F=0.4, top=0.2)
                swarm = PSO(obj=obj, npart=npart, ndim=5, max_iter=mt, init=ri, bounds=bd, inertia=LinearInertia())
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
            print("(%4d, %4d) minimum= %0.7f +/- %0.7f (success=%3d, wrong=%3d, fail=%3d)" % (npart, mt, m.mean(), m.std()/np.sqrt(m.shape[0]), s,w,f))
    print()


if (__name__ == "__main__"):
    main()

