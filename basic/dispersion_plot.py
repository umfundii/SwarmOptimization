#
#  file:  dispersion_plot.npy
#
#  Plot the swarm dispersion as function of iteration
#
#  RTK, 26-May-2020
#  Last update:  26-May-2020
#
################################################################

import numpy as np
import matplotlib.pylab as plt

# resample
ro   = np.load("ro_resample/dispersion.npy")
pso  = np.load("pso_resample/dispersion.npy")
jaya = np.load("jaya_resample/dispersion.npy")
gwo2 = np.load("gwo2_resample/dispersion.npy")
gwo4 = np.load("gwo4_resample/dispersion.npy")

x = np.arange(101)
plt.plot(x,ro, color='r')
plt.plot(x,pso, color='g')
plt.plot(x,jaya, color='b')
plt.plot(x,gwo2, color='m')
plt.plot(x,gwo4, color='k')

x = np.arange(101)[::5]
plt.plot(x,ro[::5],   marker='o', linestyle='none', color='r', label='RO')
plt.plot(x,pso[::5],  marker='s', linestyle='none', color='g', label='PSO')
plt.plot(x,jaya[::5], marker='*', linestyle='none', color='b', label='Jaya')
plt.plot(x,gwo2[::5], marker='^', linestyle='none', color='m', label='GWO ($\eta=2$)')
plt.plot(x,gwo4[::5], marker='<', linestyle='none', color='k', label='GWO ($\eta=4$)')
plt.ylim((0,13))
plt.legend(loc="upper right")
plt.ylabel("Dispersion")
plt.xlabel("Iteration")
plt.tight_layout(pad=0, w_pad=0, h_pad=0)
plt.savefig("dispersion_resample_plot.png", dpi=300)
plt.show()
plt.close()

# clip
ro   = np.load("ro_clip/dispersion.npy")
pso  = np.load("pso_clip/dispersion.npy")
jaya = np.load("jaya_clip/dispersion.npy")
gwo2 = np.load("gwo2_clip/dispersion.npy")
gwo4 = np.load("gwo4_clip/dispersion.npy")

x = np.arange(101)
plt.plot(x,ro, color='r')
plt.plot(x,pso, color='g')
plt.plot(x,jaya, color='b')
plt.plot(x,gwo2, color='m')
plt.plot(x,gwo4, color='k')

x = np.arange(101)[::5]
plt.plot(x,ro[::5],   marker='o', linestyle='none', color='r', label='RO')
plt.plot(x,pso[::5],  marker='s', linestyle='none', color='g', label='PSO')
plt.plot(x,jaya[::5], marker='*', linestyle='none', color='b', label='Jaya')
plt.plot(x,gwo2[::5], marker='^', linestyle='none', color='m', label='GWO ($\eta=2$)')
plt.plot(x,gwo4[::5], marker='<', linestyle='none', color='k', label='GWO ($\eta=4$)')
plt.ylim((0,13))
plt.legend(loc="upper right")
plt.ylabel("Dispersion")
plt.xlabel("Iteration")
plt.tight_layout(pad=0, w_pad=0, h_pad=0)
plt.savefig("dispersion_clip_plot.png", dpi=300)
plt.show()

