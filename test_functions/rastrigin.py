#
#  file:  rastrigin.py
#
#  Minimum of the Rastrigin function (f(0,...,0) = 0)
#
#  RTK, 29-Dec-2019
#  Last update:  07-Aug-2020
#
################################################################

import sys
import time

sys.path.append("../")

from PSO import *
from DE import *
from RO import *
from GWO import *
from Jaya import *
from GA import *

from RandomInitializer import *
from SphereInitializer import *
from QuasirandomInitializer import *
from Bounds import *
from LinearInertia import *

################################################################
#  dist
#
def dist(p):
    """Return the distance from p to the true minimum"""

    m = np.zeros(len(p))
    return  np.sqrt(((p-m)**2).sum())


################################################################
#  Objective
#
class Objective:
    """The objective function"""

    def __init__(self):
        """Constructor"""
        self.fcount = 0
    
    def Evaluate(self, p):
        """Evaluate a position"""
        self.fcount += 1
        return 10*len(p) + (p**2 - 10*np.cos(2*np.pi*p)).sum()
        


################################################################
#  main
#
def main():
    """Rastrigin"""

    if (len(sys.argv) == 1):
        print()
        print("rastrigin <ndim> <npart> <max_iter> <alg> RI|SI|QI")
        print()
        print("  <ndim>     - dimensionality")
        print("  <npart>    - number of swarm particles")
        print("  <max_iter> - number of iterations")
        print("  <alg>      - algorithm: PSO,DE,RO,GWO,JAYA,GA")
        print("  RI|SI|QI   - RI=random, SI=sphere, QI=quasi initializer")
        print()
        return

    ndim = int(sys.argv[1])
    npart = int(sys.argv[2])
    max_iter = int(sys.argv[3])
    alg = sys.argv[4].upper()
    itype = sys.argv[5].upper()

    b = Bounds([-2]*ndim,[2]*ndim)

    if (itype == "SI"):
        i = SphereInitializer(npart, ndim, bounds=b)
    elif (itype == "QI"):
        i = QuasirandomInitializer(npart, ndim, bounds=b)
    else:
        i = RandomInitializer(npart, ndim, bounds=b)

    obj = Objective()

    if (alg == "PSO"):
        swarm = PSO(obj=obj, npart=npart, ndim=ndim, init=i, max_iter=max_iter, bounds=b, inertia=LinearInertia())
    elif (alg == "DE"):
        swarm = DE(obj=obj, npart=npart, ndim=ndim, init=i, max_iter=max_iter, bounds=b)
    elif (alg == "RO"):
        swarm = RO(obj=obj, npart=npart, ndim=ndim, init=i, max_iter=max_iter, bounds=b)
    elif (alg == "CSO"):
        swarm = CSO(obj=obj, npart=npart, ndim=ndim, init=i, max_iter=max_iter, bounds=b)
    elif (alg == "GWO"):
        swarm = GWO(obj=obj, npart=npart, ndim=ndim, init=i, max_iter=max_iter, bounds=b)
    elif (alg == "JAYA"):
        swarm = Jaya(obj=obj, npart=npart, ndim=ndim, init=i, max_iter=max_iter, bounds=b)
    elif (alg == "GA"):
        swarm = GA(obj=obj, npart=npart, ndim=ndim, init=i, max_iter=max_iter, bounds=b)
    else:
        raise ValueError("Unknown algorithm: %s" % alg)

    st = time.time()
    swarm.Optimize()
    en = time.time()

    res = swarm.Results()
    b = res["gbest"][-1]
    p = res["gpos"][-1]
    count = swarm.obj.fcount

    print()
    print("fmin = %0.16e at:" % (b,))
    print("distance from minimum = %0.16e" % dist(p))
    print()
    for i in range(ndim):
        print("    {: .16e}".format(p[i]))
    print()
    print("(%d swarm best updates, %d function evals, time: %0.3f seconds)" % (len(res["gbest"]), count, en-st))
    print()


if (__name__ == "__main__"):
    main()

