import numpy as np
import matplotlib.pylab as plt

d = np.load("de_rand_bin_frames/dispersion.npy")
plt.plot(np.arange(101),d,color='k')
plt.plot(np.arange(101)[::4], d[::4], color='k', marker='o', linestyle='none', label='DE/rand/1/bin')

d = np.load("de_rand_ga_frames/dispersion.npy")
plt.plot(np.arange(101),d,color='k')
plt.plot(np.arange(101)[::4], d[::4], color='k', marker='s', linestyle='none', label='DE/rand/1/GA')

d = np.load("de_best_bin_frames/dispersion.npy")
plt.plot(np.arange(101),d,color='k')
plt.plot(np.arange(101)[::4], d[::4], color='k', marker='*', linestyle='none', label='DE/best/1/bin')

d = np.load("de_best_ga_frames/dispersion.npy")
plt.plot(np.arange(101),d,color='k')
plt.plot(np.arange(101)[::4], d[::4], color='k', marker='<', linestyle='none', label='DE/best/1/GA')

d = np.load("de_toggle_bin_frames/dispersion.npy")
plt.plot(np.arange(101),d,color='k')
plt.plot(np.arange(101)[::4], d[::4], color='k', marker='>', linestyle='none', label='DE/toggle/1/bin')

plt.xlim((0,60))
plt.legend(loc="upper right")
plt.xlabel('Iteration')
plt.ylabel('Dispersion')
plt.tight_layout(pad=0,w_pad=0,h_pad=0)
plt.savefig("de_dispersion_plot.png", dpi=300)
plt.show()

