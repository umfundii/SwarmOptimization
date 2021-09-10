#
#  file:  fxy_gaussian_algs.py
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

from RO import *
from PSO import *
from Jaya import *
from GWO import *
from GA import *

from Bounds import *
from RandomInitializer import *
from LinearInertia import *

class Objective:
    def Evaluate(self, p):
        return -5.0*np.exp(-0.5*((p[0]+2.2)**2/0.4+(p[1]-4.3)**2/0.4)) +  \
               -2.0*np.exp(-0.5*((p[0]-2.2)**2/0.4+(p[1]+4.3)**2/0.4))

def main():
    npart = 100
    miter = 100
    runs  = 100

    obj = Objective()

    #  RO
    np.random.seed(73939133)
    b = Bounds([-6,-6],[6,6],enforce="resample")
    ri = RandomInitializer(npart=npart, ndim=2, bounds=b)
    ro = np.zeros((runs,miter))
    for i in range(runs):
        swarm = RO(obj=obj, npart=npart, ndim=2, max_iter=miter, init=ri, bounds=b)
        swarm.Initialize()
        for j in range(miter):
            swarm.Step()
            res = swarm.Results()
            ro[i,j] = res["gbest"][-1]

    #  PSO
    np.random.seed(73939133)
    b = Bounds([-6,-6],[6,6],enforce="resample")
    ri = RandomInitializer(npart=npart, ndim=2, bounds=b)
    pso = np.zeros((runs,miter))
    for i in range(runs):
        swarm = PSO(obj=obj, npart=npart, ndim=2, max_iter=miter, init=ri, bounds=b, inertia=LinearInertia())
        swarm.Initialize()
        for j in range(miter):
            swarm.Step()
            res = swarm.Results()
            pso[i,j] = res["gbest"][-1]

    #  Jaya
    np.random.seed(73939133)
    b = Bounds([-6,-6],[6,6],enforce="resample")
    ri = RandomInitializer(npart=npart, ndim=2, bounds=b)
    jaya = np.zeros((runs,miter))
    for i in range(runs):
        swarm = Jaya(obj=obj, npart=npart, ndim=2, max_iter=miter, init=ri, bounds=b)
        swarm.Initialize()
        for j in range(miter):
            swarm.Step()
            res = swarm.Results()
            jaya[i,j] = res["gbest"][-1]

    #  GWO
    np.random.seed(73939133)
    b = Bounds([-6,-6],[6,6],enforce="resample")
    ri = RandomInitializer(npart=npart, ndim=2, bounds=b)
    gwo = np.zeros((runs,miter))
    for i in range(runs):
        swarm = GWO(obj=obj, npart=npart, ndim=2, max_iter=miter, init=ri, bounds=b, eta=4)
        swarm.Initialize()
        for j in range(miter):
            swarm.Step()
            res = swarm.Results()
            gwo[i,j] = res["gbest"][-1]

    #  GA
    np.random.seed(73939133)
    b = Bounds([-6,-6],[6,6],enforce="resample")
    ri = RandomInitializer(npart=npart, ndim=2, bounds=b)
    ga = np.zeros((runs,miter))
    for i in range(runs):
        swarm = GA(obj=obj, npart=npart, ndim=2, max_iter=miter, init=ri, bounds=b, CR=0.3, F=0.4, top=0.2)
        swarm.Initialize()
        for j in range(miter):
            swarm.Step()
            res = swarm.Results()
            ga[i,j] = res["gbest"][-1]

    #plt.plot(np.arange(miter)[::5],ro.mean(axis=0)[::5], marker='o', linestyle='none', color='k', label="RO")
    #plt.plot(ro.mean(axis=0), color='k')
    #plt.plot(np.arange(miter)[::5],pso.mean(axis=0)[::5], marker='s', linestyle='none', color='k', label="PSO")
    #plt.plot(pso.mean(axis=0), color='k')
    #plt.plot(np.arange(miter)[::5],jaya.mean(axis=0)[::5], marker='*', linestyle='none', color='k', label="Jaya")
    #plt.plot(jaya.mean(axis=0), color='k')
    #plt.plot(np.arange(miter)[::5],gwo.mean(axis=0)[::5], marker='^', linestyle='none', color='k', label="GWO")
    #plt.plot(gwo.mean(axis=0), color='k')
    #plt.plot(np.arange(miter)[::5],ga.mean(axis=0)[::5], marker='<', linestyle='none', color='k', label="GA")
    #plt.plot(ga.mean(axis=0), color='k')
    plt.errorbar(np.arange(miter)[::5],ro.mean(axis=0)[::5], (ro.std(axis=0)/np.sqrt(runs))[::5],marker='o', linestyle='none', color='k', label="RO")
    plt.plot(ro.mean(axis=0), color='k')
    plt.errorbar(np.arange(miter)[::5],pso.mean(axis=0)[::5], (pso.std(axis=0)/np.sqrt(runs))[::5],marker='s', linestyle='none', color='k', label="PSO")
    plt.plot(pso.mean(axis=0), color='k')
    plt.errorbar(np.arange(miter)[::5],jaya.mean(axis=0)[::5], (jaya.std(axis=0)/np.sqrt(runs))[::5],marker='*', linestyle='none', color='k', label="Jaya")
    plt.plot(jaya.mean(axis=0), color='k')
    plt.errorbar(np.arange(miter)[::5],gwo.mean(axis=0)[::5], (gwo.std(axis=0)/np.sqrt(runs))[::5],marker='^', linestyle='none', color='k', label="GWO")
    plt.plot(gwo.mean(axis=0), color='k')
    plt.errorbar(np.arange(miter)[::5],ga.mean(axis=0)[::5], (ga.std(axis=0)/np.sqrt(runs))[::5], marker='<', linestyle='none', color='k', label="GA")
    plt.plot(ga.mean(axis=0), color='k')

    plt.legend(loc="upper right")
    plt.xlabel('Generation')
    plt.ylabel('Swarm Best')
    plt.tight_layout(pad=0, w_pad=0, h_pad=0)
    plt.savefig("fxy_gaussian_algs_plot.png", dpi=300)
    plt.close()


if (__name__ == "__main__"):
    main()

