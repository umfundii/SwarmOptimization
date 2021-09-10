# plot product order distance as function of shopper pool size
import numpy as np
import matplotlib.pylab as plt
import pickle

def dist(b):
    a = np.arange(len(b))[::-1]
    w = np.arange(len(b))
    n = np.argsort(b)
    z = np.abs(w-a).sum()
    return np.abs(a-n).sum() / z

x = []
y = []

for p in [10,25,50,75,100,150,250,500,1000]:
    d = pickle.load(open("shoppers/jaya_%d_30_4000_results.pkl" % p, "rb"))
    x.append(p)
    y.append(dist(d["gpos"][-1]))
    
plt.plot(x,y, marker="o", color='k')
plt.xlabel("Number of shoppers")
plt.ylabel("Distance")
plt.tight_layout(pad=0, w_pad=0, h_pad=0)
plt.savefig("product_order_shoppers.png", dpi=300)
plt.show()

