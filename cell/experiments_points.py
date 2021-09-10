#
#  file:  experiments_points.py
#
#  Run experiments with placing points on the unit square.
#
#  RTK, 13-Oct-2020
#  Last update: 13-Oct-2020
#
################################################################

import os

#os.system("rm -rf results_points; mkdir results_points")

n = 0
for alg in ["RO","DE","PSO","JAYA","GWO","GA"]:
    for pnts in [2,3,4,5,6,7,8,9]:
        for r in range(8):
            miter = pnts*6000
            cmd = "python3 points.py %d 25 %d %s RI results_points/%s_%d_run%d" % (pnts,miter,alg,alg.lower(),pnts,r)
            os.system(cmd)
            n += 1

print()
print("%d experiments complete" % n)
print()

