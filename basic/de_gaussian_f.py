#
#  file:  de_gaussian_f.py
#
#  Gaussian function example for DE and F.
#
#  RTK, 13-Jul-2020
#  Last update:  13-Jul-2020
#
################################################################

import time
import os
import sys
sys.path.append("../")

import numpy as np
import matplotlib.pylab as plt
from DE import *

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

    fs = [0.0, 0.05, 0.1, 0.15, 0.2, 0.25,
          0.3, 0.35, 0.4, 0.45, 0.5, 0.6, 
          0.7, 0.8, 0.9, 1.0]

    # CR=0.8
    print("CR=0.5")
    d = np.zeros(len(fs))
    e = np.zeros(len(fs))

    for k,f in enumerate(fs):
        m = []
        s = w = ff = 0
        for i in range(runs):
            swarm = DE(obj=obj, npart=npart, ndim=2, max_iter=miter, init=ri, bounds=b, F=f)
            swarm.Optimize()
            res = swarm.Results()
            x,y = res["gpos"][-1]
            if (wdist(x,y) < 1):
                w += 1
            elif (rdist(x,y) < 1):
                m.append(res["gbest"][-1])
                s += 1
            else:
                ff += 1
        m = np.array(m)
        print("F=%0.2f, minimum= %0.7f +/- %0.7f (success=%3d, wrong=%3d, fail=%3d)" % (f, m.mean(), m.std()/np.sqrt(m.shape[0]), s,w,ff))
        d[k] = m.mean()
        e[k] = m.std()/np.sqrt(m.shape[0])

    print()

    # CR=0
    print("CR=0.0")
    dd = np.zeros(len(fs))
    ee = np.zeros(len(fs))

    for k,f in enumerate(fs):
        m = []
        s = w = ff = 0
        for i in range(runs):
            swarm = DE(obj=obj, npart=npart, ndim=2, max_iter=miter, init=ri, bounds=b, F=f, CR=0.0)
            swarm.Optimize()
            res = swarm.Results()
            x,y = res["gpos"][-1]
            if (wdist(x,y) < 1):
                w += 1
            elif (rdist(x,y) < 1):
                m.append(res["gbest"][-1])
                s += 1
            else:
                ff += 1
        m = np.array(m)
        print("F=%0.2f, minimum= %0.7f +/- %0.7f (success=%3d, wrong=%3d, fail=%3d)" % (f, m.mean(), m.std()/np.sqrt(m.shape[0]), s,w,ff))
        dd[k] = m.mean()
        ee[k] = m.std()/np.sqrt(m.shape[0])

    plt.errorbar(fs,d,e, marker='o', color='k', label="CR=0.8")
    plt.errorbar(fs,dd,ee, marker='s', color='k', label="CR=0.0")
    plt.legend(loc="upper right")
    plt.xlabel("F")
    plt.ylabel("Average Minimum")
    plt.tight_layout(pad=0, w_pad=0, h_pad=0)
    plt.savefig("de_gaussian_f_plot.png", dpi=300)
    plt.close()
    print()

    mk = ['o','s','*','^','<']
    cs = ['r','g','b','m','k']

    fs = [0.0, 0.2, 0.5, 0.8, 1.0]

    np.random.seed(73939133)
    obj = Objective()

    for k,f in enumerate(fs):
        D = np.zeros((runs,miter))
        for i in range(runs):
            b = Bounds([-6,-6],[6,6],enforce="resample")
            ri = RandomInitializer(npart=npart, ndim=2, bounds=b)
            swarm = DE(obj=obj, npart=npart, ndim=2, max_iter=miter, init=ri, bounds=b, F=f)
            swarm.Initialize()
            d = np.zeros(miter)
            for j in range(miter):
                swarm.Step()
                Dispersion(swarm, j, d)
                res = swarm.Results()
            D[i,:] = d
        plt.plot(np.arange(miter)[::5],D.mean(axis=0)[::5], marker=mk[k],
                 linestyle='none', color=cs[k], label='$F=%0.2f$' % f)
        plt.plot(D.mean(axis=0), color=cs[k])
    
    plt.legend(loc='upper right')
    plt.xlabel('Generation')
    plt.ylabel('Dispersion')
    plt.tight_layout(pad=0, w_pad=0, h_pad=0)
    plt.savefig("de_gaussian_f_dispersion_plot.png", dpi=300)
    plt.close()

    np.random.seed(73939133)
    obj = Objective()

    for k,f in enumerate(fs):
        v = np.zeros((runs,miter))
        for i in range(runs):
            b = Bounds([-6,-6],[6,6],enforce="resample")
            ri = RandomInitializer(npart=npart, ndim=2, bounds=b)
            swarm = DE(obj=obj, npart=npart, ndim=2, max_iter=miter, init=ri, bounds=b, F=f)
            swarm.Initialize()
            for j in range(miter):
                swarm.Step()
                Dispersion(swarm, j, d)
                res = swarm.Results()
                v[i,j] = res["gbest"][-1]
        plt.plot(np.arange(miter)[::5],v.mean(axis=0)[::5], marker=mk[k], 
                 linestyle='none', color=cs[k], label='$F=%0.2f$' % f)
        plt.plot(v.mean(axis=0), color=cs[k])
    
    plt.legend(loc='upper right')
    plt.xlabel('Generation')
    plt.ylabel('Swarm Best')
    plt.tight_layout(pad=0, w_pad=0, h_pad=0)
    plt.savefig("de_gaussian_f_best_plot.png", dpi=300)
    plt.close()


if (__name__ == "__main__"):
    main()

