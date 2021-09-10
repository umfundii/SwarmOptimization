#
#  file: experiments_match.py
#
#  Run a series of experiments in melody generation
#  matching the NMD slip jigs and Bach chorales
#
#  RTK, 22-Oct-2020
#  Last update:  27-Oct-2020
#
################################################################

import os
import time

st = time.time()

n = 0
for alg in ["RO","DE","PSO","GWO","JAYA","GA"]:
    for run in range(5):
        cmd = "python3 melody_match.py 20 results/match/jigs/%s_run%d 25 130000 %s RI NMD" % (alg.lower(),run,alg)
        os.system(cmd)
        n += 1

for alg in ["RO","DE","PSO","GWO","JAYA","GA"]:
    for run in range(5):
        cmd = "python3 melody_match.py 20 results/match/bach/%s_run%d 25 130000 %s RI bach" % (alg.lower(),run,alg)
        os.system(cmd)
        n += 1

print()
print("%d melodies generated (time = %0.3f seconds)" % (n, time.time()-st))
print()

