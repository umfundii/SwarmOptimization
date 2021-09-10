import numpy as np
import matplotlib.pylab as plt
import sys

if (len(sys.argv) == 1):
    print()
    print("de_pso_particles_iterations_plot <de> <pso>")
    print()
    print("  <de> - DE data")
    print("  <pso>- PSO data")
    print()
    exit(0)

d = np.load(sys.argv[1])
p = np.load(sys.argv[2])

miter = np.linspace(5,100,20)
NP = [5,10,15,20,25,30,35,40]

for i,n in enumerate(NP):
    y = d[i,:].mean(axis=1)
    ey= d[i,:].std(axis=1)/np.sqrt(d.shape[2])
    plt.errorbar(miter,y,ey,marker='o',color='k',label="DE %d" % n)
    y = p[i,:].mean(axis=1)
    ey= p[i,:].std(axis=1)/np.sqrt(d.shape[2])
    plt.errorbar(miter,y,ey,marker='s',color='k',label="PSO %d" % n)
    plt.legend(loc="upper right")
    plt.xlabel("Iteration")
    plt.ylabel("Mean Swarm Best")
    plt.xlim((1,60))
    plt.show()


