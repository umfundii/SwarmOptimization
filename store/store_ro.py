#
#  file:  store_ro.py
#
#  RTK, 05-Jan-2020
#  Last update:  25-Sep-2020
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
#  Select
#
def Select(fi):
    """Select a product according to these frequencies"""

    t = np.random.random()
    c = 0.0
    for i in range(len(fi)):
        c += fi[i]
        if (c >= t):
            return i


################################################################
#  Shopper
#
class Shopper:
    """Represent a single shopper"""

    def __init__(self, fi, pv):
        """Constructor"""
        self.item_freq = fi
        self.item_values = pv

        #  The shopper wants to buy this product
        self.target = Select(fi)

        #  Now select others the shopper will buy
        #  if encountered
        self.impulse = np.argsort(np.random.random(len(fi)))[:3]
        while (self.target in self.impulse):
            self.impulse = np.argsort(np.random.random(len(fi)))[:3]

    def GoShopping(self, products):
        """Go shopping and return the amount spent"""
        
        spent = 0.0
        for p in products:
            if (p == self.target):
                spent += self.item_values[p]
                break
            if (p in self.impulse):
                spent += self.item_values[p]
        return spent


################################################################
#  Objective
#
class Objective:
    """Simulate a day's worth of customers"""

    def __init__(self, nshoppers, ci, pv):
        """Constructor"""

        self.nshoppers = nshoppers
        self.item_freq = ci / ci.sum()
        self.item_values = pv
        self.fcount = 0
        
        self.shoppers = []
        for i in range(nshoppers):
            shopper = Shopper(self.item_freq, pv)
            self.shoppers.append(shopper)

    def Evaluate(self, p):
        """Evaluate an arrangement of products"""

        self.fcount += 1
        order = np.argsort(p)
        revenue = 0.0
        for i in range(self.nshoppers):
            revenue += self.shoppers[i].GoShopping(order)
        return -revenue


################################################################
#  main
#
def main():
    """Simulate shoppers to find the best arrangement of products"""

    if (len(sys.argv) == 1):
        print()
        print("store_ro <products> <nshoppers> <npart> <niter> RI|SI|QI <eta>")
        print()
        print("  <products>  - store products and shopper data (.pkl)")
        print("  <nshoppers> - number of shoppers per day")
        print("  <npart>     - number of particles")
        print("  <niter>     - number of iterations")
        print("  RI|SI|QI    - random|sphere|quasi initialization")
        print("  <eta>       - RO eta value (e.g. 0.1)")
        print()
        return

    products = pickle.load(open(sys.argv[1],"rb"))
    nshoppers = int(sys.argv[2])
    npart = int(sys.argv[3])
    niter = int(sys.argv[4])
    itype = sys.argv[5].upper()
    eta = float(sys.argv[6])

    #  Item names and frequencies
    ci = products[0]  # product counts
    ni = products[1]  # product names
    pv = products[2]  # product values
    pci = ci / ci.sum()  # probability of being purchased
    N = len(ci)          # number of products

    #  Set up bounds, [0,1], the sort order determines the product number
    ndim = len(ci)
    b = Bounds([0]*ndim, [1]*ndim, enforce="resample")

    if (itype == "QI"):
        i = QuasirandomInitializer(npart, ndim, bounds=b)
    elif (itype == "SI"):
        i = SphereInitializer(npart, ndim, bounds=b)
    else:
        i = RandomInitializer(npart, ndim, bounds=b)

    obj = Objective(nshoppers, ci, pv)

    swarm = RO(obj=obj, npart=npart, ndim=ndim, init=i, max_iter=niter, bounds=b, eta=eta)

    st = time.time()
    swarm.Optimize()
    en = time.time()

    res = swarm.Results()

    print()
    print("Maximum daily revenue $%0.2f (time %0.3f seconds)" % (-res["gbest"][-1], en-st))
    print("(%d best updates, %d function evaluations)" % (len(res["gbest"]), obj.fcount))
    print()
    print("Product order:")
    order = np.argsort(res["gpos"][-1])
    ni = ni[order]
    pci= pci[order]
    pv = pv[order]
    for p in range(len(pv)):
        print("%25s  (%4.1f%%) ($%0.2f)" % (ni[p], 100.0*pci[p], pv[p]))
        if (ni[p] == "whole milk"):
            milk_rank = p
        if (ni[p] == "candy"):
            candy_rank = p
    print()
    print("milk rank = %d" % milk_rank)
    print("candy rank = %d" % candy_rank)
    print()
    print("Upper half median probability of being selected = %4.1f" % (100.0*np.median(pci[:N//2]),))
    print("                           median product value = %4.2f" % (np.median(pv[:N//2]),))
    print("Lower half median probability of being selected = %4.1f" % (100.0*np.median(pci[N//2:]),))
    print("                           median product value = %4.2f" % (np.median(pv[N//2:]),))
    print()

    pickle.dump(res, open("ro_eta_%0.3f_results.pkl" % eta,"wb"))


if (__name__ == "__main__"):
    main()


