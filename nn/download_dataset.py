#
#  file:  download_dataset.py
#
#  Run once to get the breast cancer dataset locally.
#
#  RTK, 20-Aug-2020
#  Last update:  20-Aug-2020
#
################################################################

import numpy as np
from sklearn.datasets import load_breast_cancer

x,y = load_breast_cancer(True)
x = (x - x.mean(axis=0)) / x.std(axis=0)
i0 = np.where(y == 0)
i1 = np.where(y == 1)
yp = y[i1];  yn = y[i0]
xp = x[i1];  xn = x[i0]
pp = int(0.7*len(yp))
nn = int(0.7*len(yn))
xtrn = np.concatenate((xp[:pp,:], xn[:nn,:]))
ytrn = np.concatenate((yp[:pp], yn[:nn]))
xtst = np.concatenate((xp[pp:,:], xn[nn:,:]))
ytst = np.concatenate((yp[pp:], yn[nn:]))
idx = np.argsort(np.random.random(len(ytrn)))
xtrn = xtrn[idx]
ytrn = ytrn[idx]
idx = np.argsort(np.random.random(len(ytst)))
xtst = xtst[idx]
ytst = ytst[idx]

np.save("nn_xtrn.npy", xtrn)
np.save("nn_ytrn.npy", ytrn)
np.save("nn_xtst.npy", xtst)
np.save("nn_ytst.npy", ytst)

