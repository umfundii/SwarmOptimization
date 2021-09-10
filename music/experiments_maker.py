#
#  file: experiments_maker.py
#
#  Run a series of experiments in melody generation
#
#  RTK, 20-Oct-2020
#  Last update:  30-Oct-2020
#
################################################################

import os
import time

st = time.time()

#os.system("mkdir results")
#os.system("mkdir results/maker")
#os.system("mkdir results/maker/RO")
#os.system("mkdir results/maker/DE")
#os.system("mkdir results/maker/PSO")
#os.system("mkdir results/maker/GWO")
#os.system("mkdir results/maker/JAYA")
#os.system("mkdir results/maker/GA")

n = 0
for alg in ["RO","DE","PSO","GWO","JAYA","GA"]:
    for mode in ["ionian","dorian","phrygian","lydian","mixolydian","aeolian","locrian"]:
        cmd = "python3 melody_maker.py 20 results/maker/%s/%s 20 800000 %s RI %s" % (alg,mode,alg,mode)
        #os.system(cmd)
        print(cmd)
        n += 2

print()
print("%d melodies generated (time = %0.3f seconds)" % (n, time.time()-st))
print()

