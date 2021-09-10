#
#  file:  fxy_pso_precision.py
#
#  Effect of max iterations on PSO convergence.
#
#  RTK, 27-May-2020
#  Last update:  28-May-2020
#
################################################################

import time
import os
import sys
sys.path.append("../")

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

def Error(swarm):
    res = swarm.Results()
    return np.abs(-5.0 - res["gbest"][-1])

def main():
    
    npart = 20
    tol = 1e-8

    for miter in [100,500,1000,5000,10000,50000,100000]:
        ans = []
        k = 0
        while (k < 20):
            b = Bounds([-6,-6],[6,6],enforce="resample")
            obj = Objective()
            i = RandomInitializer(npart=npart, ndim=2, bounds=b)

            swarm = PSO(obj=obj, npart=npart, ndim=2, max_iter=miter, init=i, bounds=b,
                        inertia=LinearInertia(), bare=False, bare_prob=0.5, ring=False, neighbors=4)

            swarm.Initialize()
            while (Error(swarm) > tol):
                swarm.Step()
            res = swarm.Results()
            x,y = res["gpos"][-1]
            
            d = np.sqrt((-2.2-x)**2+(4.3-y)**2)
            if (d < 0.3):
                k += 1
                ans.append(swarm.iterations)

        ans = np.array(ans)
        m = ans.mean()
        se= ans.std() / np.sqrt(len(ans))
        print("(miter=%6d), iterations: %0.6f +/- %0.6f" % (miter, m,se))
    print()


if (__name__ == "__main__"):
    main()

