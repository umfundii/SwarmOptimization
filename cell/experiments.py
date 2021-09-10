#
#  file:  experiments.py
#
#  Run the cell tower placement experiments.
#
#  RTK, 03-Oct-2020
#  Last update: 03-Oct-2020
#
################################################################

import os

os.system("rm -rf results; mkdir results")

n = 0
for alg in ["RO","DE","PSO","JAYA","GWO","GA"]:
    for tower in ["towers","towers1"]:
        for m in range(5):
            for r in range(8):
                cmd = "python3 cell.py maps/map_%02d.png %s 20 300 %s RI results/%s_map_%02d_%s_run%d" %  \
                      (m, tower, alg, alg.lower(), m, tower, r)
                os.system(cmd)
                n += 1
print()
print("%d experiments complete" % n)
print()

