#
#  file:  analysis_match.py
#
#  Plots for melody match results
#
#  RTK, 27-Oct-2020
#  Last update:  29-Oct-2020
#
################################################################

import numpy as np
import matplotlib.pylab as plt
import pickle

def Plot(giter, gbest, sym, lbl):
    d = np.zeros(130000)
    for i in range(len(giter)):
        d[giter[i]:] = gbest[i]
    plt.plot(range(130000)[::8000], d[::8000], marker=sym, linestyle='none', color='k', label=lbl)
    plt.plot(range(130000), d, linewidth=1, color='k')

#  Bach
p = pickle.load(open("results/match/bach/de_run1/melody_DE.pkl","rb"))
Plot(p["giter"],p["gbest"], "o", "DE")
p = pickle.load(open("results/match/bach/ro_run1/melody_RO.pkl","rb"))
Plot(p["giter"],p["gbest"], "s", "RO")
p = pickle.load(open("results/match/bach/ga_run1/melody_GA.pkl","rb"))
Plot(p["giter"],p["gbest"], "X", "GA")
p = pickle.load(open("results/match/bach/pso_run1/melody_PSO.pkl","rb"))
Plot(p["giter"],p["gbest"], "<", "PSO")
p = pickle.load(open("results/match/bach/gwo_run1/melody_GWO.pkl","rb"))
Plot(p["giter"],p["gbest"], ">", "GWO")
p = pickle.load(open("results/match/bach/jaya_run1/melody_JAYA.pkl","rb"))
Plot(p["giter"],p["gbest"], "*", "Jaya")

plt.ylim((0,23))
plt.legend(loc="upper right")
plt.tight_layout(pad=0, w_pad=0, h_pad=0)
plt.savefig("match_bach_plot.png", dpi=300)
plt.show()
plt.close()

#  jigs
p = pickle.load(open("results/match/jigs/de_run1/melody_DE.pkl","rb"))
Plot(p["giter"],p["gbest"], "o", "DE")
p = pickle.load(open("results/match/jigs/ro_run1/melody_RO.pkl","rb"))
Plot(p["giter"],p["gbest"], "s", "RO")
p = pickle.load(open("results/match/jigs/ga_run1/melody_GA.pkl","rb"))
Plot(p["giter"],p["gbest"], "X", "GA")
p = pickle.load(open("results/match/jigs/pso_run1/melody_PSO.pkl","rb"))
Plot(p["giter"],p["gbest"], "<", "PSO")
p = pickle.load(open("results/match/jigs/gwo_run1/melody_GWO.pkl","rb"))
Plot(p["giter"],p["gbest"], ">", "GWO")
p = pickle.load(open("results/match/jigs/jaya_run1/melody_JAYA.pkl","rb"))
Plot(p["giter"],p["gbest"], "*", "Jaya")

plt.ylim((0,20))
plt.legend(loc="upper right")
plt.tight_layout(pad=0, w_pad=0, h_pad=0)
plt.savefig("match_jigs_plot.png", dpi=300)
plt.show()
plt.close()


