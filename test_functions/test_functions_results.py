#
#  file:  test_functions_results.py
#
#  Summarize the test function by algorithm type and dimensions
#
#  RTK, 08-Aug-2020
#  Last update:  08-Aug-2020
#
################################################################

import numpy as np
import pickle
import sys

fname = sys.argv[1]
d = pickle.load(open(fname,"rb"))

if (fname.find("beale") != -1) or (fname.find("easom") != -1):
    ro = [d[0][3][0],d[0][3][1],d[0][4][0],d[0][4][1]]
    pso= [d[1][3][0],d[1][3][1],d[1][4][0],d[1][4][1]]
    de = [d[2][3][0],d[2][3][1],d[2][4][0],d[2][4][1]]
    gwo= [d[3][3][0],d[3][3][1],d[3][4][0],d[3][4][1]]
    jay= [d[4][3][0],d[4][3][1],d[4][4][0],d[4][4][1]]
    ga = [d[5][3][0],d[5][3][1],d[5][4][0],d[5][4][1]]
    print("    RO  : min: %0.12f +/- %0.12f, dist: %0.12f +/- %0.12f" % (ro[0],ro[2],ro[1],ro[3]))
    print("    PSO : min: %0.12f +/- %0.12f, dist: %0.12f +/- %0.12f" % (pso[0],pso[2],pso[1],pso[3]))
    print("    DE  : min: %0.12f +/- %0.12f, dist: %0.12f +/- %0.12f" % (de[0],de[2],de[1],de[3]))
    print("    GWO : min: %0.12f +/- %0.12f, dist: %0.12f +/- %0.12f" % (gwo[0],gwo[2],gwo[1],gwo[3]))
    print("    Jaya: min: %0.12f +/- %0.12f, dist: %0.12f +/- %0.12f" % (jay[0],jay[2],jay[1],jay[3]))
    print("    GA  : min: %0.12f +/- %0.12f, dist: %0.12f +/- %0.12f" % (ga[0],ga[2],ga[1],ga[3]))
    print()
else:
    b = 0
    for i in range(4):
        ro = [d[b+ 0][3][0],d[b+ 0][3][1],d[b+ 0][4][0],d[b+ 0][4][1]]
        pso= [d[b+ 4][3][0],d[b+ 4][3][1],d[b+ 4][4][0],d[b+ 4][4][1]]
        de = [d[b+ 8][3][0],d[b+ 8][3][1],d[b+ 8][4][0],d[b+ 8][4][1]]
        gwo= [d[b+12][3][0],d[b+12][3][1],d[b+12][4][0],d[b+12][4][1]]
        jay= [d[b+16][3][0],d[b+16][3][1],d[b+16][4][0],d[b+16][4][1]]
        ga = [d[b+20][3][0],d[b+20][3][1],d[b+20][4][0],d[b+20][4][1]]
        m = d[b+0][1]
        k = d[b+0][2]
        b += 1
        print("%d dimensions, %d iterations:" % (m,k))
        print("    RO  : min: %0.12f +/- %0.12f, dist: %0.12f +/- %0.12f" % (ro[0],ro[2],ro[1],ro[3]))
        print("    PSO : min: %0.12f +/- %0.12f, dist: %0.12f +/- %0.12f" % (pso[0],pso[2],pso[1],pso[3]))
        print("    DE  : min: %0.12f +/- %0.12f, dist: %0.12f +/- %0.12f" % (de[0],de[2],de[1],de[3]))
        print("    GWO : min: %0.12f +/- %0.12f, dist: %0.12f +/- %0.12f" % (gwo[0],gwo[2],gwo[1],gwo[3]))
        print("    Jaya: min: %0.12f +/- %0.12f, dist: %0.12f +/- %0.12f" % (jay[0],jay[2],jay[1],jay[3]))
        print("    GA  : min: %0.12f +/- %0.12f, dist: %0.12f +/- %0.12f" % (ga[0],ga[2],ga[1],ga[3]))
        print()

