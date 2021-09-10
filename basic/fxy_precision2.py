#
#  file:  fxy_precision2.py
#
#  Precision of minimum found - iterations to reach a given
#  error.
#
#  RTK, 27-May-2020
#  Last update:  27-May-2020
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
    if (len(sys.argv) == 1):
        print()
        print("fxy_precision.py <ntests> <tol> <npart> <alg> <RI|QI|SI>")
        print()
        print("  <ntests> - number of precision tests to run")
        print("  <tol>    - tolerance")
        print("  <npart>  - number of particles")
        print("  <alg>    - RO,PSO,JAYA,GWO,DE,GA")
        print("  RI|QI|SI - type of initializer")
        print()
        return

    ntests = int(sys.argv[1])
    tol = float(sys.argv[2])
    npart = int(sys.argv[3])
    alg = sys.argv[4].upper()
    itype = sys.argv[5].upper()

    minutes = 2.5

    print()
    print("%s for %d runs, tolerance = %g:" % (alg, ntests, tol))
    print()

    ans = []
    k = 0
    while (k < ntests):
        b = Bounds([-6,-6],[6,6],enforce="resample")
        obj = Objective()

        if (itype == "QI"):
            i = QuasirandomInitializer(npart=npart, ndim=2, bounds=b)
        elif (itype == "SI"):
            i = SphereInitializer(npart=npart, ndim=2, bounds=b)
        else:
            i = RandomInitializer(npart=npart, ndim=2, bounds=b)

        miter = 10000000

        if (alg == "RO"):
            swarm = RO(obj=obj, npart=npart, ndim=2, max_iter=miter, init=i, bounds=b)
        elif (alg == "PSO"):
            miter = 10000  # omega is a function of max_iter
            swarm = PSO(obj=obj, npart=npart, ndim=2, max_iter=miter, init=i, bounds=b,
                        inertia=LinearInertia(), bare=False, bare_prob=0.5, ring=False, neighbors=4)
        elif (alg == "JAYA"):
            swarm = Jaya(obj=obj, npart=npart, ndim=2, max_iter=miter, init=i, bounds=b)
        elif (alg == "GWO2") or (alg == "GWO"):
            miter = 20000
            swarm = GWO(obj=obj, npart=npart, ndim=2, max_iter=miter, init=i, bounds=b, eta=2)
        elif (alg == "GWO4"):
            miter = 20000
            swarm = GWO(obj=obj, npart=npart, ndim=2, max_iter=miter, init=i, bounds=b, eta=4)
        elif (alg == "DE"):
            swarm = DE(obj=obj, npart=npart, ndim=2, max_iter=miter, init=i, bounds=b)
        elif (alg == "GA"):
            swarm = GA(obj=obj, npart=npart, ndim=2, max_iter=miter, init=i, bounds=b)
        else:
            raise ValueError("Unknown swarm algorithm: %s" % alg)

        swarm.Initialize()
        en = time.time() + 60*minutes
        while (Error(swarm) > tol) and (time.time() < en):
            if (swarm.iterations % 5000) == 0:
                print("  %9d: %0.16f" % (swarm.iterations, Error(swarm)))
            swarm.Step()

        if (time.time() >= en):
            print("  timeout!")
            k += 1
            continue

        res = swarm.Results()
        x,y = res["gpos"][-1]
        
        d = np.sqrt((-2.2-x)**2+(4.3-y)**2)
        if (d < 0.3):
            k += 1
            ans.append(swarm.iterations)

    if (len(ans) != 0):
        ans = np.array(ans)
        m = ans.mean()
        se= ans.std() / np.sqrt(len(ans))
        print()
        print("Iterations to converge: %0.6f +/- %0.6f" % (m,se))
        print()
    else:
        print()
        print("Failed to converge in %0.1f minutes" % minutes)
        print()


if (__name__ == "__main__"):
    main()

