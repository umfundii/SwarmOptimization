#
#  file:  analysis.py
#
#  Analyze the cell tower experiment results
#
#  RTK, 05-Oct-2020
#  Last update: 05-Oct-2020
#
################################################################

import numpy as np
import os
import matplotlib.pylab as plt
from PIL import Image

def Results(alg):
    res = np.zeros((2,5,8))
    k = 0
    for tower in ["towers","towers1"]:
        for m in range(5):
            for r in range(8):
                fname = "results/%s_map_%02d_%s_run%d/README.txt" % (alg.lower(), m, tower, r)
                lines = [i[:-1] for i in open(fname)]
                f = float(lines[-3].split()[-4])
                res[k,m,r] = f
        k += 1
    return res

def stats(arg):
    return [
        arg.mean(),
        arg.std(ddof=1) / np.sqrt(len(arg)),
        arg.min(),
        arg.max()]

ro = Results("ro")
de = Results("de")
pso = Results("pso")
gwo = Results("gwo")
jaya = Results("jaya")
ga = Results("ga")

print("'Towers':")
for i in range(5):
    print("    Map %d:" % i)
    m,se,mn,mx = stats(ro[0,i,:])
    print("        RO: %0.5f +/- %0.5f (%0.5f, %0.5f)" % (m,se,mn,mx))
    m,se,mn,mx = stats(de[0,i,:])
    print("        DE: %0.5f +/- %0.5f (%0.5f, %0.5f)" % (m,se,mn,mx))
    m,se,mn,mx = stats(pso[0,i,:])
    print("       PSO: %0.5f +/- %0.5f (%0.5f, %0.5f)" % (m,se,mn,mx))
    m,se,mn,mx = stats(gwo[0,i,:])
    print("       GWO: %0.5f +/- %0.5f (%0.5f, %0.5f)" % (m,se,mn,mx))
    m,se,mn,mx = stats(jaya[0,i,:])
    print("      JAYA: %0.5f +/- %0.5f (%0.5f, %0.5f)" % (m,se,mn,mx))
    m,se,mn,mx = stats(ga[0,i,:])
    print("        GA: %0.5f +/- %0.5f (%0.5f, %0.5f)" % (m,se,mn,mx))
    print()

print("'Towers1':")
for i in range(5):
    print("    Map %d:" % i)
    m,se,mn,mx = stats(ro[1,i,:])
    print("        RO: %0.5f +/- %0.5f (%0.5f, %0.5f)" % (m,se,mn,mx))
    m,se,mn,mx = stats(de[1,i,:])
    print("        DE: %0.5f +/- %0.5f (%0.5f, %0.5f)" % (m,se,mn,mx))
    m,se,mn,mx = stats(pso[1,i,:])
    print("       PSO: %0.5f +/- %0.5f (%0.5f, %0.5f)" % (m,se,mn,mx))
    m,se,mn,mx = stats(gwo[1,i,:])
    print("       GWO: %0.5f +/- %0.5f (%0.5f, %0.5f)" % (m,se,mn,mx))
    m,se,mn,mx = stats(jaya[1,i,:])
    print("      JAYA: %0.5f +/- %0.5f (%0.5f, %0.5f)" % (m,se,mn,mx))
    m,se,mn,mx = stats(ga[1,i,:])
    print("        GA: %0.5f +/- %0.5f (%0.5f, %0.5f)" % (m,se,mn,mx))
    print()

#  Comments:
#    PSO always lowest for 'towers' set, but GA/DE for 'towers1' set
#    for 'towers1' set there are failures.  E.g. PSO map_01 run6 (plot)
#      -- no valid arrangement of towers found (coverage.png shows on roads, etc)
#    for ga_map_02_towers1 -- run 4 fails, all other very good (plot)

plt.plot(np.arange(8)+0.000/1.5, pso[1,1,:], marker='s', color='k', linestyle='none', label='PSO')
plt.plot(np.arange(8)+0.125/1.5, ga[1,1,:], marker='>', color='k', linestyle='none', label='GA')
plt.plot(np.arange(8)+0.250/1.5, ro[1,1,:], marker='o', color='k', linestyle='none', label='RO')
plt.plot(np.arange(8)+0.375/1.5, gwo[1,1,:], marker='<', color='k', linestyle='none', label='GWO')
plt.plot(np.arange(8)+0.500/1.5, de[1,1,:], marker='X', color='k', linestyle='none', label='DE')
plt.plot(np.arange(8)+0.625/1.5, jaya[1,1,:], marker='*', color='k', linestyle='none', label='Jaya')
plt.xlabel("Run")
plt.ylabel("Fraction uncovered")
plt.legend(loc="upper right")
plt.tight_layout(pad=0, w_pad=0, h_pad=0)
plt.savefig("towers1_map_01_failures.png", dpi=300)
plt.show()


