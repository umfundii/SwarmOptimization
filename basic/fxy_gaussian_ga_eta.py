#
#  file:  fxy_gaussian_ga_eta.py
#
#  Gaussian function example for GA and eta.
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

    etas = [0.01, 0.1,0.2,0.3,0.4,0.5,0.6,0.7,0.8,0.9, 0.99]

    d = np.zeros(len(etas))
    e = np.zeros(len(etas))

    for k,eta in enumerate(etas):
        m = []
        s = w = f = 0
        for i in range(runs):
            swarm = GA(obj=obj, npart=npart, ndim=2, max_iter=miter, init=ri, bounds=b, top=eta)
            swarm.Optimize()
            res = swarm.Results()
            x,y = res["gpos"][-1]
            if (wdist(x,y) < 1):
                w += 1
            elif (rdist(x,y) < 1):
                m.append(res["gbest"][-1])
                s += 1
            else:
                f += 1
        m = np.array(m)
        print("eta=%0.2f, minimum= %0.7f +/- %0.7f (success=%3d, wrong=%3d, fail=%3d)" % (eta, m.mean(), m.std()/np.sqrt(m.shape[0]), s,w,f))
        d[k] = m.mean()
        e[k] = m.std()/np.sqrt(m.shape[0])

    plt.errorbar(etas,d,e, marker='o', color='k')
    plt.xlabel("$\eta$")
    plt.ylabel("Average Minimum")
    plt.tight_layout(pad=0, w_pad=0, h_pad=0)
    plt.savefig("fxy_gaussian_ga_eta_plot.png", dpi=300)
    plt.close()
    print()

    mk = ['o','s','*','^','<']
    cs = ['r','g','b','m','k']

    etas = [0.01, 0.2, 0.5, 0.8, 0.99]

    np.random.seed(73939133)
    obj = Objective()

    for k,eta in enumerate(etas):
        D = np.zeros((runs,miter))
        for i in range(runs):
            b = Bounds([-6,-6],[6,6],enforce="resample")
            ri = RandomInitializer(npart=npart, ndim=2, bounds=b)
            swarm = GA(obj=obj, npart=npart, ndim=2, max_iter=miter, init=ri, bounds=b, top=eta)
            swarm.Initialize()
            d = np.zeros(miter)
            for j in range(miter):
                swarm.Step()
                Dispersion(swarm, j, d)
                res = swarm.Results()
            D[i,:] = d
        plt.plot(np.arange(miter)[::5],D.mean(axis=0)[::5], marker=mk[k],
                 linestyle='none', color=cs[k], label='$\eta=%0.2f$' % eta)
        plt.plot(D.mean(axis=0), color=cs[k])
    
    plt.legend(loc='upper right')
    plt.xlabel('Generation')
    plt.ylabel('Dispersion')
    plt.tight_layout(pad=0, w_pad=0, h_pad=0)
    plt.savefig("fxy_gaussian_ga_eta_dispersion_plot.png", dpi=300)
    plt.close()

    np.random.seed(73939133)
    obj = Objective()

    for k,eta in enumerate(etas):
        v = np.zeros((runs,miter))
        for i in range(runs):
            b = Bounds([-6,-6],[6,6],enforce="resample")
            ri = RandomInitializer(npart=npart, ndim=2, bounds=b)
            swarm = GA(obj=obj, npart=npart, ndim=2, max_iter=miter, init=ri, bounds=b, top=eta)
            swarm.Initialize()
            for j in range(miter):
                swarm.Step()
                res = swarm.Results()
                v[i,j] = res["gbest"][-1]
        plt.plot(np.arange(miter)[::5],v.mean(axis=0)[::5], marker=mk[k], 
                 linestyle='none', color=cs[k], label='$\eta=%0.2f$' % eta)
        plt.plot(v.mean(axis=0), color=cs[k])
    
    plt.legend(loc='upper right')
    plt.xlabel('Generation')
    plt.ylabel('Swarm Best')
    plt.tight_layout(pad=0, w_pad=0, h_pad=0)
    plt.savefig("fxy_gaussian_ga_eta_best_plot.png", dpi=300)
    plt.close()


if (__name__ == "__main__"):
    main()

