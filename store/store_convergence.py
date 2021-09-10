#
#  file: store_convergence.py
#
#  Plot store convergence as function of iteration.
#
#  RTK, 24-Sep-2020
#  Last update:  24-Sep-2020
#
################################################################

import pickle
import numpy as np
import matplotlib.pylab as plt

def geny(m,gbest,giter):
    y = np.zeros(m)
    for i in range(len(giter)):
        y[giter[i]:] = -gbest[i]
    return y

# DE
d = pickle.load(open("results/de_results.pkl","rb"))
gbest, giter, miter = d["gbest"], d["giter"], d["max_iter"]
x,y = range(miter), geny(miter, gbest, giter)
plt.plot(x[::200],y[::200], marker="P", linestyle='none', color='k', label="DE")
plt.plot(x,y, color='k')

# PSO
d = pickle.load(open("results/pso_results.pkl","rb"))
gbest, giter, miter = d["gbest"], d["giter"], d["max_iter"]
x,y = range(miter), geny(miter, gbest, giter)
plt.plot(x[::200],y[::200], marker="s", linestyle='none', color='k', label="PSO")
plt.plot(x,y, color='k')

# GWO
d = pickle.load(open("results/gwo_results.pkl","rb"))
gbest, giter, miter = d["gbest"], d["giter"], d["max_iter"]
x,y = range(miter), geny(miter, gbest, giter)
plt.plot(x[::200],y[::200], marker="<", linestyle='none', color='k', label="GWO")
plt.plot(x,y, color='k')

# Jaya
d = pickle.load(open("results/jaya_results.pkl","rb"))
gbest, giter, miter = d["gbest"], d["giter"], d["max_iter"]
x,y = range(miter), geny(miter, gbest, giter)
plt.plot(x[::200],y[::200], marker="*", linestyle='none', color='k', label="Jaya")
plt.plot(x,y, color='k')

# GA
d = pickle.load(open("results/ga_results.pkl","rb"))
gbest, giter, miter = d["gbest"], d["giter"], d["max_iter"]
x,y = range(miter), geny(miter, gbest, giter)
plt.plot(x[::200],y[::200], marker=">", linestyle='none', color='k', label="GA")
plt.plot(x,y, color='k')

# RO
d = pickle.load(open("results/ro_results.pkl","rb"))
gbest, giter, miter = d["gbest"], d["giter"], d["max_iter"]
x,y = range(miter), geny(miter, gbest, giter)
plt.plot(x[::200],y[::200], marker="o", linestyle='none', color='k', label="RO")
plt.plot(x,y, color='k')

plt.legend(loc="lower right")
plt.xlabel("Iteration")
plt.ylabel("Revenue")
plt.ylim((185,255))
plt.tight_layout(pad=0, w_pad=0, h_pad=0)
plt.savefig("store_convergence.png", dpi=300)
plt.show()

