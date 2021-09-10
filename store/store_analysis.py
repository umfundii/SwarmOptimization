#
#  file:  store_analysis.py
#
#  Interpret the store simulation results
#
#  RTK, 07-Jan-2020
#  Last update:  20-Sep-2020
#
################################################################

import os
import sys
import numpy as np
import matplotlib.pylab as plt
from matplotlib.ticker import MaxNLocator

def GetResults(fname):
    """Parse an output file"""

    lines = [i[:-1] for i in open(fname)]
    revenue = float(lines[1].split()[3][1:])
    lower_prob = float(lines[-3].split()[-1])
    lower_value= float(lines[-2].split()[-1])
    upper_prob = float(lines[-5].split()[-1])
    upper_value= float(lines[-4].split()[-1])
    milk_rank = float(lines[-8].split()[-1])
    candy_rank = float(lines[-7].split()[-1])
    return lower_prob, lower_value, upper_prob, upper_value, milk_rank, candy_rank, revenue


def PlotRanking(s,title):
    """Plot milk and candy ranking"""

    t = np.zeros(len(s))
    for i in range(len(s)):
        t[i] = s[i][4]
    milk = t.copy()
    plt.plot(range(len(t)),t, color='r', marker='o', label='Milk')
    for i in range(len(s)):
        t[i] = s[i][5]
    candy = t.copy()
    plt.plot(range(len(t)),t, color='b', marker='s', label='Candy')
    plt.xticks(np.arange(0, 20, 1.0))
    plt.xlabel('Run')
    plt.ylabel('Ranking')
    plt.title(title)
    plt.tight_layout(pad=0, w_pad=0, h_pad=0)
    plt.savefig("exp_%s_ranking.png" % title, dpi=300)
    plt.show()
    return [milk, candy]


def PlotRevenue(pso,de,ro,gwo,jaya,ga):
    """Plot the daily revenue"""
    
    def revenue(s):
        t = np.zeros(len(s))
        for i in range(len(s)):
            t[i] = s[i][-1]
        return t

    ax0 = plt.subplot(611)
    plt.plot(revenue(pso), marker='.')
    plt.ylabel("PSO")
    plt.setp(ax0.get_xticklabels(), visible=False)
    ax1 = plt.subplot(612, sharex=ax0)
    plt.plot(revenue(de), marker='.')
    plt.ylabel("DE")
    plt.setp(ax1.get_xticklabels(), visible=False)
    ax2 = plt.subplot(613, sharex=ax0)
    plt.plot(revenue(ga), marker='.')
    plt.ylabel("GA")
    plt.setp(ax2.get_xticklabels(), visible=False)
    ax3 = plt.subplot(614, sharex=ax0)
    plt.plot(revenue(gwo), marker='.')
    plt.ylabel("GWO")
    plt.setp(ax3.get_xticklabels(), visible=False)
    ax4 = plt.subplot(615, sharex=ax0)
    plt.plot(revenue(jaya), marker='.')
    plt.ylabel("Jaya")
    plt.setp(ax4.get_xticklabels(), visible=False)
    ax5 = plt.subplot(616, sharex=ax0)
    plt.plot(revenue(ro), marker='.')
    plt.xticks(np.arange(0, 20, 1.0))
    plt.ylabel("RO")
    plt.xlabel("Run")
    plt.tight_layout(pad=0, w_pad=0, h_pad=0)
    plt.savefig("exp_revenue.png", dpi=300)
    plt.show()
    
    return [
        np.array(revenue(pso)), np.array(revenue(de)),   np.array(revenue(ro)),
        np.array(revenue(gwo)), np.array(revenue(jaya)), np.array(revenue(ga))
    ]


def main():
    """Make the plots"""

    N = len(os.listdir("pso_results"))

    pso = []
    for i in range(N):
        pso.append(GetResults("pso_results/pso_run%d" % i))
    de = []
    for i in range(N):
        de.append(GetResults("de_results/de_run%d" % i))
    ro = []
    for i in range(N):
        ro.append(GetResults("ro_results/ro_run%d" % i))
    gwo = []
    for i in range(N):
        gwo.append(GetResults("gwo_results/gwo_run%d" % i))
    jaya = []
    for i in range(N):
        jaya.append(GetResults("jaya_results/jaya_run%d" % i))
    ga = []
    for i in range(N):
        ga.append(GetResults("ga_results/ga_run%d" % i))

    #  Plot milk and candy rankings
    m0,c0 = PlotRanking(pso, "PSO")
    m1,c1 = PlotRanking(de, "DE")
    m2,c2 = PlotRanking(ro, "RO")
    m3,c3 = PlotRanking(gwo, "GWO")
    m4,c4 = PlotRanking(jaya, "Jaya")
    m5,c5 = PlotRanking(ga, "GA")

    #  Milk and candy stats
    n = np.sqrt(len(m0))
    print()
    print("PSO :  milk: %0.2f +/- %0.2f (%0.0f, %0.0f),  candy: %0.2f +/- %0.2f (%0.0f, %0.0f)" % \
            (m0.mean(),m0.std(ddof=1)/n,m0.max(),m0.min(),c0.mean(),c0.std(ddof=1)/n,c0.max(),c0.min()))
    print("DE  :  milk: %0.2f +/- %0.2f (%0.0f, %0.0f),  candy: %0.2f +/- %0.2f (%0.0f, %0.0f)" % \
            (m1.mean(),m1.std(ddof=1)/n,m1.max(),m1.min(),c1.mean(),c1.std(ddof=1)/n,c1.max(),c1.min()))
    print("RO  :  milk: %0.2f +/- %0.2f (%0.0f, %0.0f),  candy: %0.2f +/- %0.2f (%0.0f, %0.0f)" % \
            (m2.mean(),m2.std(ddof=1)/n,m2.max(),m2.min(),c2.mean(),c2.std(ddof=1)/n,c2.max(),c2.min()))
    print("GWO :  milk: %0.2f +/- %0.2f (%0.0f, %0.0f),  candy: %0.2f +/- %0.2f (%0.0f, %0.0f)" % \
            (m3.mean(),m3.std(ddof=1)/n,m3.max(),m3.min(),c3.mean(),c3.std(ddof=1)/n,c3.max(),c3.min()))
    print("Jaya:  milk: %0.2f +/- %0.2f (%0.0f, %0.0f),  candy: %0.2f +/- %0.2f (%0.0f, %0.0f)" % \
            (m4.mean(),m4.std(ddof=1)/n,m4.max(),m4.min(),c4.mean(),c4.std(ddof=1)/n,c4.max(),c4.min()))
    print("GA  :  milk: %0.2f +/- %0.2f (%0.0f, %0.0f),  candy: %0.2f +/- %0.2f (%0.0f, %0.0f)" % \
            (m5.mean(),m5.std(ddof=1)/n,m5.max(),m5.min(),c5.mean(),c5.std(ddof=1)/n,c5.max(),c5.min()))

    #  Plot revenue
    rev = PlotRevenue(pso,de,ro,gwo,jaya,ga)

    #  Revenue stats
    print()
    print("PSO : $%0.2f +/- %0.2f" % (rev[0].mean(), rev[0].std(ddof=1)/n))
    print("DE  : $%0.2f +/- %0.2f" % (rev[1].mean(), rev[1].std(ddof=1)/n))
    print("RO  : $%0.2f +/- %0.2f" % (rev[2].mean(), rev[2].std(ddof=1)/n))
    print("GWO : $%0.2f +/- %0.2f" % (rev[3].mean(), rev[3].std(ddof=1)/n))
    print("Jaya: $%0.2f +/- %0.2f" % (rev[4].mean(), rev[4].std(ddof=1)/n))
    print("GA  : $%0.2f +/- %0.2f" % (rev[5].mean(), rev[5].std(ddof=1)/n))
    print()


if (__name__ == "__main__"):
    main()

