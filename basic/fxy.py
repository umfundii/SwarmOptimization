#
#  file: fxy.py
#
#  The basic example from Chapter 2.
#
#  RTK, 03-Mar-2020
#  Last update:  03-Mar-2020
#
################################################################

import sys
sys.path.append("../")

import numpy as np
from PSO import *
from DE import *
from LinearInertia import *
from Bounds import *
from RandomInitializer import *

class Objective:
    def Evaluate(self, pos):
        return pos[0]*pos[1]

#  PSO with clipping
npart = 10
ndim = 2
m = 100
tol = 1e-4

b = Bounds([0.01,0.01], [1,1])
i = RandomInitializer(npart, ndim, bounds=b)

swarm = PSO(obj=Objective(), npart=npart, ndim=ndim, init=i, tol=tol, max_iter=m, bounds=b, inertia=LinearInertia())

swarm.Optimize()
res = swarm.Results()
x,y = res["gpos"][-1]
g = res["gbest"][-1]

print()
print("PSO: npart, m = %d, %d (clip)" % (npart, m))
print("    f(%0.8f, %0.8f) = %0.8f" % (x,y,g))
print("    (%d swarm best updates, %d iterations)" % (len(res["gbest"]), res["iterations"]))
print()
print("Swarm bests:")
for i in range(len(res["gbest"])):
    print("    f(%0.8f, %0.8f) = %0.8f" % (res["gpos"][i][0], res["gpos"][i][1], res["gbest"][i]))
print()
print()

#  PSO with resampling
m = 100
npart = 10
b = Bounds([0.01,0.01], [1,1], enforce="resample")
i = RandomInitializer(npart, ndim, bounds=b)

swarm = PSO(obj=Objective(), npart=npart, ndim=ndim, init=i, tol=tol, max_iter=m, bounds=b, inertia=LinearInertia())

swarm.Optimize()
res = swarm.Results()
x,y = res["gpos"][-1]
g = res["gbest"][-1]

print()
print("PSO: npart, m = %d, %d (resample)" % (npart, m))
print("    f(%0.8f, %0.8f) = %0.8f" % (x,y,g))
print("    (%d swarm best updates, %d iterations)" % (len(res["gbest"]), res["iterations"]))
print()
print("Swarm bests:")
for i in range(len(res["gbest"])):
    print("    f(%0.8f, %0.8f) = %0.8f" % (res["gpos"][i][0], res["gpos"][i][1], res["gbest"][i]))
print()
print()

m = 1000
npart = 10
b = Bounds([0.01,0.01], [1,1], enforce="resample")
i = RandomInitializer(npart, ndim, bounds=b)

swarm = PSO(obj=Objective(), npart=npart, ndim=ndim, init=i, tol=tol, max_iter=m, bounds=b, inertia=LinearInertia())

swarm.Optimize()
res = swarm.Results()
x,y = res["gpos"][-1]
g = res["gbest"][-1]

print()
print("PSO: npart, m = %d, %d (resample)" % (npart, m))
print("    f(%0.8f, %0.8f) = %0.8f" % (x,y,g))
print("    (%d swarm best updates, %d iterations)" % (len(res["gbest"]), res["iterations"]))
print()
print("Swarm bests:")
for i in range(len(res["gbest"])):
    print("    f(%0.8f, %0.8f) = %0.8f" % (res["gpos"][i][0], res["gpos"][i][1], res["gbest"][i]))
print()
print()

m = 100
npart = 100
b = Bounds([0.01,0.01], [1,1], enforce="resample")
i = RandomInitializer(npart, ndim, bounds=b)

swarm = PSO(obj=Objective(), npart=npart, ndim=ndim, init=i, tol=tol, max_iter=m, bounds=b, inertia=LinearInertia())

swarm.Optimize()
res = swarm.Results()
x,y = res["gpos"][-1]
g = res["gbest"][-1]

print()
print("PSO: npart, m = %d, %d (resample)" % (npart, m))
print("    f(%0.8f, %0.8f) = %0.8f" % (x,y,g))
print("    (%d swarm best updates, %d iterations)" % (len(res["gbest"]), res["iterations"]))
print()
print("Swarm bests:")
for i in range(len(res["gbest"])):
    print("    f(%0.8f, %0.8f) = %0.8f" % (res["gpos"][i][0], res["gpos"][i][1], res["gbest"][i]))
print()
print()

# differential evolution & resampling
m = 100
npart = 10
b = Bounds([0.01,0.01], [1,1], enforce="resample")
i = RandomInitializer(npart, ndim, bounds=b)

swarm = DE(obj=Objective(), npart=npart, ndim=ndim, init=i, tol=tol, max_iter=m, bounds=b)

swarm.Optimize()
res = swarm.Results()
x,y = res["gpos"][-1]
g = res["gbest"][-1]

print()
print("DE:  npart, m = %d, %d (resample)" % (npart, m))
print("    f(%0.8f, %0.8f) = %0.8f" % (x,y,g))
print("    (%d swarm best updates, %d iterations)" % (len(res["gbest"]), res["iterations"]))
print()
print("Swarm bests:")
for i in range(len(res["gbest"])):
    print("    f(%0.8f, %0.8f) = %0.8f" % (res["gpos"][i][0], res["gpos"][i][1], res["gbest"][i]))
print()

