#
#  file:  curves.py
#
#  Curve fitting with EA/SI.
#
#  RTK, 30-Dec-2019
#  Last update:  31-Dec-2019
#
################################################################

import pickle
import sys
import os
import numpy as np
import time
import matplotlib.pylab as plt

sys.path.append("../")

from PSO import *
from RO import *
from GWO import *
from Jaya import *
from GA import *
from DE import *

from Bounds import *
from RandomInitializer import *
from QuasirandomInitializer import *
from SphereInitializer import *
from LinearInertia import *


################################################################
#  Objective
#
class Objective:
    """Generic objective function"""

    def __init__(self, x, y, func):
        """Constructor"""

        self.x = x
        self.y = y
        self.func = func
        self.fcount = 0

    def Evaluate(self, p):
        """Evaluate a position"""

        self.fcount += 1
        x = self.x
        y = eval(self.func)
        return ((y - self.y)**2).mean()


################################################################
#  GetBounds
#
def GetBounds(s,ndim):
    """Parse a bounds string"""

    if (s.find("x") == -1):
        try:
            n = np.ones(ndim)*float(s)
        except:
            n = None
    else:
        try:
            n = np.array([float(i) for i in s.split("x")])
        except:
            n = None
    return n


################################################################
#  GetData
#
def GetData(s):
    """Parse a data file"""

    lines = [i[:-1] for i in open(s)]
    func = lines[0]
    d = np.zeros((len(lines[1:]),2))
    for i in range(1,len(lines)):
        d[i-1,:] = [float(k) for k in lines[i].split()]
    return d[:,1], d[:,0], func


################################################################
#  main
#
def main():
    """Fit functions to datasets"""

    if (len(sys.argv) == 1):
        print()
        print("curves <data> <lower> <upper> <ndim> <npart> <niter> <tol> <alg> RI|SI|QI <plot> <output>")
        print()
        print("  <data>   - Text file w/coordinates (y x), function (first line) (.txt)")
        print("  <lower>  - lower parameter bounds")
        print("  <upper>  - upper parameter bounds")
        print("  <ndim>   - number of parameters")
        print("  <npart>  - number of particles")
        print("  <niter>  - number of iterations")
        print("  <tol>    - tolerance (quit if error less than)")
        print("  <alg>    - PSO,RO,GWO,JAYA,GA,DE")
        print("  RI|SI|QI - random|sphere|quasi initialization")
        print("  <plot>   - show fit plot")
        print("  <output> - store the results here (.pkl)")
        print()
        return

    #  Get the parameters
    X,Y,func = GetData(sys.argv[1])
    ndim = int(sys.argv[4])
    lower = GetBounds(sys.argv[2], ndim)
    upper = GetBounds(sys.argv[3], ndim)
    npart = int(sys.argv[5])
    niter = int(sys.argv[6])
    tol = float(sys.argv[7])
    alg = sys.argv[8].upper()
    itype = sys.argv[9].upper()

    #  Setup
    if (type(lower) is type(None)) and (type(upper) is type(None)):
        b = None
    else:
        b = Bounds(lower, upper, enforce="resample")

    if (itype == "QI"):
        i = QuasirandomInitializer(npart, ndim, bounds=b)
    elif (itype == "SI"):
        i = SphereInitializer(npart, ndim, bounds=b)
    else:
        i = RandomInitializer(npart, ndim, bounds=b)

    obj = Objective(X, Y, func)

    if (alg == "PSO"):
        swarm = PSO(obj=obj, npart=npart, ndim=ndim, init=i, tol=tol, max_iter=niter, bounds=b, inertia=LinearInertia())
    elif (alg == "RO"):
        swarm = RO(obj=obj, npart=npart, ndim=ndim, init=i, tol=tol, max_iter=niter, bounds=b)
    elif (alg == "GWO"):
        swarm = GWO(obj=obj, npart=npart, ndim=ndim, init=i, tol=tol, max_iter=niter, bounds=b)
    elif (alg == "JAYA"):
        swarm = Jaya(obj=obj, npart=npart, ndim=ndim, init=i, tol=tol, max_iter=niter, bounds=b)
    elif (alg == "GA"):
        swarm = GA(obj=obj, npart=npart, ndim=ndim, init=i, tol=tol, max_iter=niter, bounds=b)
    elif (alg == "DE"):
        swarm = DE(obj=obj, npart=npart, ndim=ndim, init=i, tol=tol, max_iter=niter, bounds=b)
    else:
        raise ValueError("Unknown algorithm: %s" % alg)

    st = time.time()
    swarm.Optimize()
    en = time.time()

    res = swarm.Results()

    print()
    print("Minimum mean total squared error: %0.9f  (%s)" % (res["gbest"][-1],os.path.basename(sys.argv[1])))
    print("Parameters:")
    for k,p in enumerate(res["gpos"][-1]):
        print("%2d: %21.16f" % (k,p))
    print("(%d best updates, %d function calls, time: %0.3f seconds)" % (len(res["gbest"]), swarm.obj.fcount, en-st))
    print()

    if (len(sys.argv) >= 11):
        x = np.linspace(X.min(),X.max(),200)
        p = res["gpos"][-1]
        y = eval(func)
        plt.plot(x,y,color='b')
        plt.plot(X,Y,color='r',marker='.',linestyle='none')
        plt.xlabel("$x$")
        plt.ylabel("$y$")
        plt.savefig(sys.argv[10], dpi=300)
        #plt.show()

    if (len(sys.argv) >= 12):
        pickle.dump(res, open(sys.argv[11],"wb"))


if (__name__ == "__main__"):
    main()

