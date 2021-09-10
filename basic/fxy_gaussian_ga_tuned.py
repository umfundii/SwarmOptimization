#
#  file:  fxy_gaussian_ga_tuned.py
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

from Bounds import *
from RandomInitializer import *

class Objective:
    def Evaluate(self, p):
        return -5.0*np.exp(-0.5*((p[0]+2.2)**2/0.4+(p[1]-4.3)**2/0.4)) +  \
               -2.0*np.exp(-0.5*((p[0]-2.2)**2/0.4+(p[1]+4.3)**2/0.4))


def Dispersion(swarm, i, d): 
    x,y = swarm.pos[:,0], swarm.pos[:,1]
    dx = x.max() - x.min()
    dy = y.max() - y.min()
    d[i] = (dx + dy) / 2.0 

def wdist(x,y):
    return np.sqrt((2.2-x)**2 + (-4.3-y)**2)

def rdist(x,y):
    return np.sqrt((-2.2-x)**2 + (4.3-y)**2)


def main():
    npart = 100
    miter = 100
    runs  = 100

    b = Bounds([-6,-6],[6,6],enforce="resample")
    obj = Objective()
    ri = RandomInitializer(npart=npart, ndim=2, bounds=b)

    v = np.zeros((runs,miter))
    for i in range(runs):
        b = Bounds([-6,-6],[6,6],enforce="resample")
        ri = RandomInitializer(npart=npart, ndim=2, bounds=b)
        swarm = GA(obj=obj, npart=npart, ndim=2, max_iter=miter, init=ri, bounds=b, CR=0.3, F=0.4, top=0.2)
        swarm.Initialize()
        for j in range(miter):
            swarm.Step()
            res = swarm.Results()
            v[i,j] = res["gbest"][-1]
    plt.plot(np.arange(miter)[::5],v.mean(axis=0)[::5], marker='o', linestyle='none', color='k')
    plt.plot(v.mean(axis=0), color='k')
    plt.xlabel('Generation')
    plt.ylabel('Swarm Best')
    plt.tight_layout(pad=0, w_pad=0, h_pad=0)
    plt.savefig("fxy_gaussian_ga_tuned_plot.png", dpi=300)
    plt.close()
    print("Final minimum value %0.8f" % (v.mean(axis=0)[-1],))
    print()


if (__name__ == "__main__"):
    main()

