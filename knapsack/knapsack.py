#
#  file:  knapsack.py
#
#  0-1 knapsack problem
#
#  RTK, 28-Dec-2019
#  Last update:  11-Aug-2020
#
################################################################

import time
import os
import sys
import pickle

import numpy as np

sys.path.append("../")

from Jaya import *
from GWO import *
from PSO import *
from DE import *
from RO import *
from GA import *

from RandomInitializer import *
from Bounds import *
from LinearInertia import *


################################################################
#  KnapsackBounds
#
class KnapsackBounds(Bounds):
    """Subclass of Bounds to enforce 0|1"""

    def __init__(self, lower, upper):
        """Constructor"""

        super().__init__(lower, upper, enforce="resample")

    def Validate(self, p):
        """Enforce discretization and weight limit"""

        p[np.where(p < 0.5)] = 0
        p[np.where(p >= 0.5)]= 1

        return p.astype("float64")


################################################################
#  Objective
#
class Objective:
    """Objective for knapsack problem"""

    def __init__(self, values, weights, max_weight):
        """Store limits"""

        self.values = values
        self.weights= weights
        self.max_weight = max_weight
        self.fcount = 0

    def Evaluate(self, p):
        """Evaluate a given set of objects"""

        self.fcount += 1
        value = (self.values*p).sum()
        weight= (self.weights*p).sum()
        if (weight > self.max_weight):
            return 1e9
        return -value


################################################################
#  LoadProblemFile
#
def LoadProblemFile(fname):
    """Load a knapsack problem file"""

    lines = [i for i in open(fname)]
    n,wmax = [float(i) for i in lines[0].split()]
    n = int(n)
    values = np.zeros(n)
    weights= np.zeros(n)
    for i in range(n):
        v,w = [float(j) for j in lines[i+1].split()]
        values[i] = v
        weights[i] = w
    return values, weights, wmax


################################################################
#  main
#
def main():
    """0-1 Knapsack problem"""

    if (len(sys.argv) == 1):
        print()
        print("knapsack <problem> <npart> <max_iter> <alg> [<results>]")
        print()
        print("  <problem>        - knapsack problem definition file")
        print("  <npart>          - swarm size (template sets dimensions)")
        print("  <max_iter>       - maximum number of iterations")
        print("  <alg>            - algorithm: PSO,DE,RO,GWO,JAYA,GA")
        print("  <results>        - store results here (optional, .pkl)")
        print()
        return

    npart = int(sys.argv[2])
    max_iter = int(sys.argv[3])
    alg = sys.argv[4].upper()
    itype = sys.argv[5].upper()

    values, weights, max_weight = LoadProblemFile(sys.argv[1])

    obj = Objective(values, weights, max_weight)
    ndim = values.shape[0]
    b = KnapsackBounds([0]*ndim, [1]*ndim)
    ri = RandomInitializer(npart, ndim, bounds=b)

    if (alg == "PSO"):
        swarm = PSO(obj=obj, npart=npart, ndim=ndim, max_iter=max_iter, init=ri, bounds=b,
                    inertia=LinearInertia())
    elif (alg == "DE"):
        swarm = DE(obj=obj, npart=npart, ndim=ndim, max_iter=max_iter, init=ri, bounds=b)
    elif (alg == "RO"):
        swarm = RO(obj=obj, npart=npart, ndim=ndim, max_iter=max_iter, init=ri, bounds=b)
    elif (alg == "GWO"):
        swarm = GWO(obj=obj, npart=npart, ndim=ndim, max_iter=max_iter, init=ri, bounds=b)
    elif (alg == "JAYA"):
        swarm = Jaya(obj=obj, npart=npart, ndim=ndim, max_iter=max_iter, init=ri, bounds=b)
    elif (alg == "GA"):
        swarm = GA(obj=obj, npart=npart, ndim=ndim, max_iter=max_iter, init=ri, bounds=b)
    else:
        raise ValueError("Unknown swarm algorithm: %s" % alg)

    st = time.time()
    swarm.Optimize()
    en = time.time()

    res = swarm.Results()
    fcount = swarm.obj.fcount

    weight = (weights*res["gpos"][-1]).sum()

    print()
    print("Final value=%0.2f, weight=%0.1f/%0.1f, objects:" % (-res["gbest"][-1], weight, max_weight))
    print()
    print(np.array2string(res["gpos"][-1].astype("uint8")))
    print()
    print("(%d swarm best updates, %d function evals, time: %0.3f seconds)" % (len(res["gbest"]), fcount, en-st,))
    print()

    if (len(sys.argv) == 6):
        pickle.dump(res, open(sys.argv[5],"wb"))


if (__name__ == "__main__"):
    main()

