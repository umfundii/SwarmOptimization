#
#  file:  fxy_convergence.py
#
#  RTK, 24-May-2020
#  Last update:  26-May-2020
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
        print("fxy_convergence.py <npart> <max> <alg> <RI|QI|SI> resample|clip points")
        print()
        print("  <npart>  - number of particles")
        print("  <max>    - max iterations")
        print("  <alg>    - RO,PSO,JAYA,GWO,DE,GA")
        print("  RI|QI|SI - type of initializer")
        print("  resample or clip")
        print("  points   - plot points (.npy)")
        print()
        return

    npart = int(sys.argv[1])
    miter = int(sys.argv[2])
    alg = sys.argv[3].upper()
    itype = sys.argv[4].upper()
    btype = sys.argv[5].lower()
    pname = sys.argv[6]

    np.random.seed(8675309)
    b = Bounds([-6,-6],[6,6],enforce=btype)
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
    elif (alg == "GWO"):
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

    print()
    print("f(%0.8f, %0.8f) = %0.10f" % (x,y,v))
    print("(%d swarm best updates, time = %0.3f seconds)" % (len(res["gbest"]), en-st))
    print()

    g = np.zeros(miter)
    gbest = res["gbest"].copy()
    giter = res["giter"].copy()
    for j,i in enumerate(giter):
        g[i:] = gbest[j]
    np.save(pname, g)


if (__name__ == "__main__"):
    main()

