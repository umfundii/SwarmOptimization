import numpy as np
import pickle
import matplotlib.pylab as plt

d = pickle.load(open("de_50_40_16000_results.pkl","rb"))
r = pickle.load(open("ro_50_40_16000_results.pkl","rb"))
#g = pickle.load(open("ga_50_40_16000_results.pkl","rb"))
p = np.array(pickle.load(open("products.pkl","rb"))[-1])
w = np.array(pickle.load(open("products.pkl","rb"))[0])
w = w / w.sum()

de   = p[np.argsort(d["gpos"][-1])]
wde  = w[np.argsort(d["gpos"][-1])]
ro   = p[np.argsort(r["gpos"][-1])]
wro  = w[np.argsort(r["gpos"][-1])]
#ga   = p[np.argsort(g["gpos"][-1])]
#wga  = w[np.argsort(g["gpos"][-1])]

plt.plot(de, marker='P', linestyle='none', color='k', label='DE')
plt.plot(ro, marker='o', linestyle='none', color='k', label='RO')
#plt.plot(ga, marker='>', linestyle='none', color='k', label='GA')
plt.plot(de, linestyle='solid', color='k')
plt.plot(ro, linestyle='dotted', color='k')
#plt.plot(ga, linestyle='dashed', color='k')
plt.xlabel("Product order")
plt.ylabel("Cost")
plt.legend(loc="upper right")
plt.tight_layout(pad=0, w_pad=0, h_pad=0)
plt.savefig("store_de_ro_prices.png", dpi=300)
plt.show()
plt.close()

plt.plot(wde*de, marker='P', linestyle='none', color='k', label='DE')
plt.plot(wro*ro, marker='o', linestyle='none', color='k', label='RO')
#plt.plot(wga*ga, marker='>', linestyle='none', color='k', label='GA')
plt.plot(wde*de, linestyle='solid', color='k')
plt.plot(wro*ro, linestyle='dotted', color='k')
#plt.plot(wga*ga, linestyle='dashed', color='k')
plt.xlabel("Product order")
plt.ylabel("Cost * Probability")
plt.legend(loc="upper left")
plt.tight_layout(pad=0, w_pad=0, h_pad=0)
plt.savefig("store_de_ro_prob.png", dpi=300)
plt.show()
