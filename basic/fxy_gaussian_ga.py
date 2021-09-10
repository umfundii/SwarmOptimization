#
#  file:  fxy_gaussian_ga.py
#
#  Gaussian function example for GA and top.
#
#  RTK, 19-Jun-2020
#  Last update:  19-Jun-2020
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


def main():
    npart = 100
    miter = 100
    runs  = 20

    np.random.seed(73939133)
    b = Bounds([-6,-6],[6,6],enforce="resample")
    obj = Objective()
    ri = RandomInitializer(npart=npart, ndim=2, bounds=b)

    ls = ['solid',(0,(3,1,1,1,1,1)),(0,(1,1)),(0,(3,1,1,1)),(0,(5,1))]
    mk = ['o','s','*','^','<']
    cs = ['r','g','b','m','k']

    for k,top in enumerate([0.01, 0.1, 0.5, 0.9, 0.99]):
        swarm = GA(obj=obj, npart=npart, ndim=2, max_iter=miter, init=ri, bounds=b, top=top)
        swarm.Initialize()
        v = np.zeros((runs,miter))
        D = np.zeros((runs,miter))
        for i in range(runs):
            d = np.zeros(miter)
            for j in range(miter):
                swarm.Step()
                Dispersion(swarm, j, d)
                res = swarm.Results()
                v[i,j] = res["gbest"][-1]
            D[i,:] = d
        plt.plot(np.arange(miter)[::5],D.mean(axis=0)[::5], marker=mk[k],
                 linestyle='none', color=cs[k], label='$\eta=%0.2f$' % top)
        plt.plot(D.mean(axis=0), color=cs[k])
    
    plt.legend(loc='upper right')
    plt.xlabel('Generation')
    plt.ylabel('Dispersion')
    plt.tight_layout(pad=0, w_pad=0, h_pad=0)
    plt.savefig("fxy_gaussian_ga_eta_dispersion_plot.png", dpi=300)
    plt.close()

    np.random.seed(73939133)
    b = Bounds([-6,-6],[6,6],enforce="resample")
    obj = Objective()
    ri = RandomInitializer(npart=npart, ndim=2, bounds=b)

    for k,top in enumerate([0.01, 0.1, 0.5, 0.9, 0.99]):
        swarm = GA(obj=obj, npart=npart, ndim=2, max_iter=miter, init=ri, bounds=b, top=top)
        swarm.Initialize()
        v = np.zeros((runs,miter))
        D = np.zeros((runs,miter))
        for i in range(runs):
            d = np.zeros(miter)
            for j in range(miter):
                swarm.Step()
                Dispersion(swarm, j, d)
                res = swarm.Results()
                v[i,j] = res["gbest"][-1]
            D[i,:] = d
        plt.plot(np.arange(miter)[::5],v.mean(axis=0)[::5], marker=mk[k], 
                 linestyle='none', color=cs[k], label='$\eta=%0.2f$' % top)
        plt.plot(v.mean(axis=0), color=cs[k])
    
    plt.legend(loc='upper right')
    plt.xlabel('Generation')
    plt.ylabel('Swarm Best')
    plt.tight_layout(pad=0, w_pad=0, h_pad=0)
    plt.savefig("fxy_gaussian_ga_eta_best_plot.png", dpi=300)
    plt.close()


if (__name__ == "__main__"):
    main()

