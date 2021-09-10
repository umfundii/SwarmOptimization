#
#  file:  de_gaussian_5d_plot.py
#
#  5D Gaussian function example for DE.
#
#  RTK, 15-Jul-2020
#  Last update:  15-Jul-2020
#
################################################################

import time
import os
import sys
sys.path.append("../")

import numpy as np
import matplotlib.pylab as plt
from DE import *
from RO import *
from Jaya import *
from GWO import *
from GA import *
from PSO import *

from Bounds import *
from RandomInitializer import *
from LinearInertia import *

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
    m = np.zeros((mt,runs))
    j = 0
    while (j < runs):
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

        swarm.Initialize()
        for i in range(mt):
            swarm.Step()
            res = swarm.Results()
            m[i,j] = res["gbest"][-1]
        
        x,y,z,a,b = swarm.Results()["gpos"][-1]
        if (rdist(x,y,z,a,b) < 1):
            j += 1

    return m
            

def main():
    npart= 20
    miter= 450
    runs = 20

    ro = Run("RO", npart, miter, runs)
    pso = Run("PSO", npart, miter, runs)
    jaya = Run("Jaya", npart, miter, runs)
    gwo = Run("GWO", npart, miter, runs)
    ga = Run("GA", npart, miter, runs)
    de = Run("DE", npart, miter, runs)
    
    x = np.arange(miter)
    plt.plot(x, ro.mean(axis=1), color='r')
    plt.plot(x, pso.mean(axis=1), color='g')
    plt.plot(x, jaya.mean(axis=1), color='b')
    plt.plot(x, gwo.mean(axis=1), color='m')
    plt.plot(x, ga.mean(axis=1), color='c')
    plt.plot(x, de.mean(axis=1), color='k')
    plt.errorbar(x[::20], ro.mean(axis=1)[::20], (ro.std(axis=1)/np.sqrt(runs))[::20], marker='o', linestyle='none',color='r', label='RO')
    plt.errorbar(x[1::20], pso.mean(axis=1)[1::20], (pso.std(axis=1)/np.sqrt(runs))[1::20], marker='s', linestyle='none', color='g', label='PSO')
    plt.errorbar(x[2::20], jaya.mean(axis=1)[2::20], (jaya.std(axis=1)/np.sqrt(runs))[2::20], marker='*', linestyle='none', color='b', label='Jaya')
    plt.errorbar(x[3::20], gwo.mean(axis=1)[3::20], (gwo.std(axis=1)/np.sqrt(runs))[3::20], marker='<', linestyle='none', color='m', label='GWO')
    plt.errorbar(x[4::20], ga.mean(axis=1)[4::20], (ga.std(axis=1)/np.sqrt(runs))[4::20], marker='>', linestyle='none', color='c', label='GA')
    plt.errorbar(x[5::20], de.mean(axis=1)[5::20], (de.std(axis=1)/np.sqrt(runs))[5::20], marker='P', linestyle='none', color='k', label='DE')
    
    plt.legend(loc="upper right")
    plt.tight_layout(pad=0, w_pad=0, h_pad=0)
    plt.savefig("de_gaussian_5d_plot.png", dpi=300)
    plt.show()


if (__name__ == "__main__"):
    main()

