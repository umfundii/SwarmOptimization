import numpy as np
import matplotlib.pylab as plt

r = np.load("shoppers/revenue.npy")
n = np.load("shoppers/nshoppers.npy")

plt.plot(n,r/n, marker="o", color='k')
plt.xlabel("Number of Shoppers")
plt.ylabel("Revenue per shopper")
plt.tight_layout(pad=0,w_pad=0,h_pad=0)
plt.savefig("per_shopper_plot.png", dpi=300)
plt.show()

