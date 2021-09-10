#
#  file:  curves_plot.py
#
#  Take curve fit results and plot progress of the search
#
#  RTK, 31-Dec-2019
#  Last update:  31-Dec-2019
#
################################################################

import numpy as np
import pickle
import matplotlib.pylab as plt
import sys
import os

def GetData(s):
    """Parse a data file"""

    lines = [i for i in open(s)]
    func = lines[0]
    with open("/tmp/xyzzy","w") as f:
        for t in lines[1:]:
            f.write("%s\n" % t)
    d = np.loadtxt("/tmp/xyzzy")
    return d[:,1], d[:,0], func

if (len(sys.argv) == 1):
    print()
    print("curves_plot <results> <source> <outdir>")
    print()
    print("  <results>  -  swarm curve fit results (.pkl)")
    print("  <source>   -  source dataset (.txt)")
    print("  <outdir>   -  output directory (overwritten)")
    print()
    exit(0)

res = pickle.load(open(sys.argv[1],"rb"))
X,Y,func = GetData(sys.argv[2])
outdir = sys.argv[3]

os.system("rm -rf %s; mkdir %s" % (outdir, outdir))

#  Plot mean squared error progress
plt.plot(res["gbest"], color='b')
plt.xlabel("Swarm Bests")
plt.ylabel("Mean Squared Error")
plt.savefig(outdir+"/swarm_bests.png", dpi=300)
plt.show()
plt.close()

#  Plot the curve frames
ymin = Y.min()
if (ymin < 0):
    ymin += 0.1*ymin
else:
    ymin -= 0.1*ymin
ymax = Y.max()
if (ymax < 0):
    ymax -= 0.1*ymax
else:
    ymax += 0.1*ymax

for i, p in enumerate(res["gpos"]):
    x = np.linspace(X.min(), X.max(), 200)
    y = eval(func)
    plt.plot(X,Y, marker='.', linestyle='none', color='r')
    plt.plot(x,y, color='b')
    plt.ylim((ymin,ymax))
    plt.xlabel("x")
    plt.ylabel("y")
    plt.title("Frame %04d" % i)
    plt.savefig(outdir+("/frame_%04d.png" % i), dpi=150)
    plt.close()
    print(".", end="", flush=True)
print()
print()

