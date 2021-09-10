#
#  file:  rank_results.py
#
#  Rank a set of NN training results.
#
#  RTK, 20-Aug-2020
#  Last update:  20-Aug-2020
#
################################################################

import numpy as np
import sys

def GetRanking(fname):
    """Get the ranking for this run"""

    lines = [i[:-1] for i in open(fname)]
    lines = lines[3:]
    ranks = []
    for line in lines:
        try:
            ranks.append(line.split()[-1])
        except:
            pass
    return ranks


ranks = {
    "MLP": [],
    "RO": [],
    "PSO": [],
    "DE": [],
    "GWO": [],
    "JAYA": [],
    "GA": [],
}

for i in range(1, len(sys.argv)):
    order = GetRanking(sys.argv[i])
    for i,label in enumerate(order):
        ranks[label].append(i)

print()
for k in ["MLP","RO","PSO","DE","GWO","JAYA","GA"]:
    r = np.array(ranks[k])
    print("%4s: %0.3f +/- %0.3f, " % (k, r.mean(), r.std(ddof=1)), r.astype("uint16"))
print()

