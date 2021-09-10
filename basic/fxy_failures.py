#
#  file:  fxy_failures.py
#
#  Gaussian function example for testing swarm algorithms.
#
#  RTK, 23-May-2020
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


def wdist(x,y):
    return np.sqrt((2.2-x)**2 + (-4.3-y)**2)

def rdist(x,y):
    return np.sqrt((-2.2-x)**2 + (4.3-y)**2)


def main():
    """Run N times and track failures"""

    N = 5000
    npart = 20
    miter = 100
    #b = Bounds([-6,-6],[6,6],enforce="resample")
    b = Bounds([-6,-6],[6,6],enforce="clip")
    obj = Objective()
    i = RandomInitializer(npart=npart, ndim=2, bounds=b)

    threshold = 0.3
    ans = []

    success = fail = wrong = 0
    for j in range(N):
        swarm = RO(obj=obj, npart=npart, ndim=2, max_iter=miter, init=i, bounds=b)
        swarm.Optimize()
        res = swarm.Results()
        x,y = res["gpos"][-1]
        if (wdist(x,y) < 1):
            wrong += 1
        elif (rdist(x,y) < 1):
            success += 1
        else:
            fail += 1
    ans.append([success,fail,wrong])

    success = fail = wrong = 0
    for j in range(N):
        swarm = PSO(obj=obj, npart=npart, ndim=2, max_iter=miter, init=i, bounds=b,
                    inertia=LinearInertia(), bare=False, bare_prob=0.5, ring=False, neighbors=4)
        swarm.Optimize()
        res = swarm.Results()
        x,y = res["gpos"][-1]
        if (wdist(x,y) < 1):
            wrong += 1
        elif (rdist(x,y) < 1):
            success += 1
        else:
            fail += 1
    ans.append([success,fail,wrong])

    success = fail = wrong = 0
    for j in range(N):
        swarm = Jaya(obj=obj, npart=npart, ndim=2, max_iter=miter, init=i, bounds=b)
        swarm.Optimize()
        res = swarm.Results()
        x,y = res["gpos"][-1]
        if (wdist(x,y) < 1):
            wrong += 1
        elif (rdist(x,y) < 1):
            success += 1
        else:
            fail += 1
    ans.append([success,fail,wrong])

    success = fail = wrong = 0
    for j in range(N):
        swarm = GWO(obj=obj, npart=npart, ndim=2, max_iter=miter, init=i, bounds=b)
        swarm.Optimize()
        res = swarm.Results()
        x,y = res["gpos"][-1]
        if (wdist(x,y) < 1):
            wrong += 1
        elif (rdist(x,y) < 1):
            success += 1
        else:
            fail += 1
    ans.append([success,fail,wrong])

    success = fail = wrong = 0
    for j in range(N):
        swarm = GWO(obj=obj, npart=npart, ndim=2, max_iter=miter, init=i, bounds=b, eta=4)
        swarm.Optimize()
        res = swarm.Results()
        x,y = res["gpos"][-1]
        if (wdist(x,y) < 1):
            wrong += 1
        elif (rdist(x,y) < 1):
            success += 1
        else:
            fail += 1
    ans.append([success,fail,wrong])

    success = fail = wrong = 0
    for j in range(N):
        swarm = DE(obj=obj, npart=npart, ndim=2, max_iter=miter, init=i, bounds=b)
        swarm.Optimize()
        res = swarm.Results()
        x,y = res["gpos"][-1]
        if (wdist(x,y) < 1):
            wrong += 1
        elif (rdist(x,y) < 1):
            success += 1
        else:
            fail += 1
    ans.append([success,fail,wrong])

    success = fail = wrong = 0
    for j in range(N):
        swarm = GA(obj=obj, npart=npart, ndim=2, max_iter=miter, init=i, bounds=b)
        swarm.Optimize()
        res = swarm.Results()
        x,y = res["gpos"][-1]
        if (wdist(x,y) < 1):
            wrong += 1
        elif (rdist(x,y) < 1):
            success += 1
        else:
            fail += 1
    ans.append([success,fail,wrong])

    #  Results
    print()
    print("Average number of failures by type:")
    print()
    print("       Success  Failure  Wrong")
    print("RO   : %0.4f   %0.4f   %0.4f" % (ans[0][0]/N, ans[0][1]/N, ans[0][2]/N))
    print("PSO  : %0.4f   %0.4f   %0.4f" % (ans[1][0]/N, ans[1][1]/N, ans[1][2]/N))
    print("Jaya : %0.4f   %0.4f   %0.4f" % (ans[2][0]/N, ans[2][1]/N, ans[2][2]/N))
    print("GWO 2: %0.4f   %0.4f   %0.4f" % (ans[3][0]/N, ans[3][1]/N, ans[3][2]/N))
    print("GWO 4: %0.4f   %0.4f   %0.4f" % (ans[4][0]/N, ans[4][1]/N, ans[4][2]/N))
    print("DE   : %0.4f   %0.4f   %0.4f" % (ans[5][0]/N, ans[5][1]/N, ans[5][2]/N))
    print("GA   : %0.4f   %0.4f   %0.4f" % (ans[6][0]/N, ans[6][1]/N, ans[6][2]/N))
    print()


if (__name__ == "__main__"):
    main()

