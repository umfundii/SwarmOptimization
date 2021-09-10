#
#  file:  brute_force.py
#
#  Brute force solution to 0-1 knapsack
#
#  RTK, 13-Aug-2020
#  Last update:  13-Aug-2020
#
################################################################

import time
import os
import sys
import pickle
import numpy as np

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
#  BinaryVector
#
def BinaryVector(n, ndigits):
    """Convert an int to a binary vector"""

    t = "0"*10000
    b = t + bin(n)[2:]
    b = b[-ndigits:]
    return np.array([int(i) for i in list(b)])
        

################################################################
#  main
#
def main():
    """0-1 Knapsack problem - brute force"""

    if (len(sys.argv) == 1):
        print()
        print("knapsack <problem> [<results>]")
        print()
        print("  <problem>        - knapsack problem definition file")
        print()
        return

    values, weights, max_weight = LoadProblemFile(sys.argv[1])
    mval = mweight = 0.0

    for n in range(2**len(values)):
        b = BinaryVector(n, len(values))
        weight = (weights*b).sum()
        value = (values*b).sum()
        if (weight <= max_weight) and (value >= mval):
            mval = value
            mweight = weight
            mb = b.copy()
    
    print()
    print("maximum value: %0.0f, weight %0.0f/%0.0f" % (mval, mweight, max_weight))
    print()
    print(mb)
    print()

if (__name__ == "__main__"):
    main()

