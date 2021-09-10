import numpy as np
import matplotlib.pylab as plt
import sys

if (len(sys.argv) == 1):
    print()
    print("de_particles_iterations_plot <data>")
    print()
    print("  <data> - data to plot")
    print()
    exit(0)

d = np.load(sys.argv[1])
miter = np.linspace(5,100,20)
NP = [5,10,15,20,25,30,35,40]
m = ['o','s','*','<','>','P','+','x']

for i,n in enumerate(NP):
    y = d[i,:].mean(axis=1)
    ey= d[i,:].std(axis=1)/np.sqrt(d.shape[2])
    plt.errorbar(miter,y,ey,color='k')
    plt.plot(miter,y,marker=m[i],linestyle='none',color='k',label="%d" % n)

plt.legend(loc="upper right")
plt.xlabel("Iteration")
plt.ylabel("Mean Swarm Best")
plt.xlim((1,60))
plt.show()


