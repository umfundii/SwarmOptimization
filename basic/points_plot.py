import numpy as np
import matplotlib.pylab as plt

ro  = np.load("points_ro_resample.npy")
pso = np.load("points_pso_resample.npy")
jaya= np.load("points_jaya_resample.npy")
gwo = np.load("points_gwo_resample.npy")
gwo2= np.load("points_gwo_n4_resample.npy")

x = np.arange(100)
plt.plot(x,ro, color='r')
plt.plot(x,pso, color='g')
plt.plot(x,jaya, color='b')
plt.plot(x,gwo, color='m')
plt.plot(x,gwo2, color='k')

x = np.arange(100)[::5]
plt.plot(x,ro[::5], marker='o', linestyle='none',color='r', label='RO')
plt.plot(x,pso[::5], marker='s', linestyle='none',color='g', label='PSO')
plt.plot(x,jaya[::5], marker='*', linestyle='none',color='b', label='Jaya')
plt.plot(x,gwo[::5], marker='^', linestyle='none', color='m', label='GWO ($\eta=2$)')
plt.plot(x,gwo2[::5], marker='<', linestyle='none', color='k', label='GWO ($\eta=4$)')

plt.ylim((-5.1,-0.7))
plt.legend(loc="upper right")
plt.xlabel("Iteration")
plt.ylabel("Objective Function")
plt.tight_layout(pad=0, w_pad=0, h_pad=0)
plt.savefig("points_plot_resample.png", dpi=300)
plt.show()
plt.close()

ro  = np.load("points_ro_clip.npy")
pso = np.load("points_pso_clip.npy")
jaya= np.load("points_jaya_clip.npy")
gwo = np.load("points_gwo_clip.npy")
gwo2= np.load("points_gwo_n4_clip.npy")

x = np.arange(100)
plt.plot(x,ro, color='r')
plt.plot(x,pso, color='g')
plt.plot(x,jaya, color='b')
plt.plot(x,gwo, color='m')
plt.plot(x,gwo2, color='k')

x = np.arange(100)[::5]
plt.plot(x,ro[::5], marker='o', linestyle='none',color='r', label='RO')
plt.plot(x,pso[::5], marker='s', linestyle='none',color='g', label='PSO')
plt.plot(x,jaya[::5], marker='*', linestyle='none',color='b', label='Jaya')
plt.plot(x,gwo[::5], marker='^', linestyle='none', color='m', label='GWO ($\eta=2$)')
plt.plot(x,gwo2[::5], marker='<', linestyle='none', color='k', label='GWO ($\eta=4$)')

plt.ylim((-5.1,-0.7))
plt.legend(loc="upper right")
plt.xlabel("Iteration")
plt.ylabel("Objective Function")
plt.tight_layout(pad=0, w_pad=0, h_pad=0)
plt.savefig("points_plot_clip.png", dpi=300)
plt.show()
plt.close()

