#
#  file:  store_eta_analysis.py
#
#  Interpret the store RO simulation results
#
#  RTK, 07-Jan-2020
#  Last update:  26-Sep-2020
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


def main():
    """summaries RO eta results"""

    eta = [0.01,0.03,0.05,0.1,0.13,0.15,0.2,0.25,0.3,0.4,0.5,0.6,0.7,0.8,1,1.5,2]
    milk = np.zeros((6,len(eta)))
    candy = np.zeros((6,len(eta)))
    revenue = np.zeros((6,len(eta)))

    for k,e in enumerate(eta):
        for i in range(6):
            _,_,_,_,m,c,r = GetResults("ro_eta_run%d/ro_eta_%0.2f.txt" % (i,e))
            milk[i,k] = m
            candy[i,k] = c
            revenue[i,k] = r
    mmilk, smilk = milk.mean(axis=0), milk.std(axis=0, ddof=1)/np.sqrt(6)
    mcandy, scandy = candy.mean(axis=0), candy.std(axis=0, ddof=1)/np.sqrt(6)
    mrevenue, srevenue = revenue.mean(axis=0), revenue.std(axis=0, ddof=1)/np.sqrt(6)

    print()
    for k,e in enumerate(eta):
        print("eta = %0.2f:" % e)
        print("    milk   :  %0.4f +/- %0.4f" % (mmilk[k],smilk[k]))
        print("    candy  :  %0.4f +/- %0.4f" % (mcandy[k],scandy[k]))
        print("    revenue:  %0.4f +/- %0.4f" % (mrevenue[k],srevenue[k]))
        print()
    
    plt.plot(eta,mmilk,marker="s", color='b')
    plt.plot(eta,mcandy,marker='o',color='r')
    plt.xlabel("$\eta$")
    plt.ylabel("Mean rank")
    plt.tight_layout(pad=0,w_pad=0,h_pad=0)
    plt.savefig("ro_eta_ranks.png", dpi=300)
    plt.show()
    plt.close()

    plt.plot(eta,mrevenue,marker='X',color='k')
    plt.xlabel("$\eta$")
    plt.ylabel("Mean revenue")
    plt.tight_layout(pad=0,w_pad=0,h_pad=0)
    plt.savefig("ro_eta_revenue.png", dpi=300)
    plt.show()
    plt.close()




if (__name__ == "__main__"):
    main()

