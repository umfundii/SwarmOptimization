#
#  file:  test_functions.py
#
#  Test the standard functions
#
#  RTK, 07-Aug-2020
#  Last update:  08-Aug-2020
#
################################################################

import sys
import time
import pickle

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
def dist(p, func):
    """Return the distance from p to the true minimum"""

    if (func == "sphere"):
        m = np.zeros(len(p))
    elif (func == "beale"):
        m = np.array([3, 0.5])
    elif (func == "easom"):
        m = np.pi*np.ones(2)
    elif (func == "rastrigin"):
        m = np.zeros(len(p))
    elif (func == "rosenbrock"):
        m = np.ones(len(p))

    return  np.sqrt(((p-m)**2).sum())


################################################################
#  Objectives
#
class SphereObjective:
    def __init__(self):
        """Constructor"""
        self.fcount = 0
    
    def Evaluate(self, p):
        """Evaluate a position"""
        self.fcount += 1
        return (p**2).sum() 

class BealeObjective:
    def __init__(self):
        """Constructor"""
        self.fcount = 0
    
    def Evaluate(self, p):
        """Evaluate a position"""
        self.fcount += 1
        return (1.5 - p[0] + p[0]*p[1])**2     +  \
               (2.25 - p[0] + p[0]*p[1]**2)**2 +  \
               (2.625 - p[0] + p[0]*p[1]**3)**2

class EasomObjective:
    def __init__(self):
        """Constructor"""
        self.fcount = 0
    
    def Evaluate(self, p):
        """Evaluate a position"""
        self.fcount += 1
        return -np.cos(p[0])*np.cos(p[1])*np.exp(-((p[0]-np.pi)**2+(p[1]-np.pi)**2)) 

class RastriginObjective:
    def __init__(self):
        """Constructor"""
        self.fcount = 0
    
    def Evaluate(self, p):
        """Evaluate a position"""
        self.fcount += 1
        return 10*len(p) + (p**2 - 10*np.cos(2*np.pi*p)).sum()

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

def FunctionObjective(func):
    if (func == "sphere"):
        return SphereObjective()
    elif (func == "beale"):
        return BealeObjective()
    elif (func == "easom"):
        return EasomObjective()
    elif (func == "rastrigin"):
        return RastriginObjective()
    elif (func == "rosenbrock"):
        return RosenbrockObjective()


################################################################
#  main
#
def main():
    """Test the standard functions"""

    if (len(sys.argv) == 1):
        print()
        print("test_functions sphere|beale|easom|rastrigin|rosenbrock <npart> <niter> <output>")
        print()
        print("  <npart> - number of particles")
        print("  <niter> - number of iterations")
        print("  <output>- output .pkl file")
        print()
        return

    func = sys.argv[1].lower()
    npart = int(sys.argv[2])
    miter = int(sys.argv[3])
    itype = "RI"
    navg = 10

    results = [] 

    for alg in ["RO","PSO","DE","GWO","JAYA","GA"]:
        for ndim in [3,10,25,50]:
            max_iter = (miter*ndim)//3  # increase iterations w/dimensions
            rang = 1.1
            if (func in ["beale","easom"]):
                if (ndim == 3):
                    ndim = 2
                    rang = 4
                else:
                    continue
            r = np.zeros((navg,ndim+2))
            for m in range(navg):
                b = Bounds([-rang]*ndim,[rang]*ndim)

                if (itype == "SI"):
                    i = SphereInitializer(npart, ndim, bounds=b)
                elif (itype == "QI"):
                    i = QuasirandomInitializer(npart, ndim, bounds=b)
                else:
                    i = RandomInitializer(npart, ndim, bounds=b)

                obj = FunctionObjective(func)

                if (alg == "PSO"):
                    swarm = PSO(obj=obj, npart=npart, ndim=ndim, init=i, max_iter=max_iter, bounds=b, inertia=LinearInertia())
                elif (alg == "DE"):
                    swarm = DE(obj=obj, npart=npart, ndim=ndim, init=i, max_iter=max_iter, bounds=b)
                elif (alg == "RO"):
                    swarm = RO(obj=obj, npart=npart, ndim=ndim, init=i, max_iter=max_iter, bounds=b)
                elif (alg == "GWO"):
                    swarm = GWO(obj=obj, npart=npart, ndim=ndim, init=i, max_iter=max_iter, bounds=b)
                elif (alg == "JAYA"):
                    swarm = Jaya(obj=obj, npart=npart, ndim=ndim, init=i, max_iter=max_iter, bounds=b)
                elif (alg == "GA"):
                    swarm = GA(obj=obj, npart=npart, ndim=ndim, init=i, max_iter=max_iter, bounds=b)
                else:
                    raise ValueError("Unknown algorithm: %s" % alg)

                swarm.Optimize()

                res = swarm.Results()
                r[m,0] = res["gbest"][-1]
                p = res["gpos"][-1]
                r[m,1] = dist(p, func)
                r[m,2:] = p
            
            rmean = r.mean(axis=0)
            rSE = r.std(axis=0, ddof=1) / np.sqrt(navg)
            results.append([alg, ndim, max_iter, rmean, rSE])

    pickle.dump(results, open(sys.argv[4],"wb"))


if (__name__ == "__main__"):
    main()

