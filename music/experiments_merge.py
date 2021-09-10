#
#  file: experiments_merge.py
#
#  Merge melodies
#
#  RTK, 27-Oct-2020
#  Last update:  27-Oct-2020
#
################################################################
# 
# swarm_melody <template1> <template2> <alpha> <outdir> <npart> <max_iter>
# 
#   <template1>      - first template melody (.npy)
#   <template2>|none - second template melody (.npy)
#   <alpha>          - balance between melodies [0,1]
#   <outdir>         - output directory (overwritten)
#   <npart>          - swarm size (template sets dimensions)
#   <max_iter>       - maximum number of iterations
#   <alg>            - algorithm: PSO,DE,RO,GWO,JAYA,GA
# 

import os
import time

st = time.time()

n = 0
for alg in ["RO","DE","PSO","GWO","JAYA","GA"]:
    for alpha in [0.1,0.3,0.5,0.7,0.9]:
        cmd = "python3 melody_merge.py mary.npy ode.npy %0.1f results/merge/mary_ode_alpha_%0.1f_%s 20 10000 %s" % (alpha, alpha, alg, alg)
        os.system(cmd)
        n += 1

for alg in ["RO","DE","PSO","GWO","JAYA","GA"]:
    for alpha in [0.1,0.3,0.5,0.7,0.9]:
        cmd = "python3 melody_merge.py mary.npy happy.npy %0.1f results/merge/mary_happy_alpha_%0.1f_%s 20 10000 %s" % (alpha, alpha, alg, alg)
        os.system(cmd)
        n += 1

for alg in ["RO","DE","PSO","GWO","JAYA","GA"]:
    for alpha in [0.1,0.3,0.5,0.7,0.9]:
        cmd = "python3 melody_merge.py happy.npy ode.npy %0.1f results/merge/happy_ode_alpha_%0.1f_%s 20 10000 %s" % (alpha, alpha, alg, alg)
        os.system(cmd)
        n += 1
print()
print("%d melodies generated (time = %0.3f seconds)" % (n, time.time()-st))
print()

