import numpy as np
import pickle

N = 24
ci = np.load("item_counts.npy")
ni = np.load("item_names.npy")
ci = ci[::2]
ni = ni[::2]
ci = ci[:N]
ni = ni[:N]

t = np.random.beta(3.5,1,size=10000000)
h = np.array(np.histogram(t, bins=len(ci))[0])
h = h / h.sum()
pv = 10.0*h + 1

p = [ci,ni,pv]

pickle.dump(p, open("products.pkl","wb"))

