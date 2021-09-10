import numpy as np
import matplotlib.pylab as plt
import pickle

d = pickle.load(open("products.pkl","rb"))
pv = np.array(d[2])
ci = np.array(d[0])
ci = 20*(ci / ci.sum())

plt.plot(range(24),ci,marker='o',label='Likelihood')
plt.plot(range(24),pv,marker="s",label='Cost')
plt.xlabel("Item Number")
plt.ylabel("Cost (\$) or Likelihood (x20)")
plt.legend(loc="upper right")
plt.tight_layout(pad=0,w_pad=0,h_pad=0)
plt.savefig("product_costs.png", dpi=300)
plt.show()
