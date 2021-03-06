#
#  file: fxy_gaussian_ga_20_1000_ri_results.py
#
#  RTK, 14-Jun-2020
#  Last update:  19-Jun-2020
#
################################################################

import numpy as np

d = np.array([
    [2.18270601, -4.30299190, -1.9992300643, 14],
    [-2.19873230, 4.24876127, -4.9836080905, 14],
    [-2.20652287, 4.28649977, -4.9985951725, 6],
    [-2.21984076, 4.30195327, -4.9975164225, 7],
    [-2.18407295, 4.28462797, -4.9969386230, 9],
    [-2.23161415, 4.27247209, -4.9890292991, 16],
    [-2.24172220, 4.29390141, -4.9889002469, 16],
    [-2.19517295, 4.30631994, -4.9996047529, 10],
    [-2.21679020, 4.33249256, -4.9916465006, 8],
    [-2.19118248, 4.28716000, -4.9984838905, 21],
    [2.16398094, -4.30570645, -1.9966779209, 12],
    [-2.23091570, 4.26224648, -4.9851401943, 15],
    [-2.21503156, 4.29804444, -4.9985641314, 17],
    [2.19664778, -4.30397263, -1.9999324531, 8],
    [2.20130350, -4.32621316, -1.9982786694, 11],
    [-2.21898917, 4.30340288, -4.9976744895, 11],
    [-2.20658345, 4.26710961, -4.9929729449, 12],
    [-2.20058131, 4.30820865, -4.9995767692, 8],
    [2.22571400, -4.30825198, -1.9981775689, 8],
    [-2.21580456, 4.31146192, -4.9976183189, 6],
    [-2.19892593, 4.30825610, -4.9995667885, 6],
])

s = d[[1,2,3,4,5,6,7,8,9,11,12,15,16,17,19,20],:]
w = d[[0,10,13,14,18],:]
f = []

print()
print("21 searches, fxy_gaussian, GA, 20 particles, 1000 iterations, RI")
print("%d successes, %d wrong, %d failures" % (len(s),len(w),len(f)))
print()
print("Successes, objective    = %0.5f +/- %0.5f" % (s[:,2].mean(), s[:,2].std()/np.sqrt(s.shape[0])))
print("Successes, best updates = %0.5f +/- %0.5f" % (s[:,-1].mean(), s[:,-1].std()/np.sqrt(s.shape[0])))
print()


