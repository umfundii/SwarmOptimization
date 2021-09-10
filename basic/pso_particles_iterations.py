#
#  file:  pso_particles_iterations.py
#
#  Gaussian function example for testing PSO as a function
#  of swarm size and iterations.
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
from PSO import *
from Bounds import *
from RandomInitializer import *
from LinearInertia import *

class Objective:
    def Evaluate(self, p):
        return -5.0*np.exp(-0.5*((p[0]+2.2)**2/0.4+(p[1]-4.3)**2/0.4)) +  \
               -2.0*np.exp(-0.5*((p[0]-2.2)**2/0.4+(p[1]+4.3)**2/0.4))

def main():
    np.random.seed(8675309)
    b = Bounds([-6,-6],[6,6],enforce="resample")
    obj = Objective()

    M = 20
    NP = [5,10,15,20,25,30,35,40]
    MI = np.linspace(5,100,20, dtype="uint8")

    m = np.zeros((len(NP),len(MI),M))

    for I,npart in enumerate(NP):
        for J,miter in enumerate(MI):
            k = 0
            while (k < M):
                ii = RandomInitializer(npart=npart, ndim=2, bounds=b)
                swarm = PSO(obj=obj, npart=npart, ndim=2, max_iter=miter, init=ii, bounds=b,
                           inertia=LinearInertia())
                swarm.Initialize()
                bad = False
                for i in range(miter):
                    swarm.Step()
                    res = swarm.Results()
                    x,y = res["gpos"][-1]
                    v = res["gbest"][-1]
                    if (np.abs(x-2.2) < 0.1) and (np.abs(y+4.3) < 0.1):
                        bad = True
                        break
                    m[I,J,k] = v
                if (bad):
                    continue
                k += 1

    np.save("pso_particles_iterations_results.npy", m)
                 

if (__name__ == "__main__"):
    main()

