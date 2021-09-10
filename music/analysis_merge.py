#
#  file:  analysis_merge.py
#
#  Plots for melody merge results
#
#  RTK, 27-Oct-2020
#  Last update:  27-Oct-2020
#
################################################################

import numpy as np
import matplotlib.pylab as plt
import pickle

def Plot(giter, gbest, sym, lbl):
    d = np.zeros(10000)
    for i in range(len(giter)):
        d[giter[i]:] = gbest[i]
    plt.plot(range(10000)[::800], d[::800], marker=sym, linestyle='none', color='k', label=lbl)
    plt.plot(range(10000), d, linewidth=1, color='k')

#  alpha = 0.5
p = pickle.load(open("results/merge/mary_ode_alpha_0.5_DE/results.pkl","rb"))
Plot(p["giter"],p["gbest"], "o", "DE")
p = pickle.load(open("results/merge/mary_ode_alpha_0.5_RO/results.pkl","rb"))
Plot(p["giter"],p["gbest"], "s", "RO")
p = pickle.load(open("results/merge/mary_ode_alpha_0.5_GA/results.pkl","rb"))
Plot(p["giter"],p["gbest"], "X", "GA")
p = pickle.load(open("results/merge/mary_ode_alpha_0.5_PSO/results.pkl","rb"))
Plot(p["giter"],p["gbest"], "<", "PSO")
p = pickle.load(open("results/merge/mary_ode_alpha_0.5_GWO/results.pkl","rb"))
Plot(p["giter"],p["gbest"], ">", "GWO")
p = pickle.load(open("results/merge/mary_ode_alpha_0.5_JAYA/results.pkl","rb"))
Plot(p["giter"],p["gbest"], "*", "Jaya")

plt.legend(loc="upper right")
plt.tight_layout(pad=0, w_pad=0, h_pad=0)
plt.savefig("merge_0.5_plot.png", dpi=300)
plt.show()
plt.close()

#  alpha = 0.1
p = pickle.load(open("results/merge/mary_ode_alpha_0.1_DE/results.pkl","rb"))
Plot(p["giter"],p["gbest"], "o", "DE")
p = pickle.load(open("results/merge/mary_ode_alpha_0.1_RO/results.pkl","rb"))
Plot(p["giter"],p["gbest"], "s", "RO")
p = pickle.load(open("results/merge/mary_ode_alpha_0.1_GA/results.pkl","rb"))
Plot(p["giter"],p["gbest"], "X", "GA")
p = pickle.load(open("results/merge/mary_ode_alpha_0.1_PSO/results.pkl","rb"))
Plot(p["giter"],p["gbest"], "<", "PSO")
p = pickle.load(open("results/merge/mary_ode_alpha_0.1_GWO/results.pkl","rb"))
Plot(p["giter"],p["gbest"], ">", "GWO")
p = pickle.load(open("results/merge/mary_ode_alpha_0.1_JAYA/results.pkl","rb"))
Plot(p["giter"],p["gbest"], "*", "Jaya")

plt.legend(loc="upper right")
plt.tight_layout(pad=0, w_pad=0, h_pad=0)
plt.savefig("merge_0.1_plot.png", dpi=300)
plt.show()
plt.close()

#  alpha = 0.9
p = pickle.load(open("results/merge/mary_ode_alpha_0.9_DE/results.pkl","rb"))
Plot(p["giter"],p["gbest"], "o", "DE")
p = pickle.load(open("results/merge/mary_ode_alpha_0.9_RO/results.pkl","rb"))
Plot(p["giter"],p["gbest"], "s", "RO")
p = pickle.load(open("results/merge/mary_ode_alpha_0.9_GA/results.pkl","rb"))
Plot(p["giter"],p["gbest"], "X", "GA")
p = pickle.load(open("results/merge/mary_ode_alpha_0.9_PSO/results.pkl","rb"))
Plot(p["giter"],p["gbest"], "<", "PSO")
p = pickle.load(open("results/merge/mary_ode_alpha_0.9_GWO/results.pkl","rb"))
Plot(p["giter"],p["gbest"], ">", "GWO")
p = pickle.load(open("results/merge/mary_ode_alpha_0.9_JAYA/results.pkl","rb"))
Plot(p["giter"],p["gbest"], "*", "Jaya")

plt.legend(loc="upper right")
plt.tight_layout(pad=0, w_pad=0, h_pad=0)
plt.savefig("merge_0.9_plot.png", dpi=300)
plt.show()
plt.close()

