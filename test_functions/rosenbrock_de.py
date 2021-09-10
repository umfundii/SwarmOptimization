#
#  file:  rosenbrock_de.py
#
#  Generate a 2D map of DE's results on the 20-dimensional
#  rosenbrock function.
#
#  RTK, 09-Aug-2020
#  Last update:  09-Aug-2020
#
################################################################

import sys
import time
import pickle

sys.path.append("../")

from DE import *

from RandomInitializer import *
from Bounds import *

################################################################
#  dist
#
def dist(p):
    """Return the distance from p to the true minimum"""

    m = np.ones(len(p))
    return  np.sqrt(((p-m)**2).sum())


################################################################
#  RosenbrockObjective
#
class RosenbrockObjective:
    def __init__(self):
        """Constructor"""
        self.fcount = 0
    
    def Evaluate(self, p):
        """Evaluate a position"""
        self.fcount += 1
        s = 0.0
        for i in range(len(p)-1):
            s += 100*(p[i+1]-p[i]**2)**2 + (1-p[i])**2
        return s


################################################################
#  main
#
def main():
    """Evaluate DE's performance on the Rosenbrock function"""

    if (len(sys.argv) == 1):
        print()
        print("rosenbrock_de <output>")
        print()
        print("  <output> - output filename")
        print()
        return

    outname = sys.argv[1]
    navg = 6
    ndim = 22

    results = [] 

    for npart in [10,20,30,40,50,60,70,80,90,100]:
        for max_iter in [100,5000,10000,15000,20000,25000,30000,35000,40000,45000,50000]:
            r = np.zeros(navg)
            for m in range(navg):
                b = Bounds([-1.1]*ndim,[1.1]*ndim)
                i = RandomInitializer(npart, ndim, bounds=b)
                obj = RosenbrockObjective()
                swarm = DE(obj=obj, npart=npart, ndim=ndim, init=i, max_iter=max_iter, bounds=b)
                swarm.Optimize()
                res = swarm.Results()
                p = res["gpos"][-1]
                r[m] = dist(p)
            rmean = r.mean(axis=0)
            rSE = r.std(axis=0, ddof=1) / np.sqrt(navg)
            results.append([npart, max_iter, rmean, rSE])
            print("npart: %3d, max_iter: %6d, dist: %0.16f +/- %0.16f" % (npart, max_iter, rmean, rSE), flush=True)
    
    results = np.array(results)
    np.save(outname, results)


if (__name__ == "__main__"):
    main()

