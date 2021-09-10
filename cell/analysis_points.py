#
#  file:  analysis_points.py
#
#  Analyze the point placement results
#
#  RTK, 14-Oct-2020
#  Last update: 18-Oct-2020
#
################################################################

import numpy as np
import os
import matplotlib.pylab as plt
from PIL import Image

def Results(alg):
    res = np.zeros((8,8))
    k = 0
    for pnts in range(2,10):
        for runs in range(8):
            fname = "results_points/%s_%d_run%d/README.txt" % (alg.lower(), pnts, runs)
            line = [i[:-1] for i in open(fname) if (i.find("Optimization minimum") != -1)]
            res[k,runs] = -float(line[0].split()[2])
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

print()
for pnts in range(2,10):
    print("%d points:" % pnts)
    m,se,mn,mx = stats(ro[pnts-2,:])
    print("    RO  : %0.5f +/- %0.5f (%0.5f, %0.5f)" % (m,se,mn,mx))
    m,se,mn,mx = stats(de[pnts-2,:])
    print("    DE  : %0.5f +/- %0.5f (%0.5f, %0.5f)" % (m,se,mn,mx))
    m,se,mn,mx = stats(pso[pnts-2,:])
    print("    PSO : %0.5f +/- %0.5f (%0.5f, %0.5f)" % (m,se,mn,mx))
    m,se,mn,mx = stats(gwo[pnts-2,:])
    print("    GWO : %0.5f +/- %0.5f (%0.5f, %0.5f)" % (m,se,mn,mx))
    m,se,mn,mx = stats(jaya[pnts-2,:])
    print("    JAYA: %0.5f +/- %0.5f (%0.5f, %0.5f)" % (m,se,mn,mx))
    m,se,mn,mx = stats(ga[pnts-2,:])
    print("    GA  : %0.5f +/- %0.5f (%0.5f, %0.5f)" % (m,se,mn,mx))
print()

# RO PSO GA DE GWO Jaya
markers = ["o","s",">","X","<","*"]

actual = [np.sqrt(2),np.sqrt(6)-np.sqrt(2),1,np.sqrt(2)/2,np.sqrt(13)/6,
          2*(2-np.sqrt(3)),(np.sqrt(6)-np.sqrt(2))/2,0.5]

for pnts in range(2,10):
    k = 0
    for i in range(8):
        if (i == 0):
            plt.plot(k,actual[pnts-2]-ro[pnts-2,i], marker='o', linestyle='none', color='k', label='RO')
        else:
            plt.plot(k,actual[pnts-2]-ro[pnts-2,i], marker='o', linestyle='none', color='k')
        k += 1
    k += 3
    for i in range(8):
        if (i == 0):
            plt.plot(k,actual[pnts-2]-pso[pnts-2,i], marker='s', linestyle='none', color='k', label='PSO')
        else:
            plt.plot(k,actual[pnts-2]-pso[pnts-2,i], marker='s', linestyle='none', color='k')
        k += 1
    k += 3
    for i in range(8):
        if (i == 0):
            plt.plot(k,actual[pnts-2]-ga[pnts-2,i], marker='>', linestyle='none', color='k', label='GA')
        else:
            plt.plot(k,actual[pnts-2]-ga[pnts-2,i], marker='>', linestyle='none', color='k')
        k += 1
    k += 3
    for i in range(8):
        if (i == 0):
            plt.plot(k,actual[pnts-2]-de[pnts-2,i], marker='X', linestyle='none', color='k', label='DE')
        else:
            plt.plot(k,actual[pnts-2]-de[pnts-2,i], marker='X', linestyle='none', color='k')
        k += 1
    k += 3
    for i in range(8):
        if (i == 0):
            plt.plot(k,actual[pnts-2]-gwo[pnts-2,i], marker='<', linestyle='none', color='k', label='GWO')
        else:
            plt.plot(k,actual[pnts-2]-gwo[pnts-2,i], marker='<', linestyle='none', color='k')
        k += 1
    k += 3
    for i in range(8):
        if (i == 0):
            plt.plot(k,actual[pnts-2]-jaya[pnts-2,i], marker='*', linestyle='none', color='k', label='Jaya')
        else:
            plt.plot(k,actual[pnts-2]-jaya[pnts-2,i], marker='*', linestyle='none', color='k')
        k += 1
    plt.plot([0,k],[0,0], color='k')
    plt.ylim((0,0.2))
    plt.xlabel("Runs")
    plt.ylabel("Distance")
    plt.legend(loc="upper left")
    plt.tight_layout(pad=0,w_pad=0,h_pad=0)
    plt.savefig("points_resample_%d.png" % pnts, dpi=300)
    plt.close()

