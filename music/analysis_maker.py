#
#  file:  analysis_maker.py
#
#  Plots for melody maker results
#
#  RTK, 27-Oct-2020
#  Last update:  31-Oct-2020
#
################################################################

import numpy as np
import matplotlib.pylab as plt
import pickle

def Plot(giter, gbest, sym, lbl):
    d = np.zeros(800000)
    for i in range(len(giter)):
        d[giter[i]:] = gbest[i]
    plt.plot(range(800000)[::64000], d[::64000], marker=sym, linestyle='none', color='k', label=lbl)
    plt.plot(range(800000), d, linewidth=1, color='k')

#  ionian
p = pickle.load(open("results/maker/run_800000/DE/ionian/melody_DE.pkl","rb"))
Plot(p["giter"],p["gbest"], "o", "DE")
p = pickle.load(open("results/maker/run_800000/RO/ionian/melody_RO.pkl","rb"))
Plot(p["giter"],p["gbest"], "s", "RO")
p = pickle.load(open("results/maker/run_800000/GA/ionian/melody_GA.pkl","rb"))
Plot(p["giter"],p["gbest"], "X", "GA")
p = pickle.load(open("results/maker/run_800000/PSO/ionian/melody_PSO.pkl","rb"))
Plot(p["giter"],p["gbest"], "<", "PSO")
p = pickle.load(open("results/maker/run_800000/GWO/ionian/melody_GWO.pkl","rb"))
Plot(p["giter"],p["gbest"], ">", "GWO")
p = pickle.load(open("results/maker/run_800000/JAYA/ionian/melody_JAYA.pkl","rb"))
Plot(p["giter"],p["gbest"], "*", "Jaya")

plt.legend(loc="upper right")
plt.tight_layout(pad=0, w_pad=0, h_pad=0)
plt.savefig("maker_ionian_plot.png", dpi=300)
#plt.show()
plt.close()

#  aeolian
p = pickle.load(open("results/maker/run_800000/DE/aeolian/melody_DE.pkl","rb"))
Plot(p["giter"],p["gbest"], "o", "DE")
p = pickle.load(open("results/maker/run_800000/RO/aeolian/melody_RO.pkl","rb"))
Plot(p["giter"],p["gbest"], "s", "RO")
p = pickle.load(open("results/maker/run_800000/GA/aeolian/melody_GA.pkl","rb"))
Plot(p["giter"],p["gbest"], "X", "GA")
p = pickle.load(open("results/maker/run_800000/PSO/aeolian/melody_PSO.pkl","rb"))
Plot(p["giter"],p["gbest"], "<", "PSO")
p = pickle.load(open("results/maker/run_800000/GWO/aeolian/melody_GWO.pkl","rb"))
Plot(p["giter"],p["gbest"], ">", "GWO")
p = pickle.load(open("results/maker/run_800000/JAYA/aeolian/melody_JAYA.pkl","rb"))
Plot(p["giter"],p["gbest"], "*", "Jaya")

plt.legend(loc="upper right")
plt.tight_layout(pad=0, w_pad=0, h_pad=0)
plt.savefig("maker_aeolian_plot.png", dpi=300)
#plt.show()
plt.close()

#  Swarm diversity
print("Swarm diversity:")
for alg in ["DE","PSO","GA","JAYA","GWO","RO"]:
    smode = 0.0
    for mode in ["ionian","aeolian","dorian","lydian","mixolydian","phrygian","locrian"]:
        p = pickle.load(open("results/maker/run_800000/%s/%s/melody_%s.pkl" % (alg,mode,alg),"rb"))
        s = p["pos"].std(ddof=1,axis=0)
        smode += s.mean()
        print("    %4s, %10s: %0.8f" % (alg, mode, s.mean()))
    print("    mean: %0.8f" % (smode/7,))
    print()
print()

#  Plot diversity across particle elements
ax0 = plt.subplot(611)
p = pickle.load(open("results/maker/run_800000/RO/ionian/melody_RO.pkl","rb"))
s = p["pos"].std(ddof=1,axis=0) / (p["pos"].mean(axis=0)+1e-9)
plt.plot(s, marker="."); plt.ylabel("RO"); plt.setp(ax0.get_xticklabels(), visible=False)
plt.ylim((0,0.7))
ax1 = plt.subplot(612, sharex=ax0)
p = pickle.load(open("results/maker/run_800000/DE/ionian/melody_DE.pkl","rb"))
s = p["pos"].std(ddof=1,axis=0) / (p["pos"].mean(axis=0)+1e-9)
plt.plot(s, marker="."); plt.ylabel("DE"); plt.setp(ax1.get_xticklabels(), visible=False)
plt.ylim((0,0.7))
ax2 = plt.subplot(613, sharex=ax0)
p = pickle.load(open("results/maker/run_800000/JAYA/ionian/melody_JAYA.pkl","rb"))
s = p["pos"].std(ddof=1,axis=0) / (p["pos"].mean(axis=0)+1e-9)
plt.plot(s, marker="."); plt.ylabel("Jaya"); plt.setp(ax2.get_xticklabels(), visible=False)
plt.ylim((0,0.7))
ax3 = plt.subplot(614, sharex=ax0)
p = pickle.load(open("results/maker/run_800000/GWO/ionian/melody_GWO.pkl","rb"))
s = p["pos"].std(ddof=1,axis=0) / (p["pos"].mean(axis=0)+1e-9)
plt.plot(s, marker="."); plt.ylabel("GWO"); plt.setp(ax3.get_xticklabels(), visible=False)
plt.ylim((0,0.7))
ax4 = plt.subplot(615, sharex=ax0)
p = pickle.load(open("results/maker/run_800000/GA/ionian/melody_GA.pkl","rb"))
s = p["pos"].std(ddof=1,axis=0) / (p["pos"].mean(axis=0)+1e-9)
plt.plot(s, marker="."); plt.ylabel("GA"); plt.setp(ax4.get_xticklabels(), visible=False)
plt.ylim((0,0.7))
ax5 = plt.subplot(616, sharex=ax0)
p = pickle.load(open("results/maker/run_800000/PSO/ionian/melody_PSO.pkl","rb"))
s = p["pos"].std(ddof=1,axis=0) / (p["pos"].mean(axis=0)+1e-9)
plt.plot(s, marker="."); plt.ylabel("PSO");
plt.ylim((0,0.7))
plt.xlabel("Element")
plt.tight_layout(pad=0, w_pad=0, h_pad=0)
plt.savefig("maker_ionian_diversity_plot.png", dpi=300)
plt.show()
plt.close()

