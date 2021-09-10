#
#  file:  fxy_runtime.py
#
#  Clock time
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

def main():
    if (len(sys.argv) == 1):
        print()
        print("fxy_precision.py <ntests> <npart> <max> <alg> <RI|QI|SI>")
        print()
        print("  <ntests> - number of precision tests to run")
        print("  <npart>  - number of particles")
        print("  <max>    - max iterations")
        print("  <alg>    - RO,PSO,JAYA,GWO,DE,GA")
        print("  RI|QI|SI - type of initializer")
        print()
        return

    ntests = int(sys.argv[1])
    npart = int(sys.argv[2])
    miter = int(sys.argv[3])
    alg = sys.argv[4].upper()
    itype = sys.argv[5].upper()

    tm = []
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

        if (alg == "RO"):
            swarm = RO(obj=obj, npart=npart, ndim=2, max_iter=miter, init=i, bounds=b)
        elif (alg == "PSO"):
            swarm = PSO(obj=obj, npart=npart, ndim=2, max_iter=miter, init=i, bounds=b,
                        inertia=LinearInertia(), bare=False, bare_prob=0.5, ring=False, neighbors=4)
        elif (alg == "JAYA"):
            swarm = Jaya(obj=obj, npart=npart, ndim=2, max_iter=miter, init=i, bounds=b)
        elif (alg == "GWO2") or (alg == "GWO"):
            swarm = GWO(obj=obj, npart=npart, ndim=2, max_iter=miter, init=i, bounds=b, eta=2)
        elif (alg == "GWO4"):
            swarm = GWO(obj=obj, npart=npart, ndim=2, max_iter=miter, init=i, bounds=b, eta=4)
        elif (alg == "DE"):
            swarm = DE(obj=obj, npart=npart, ndim=2, max_iter=miter, init=i, bounds=b)
        elif (alg == "GA"):
            swarm = GA(obj=obj, npart=npart, ndim=2, max_iter=miter, init=i, bounds=b)
        else:
            raise ValueError("Unknown swarm algorithm: %s" % alg)

        st = time.time()
        swarm.Optimize()
        en = time.time()
        res = swarm.Results()
        x,y = res["gpos"][-1]
        v = res["gbest"][-1]
        
        d = np.sqrt((-2.2-x)**2+(4.3-y)**2)
        if (d < 0.3):
            k += 1
            tm.append(en-st)

    tm = np.array(tm)
    m = tm.mean()
    se= tm.std() / np.sqrt(len(tm))
    print()
    print("Search time: %0.16f +/- %0.16f" % (m,se))
    print()


if (__name__ == "__main__"):
    main()

