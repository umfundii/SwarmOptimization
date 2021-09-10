import numpy as np
import matplotlib.pylab as plt
from PIL import Image
from scipy.interpolate import interp2d

d = np.load("rosenbrock_de_results_run3.npy")
x = d[:,0]
y = d[:,1]
z = d[:,2]

func = interp2d(x,y,z, kind="cubic")
xmin, xmax = x.min(), x.max()
ymin, ymax = y.min(), y.max()
X = np.linspace(xmin, xmax, 72)
Y = np.linspace(ymin, ymax, 72)
zimg = np.zeros((len(X),len(Y)))
for i,x in enumerate(X):
    for j,y in enumerate(Y):
        zimg[i,j] = func(x,y)
zimg += np.abs(zimg.min())
zimg = np.log(zimg+1)
zimg /= zimg.max()
img = (255.0*zimg).astype("uint8")
img = Image.fromarray(img).resize((10*len(X),10*len(Y)))
img = np.array(img)
fig, ax = plt.subplots(figsize=(6,6))
ax.imshow(img, cmap='gray', extent=[100,50000, 100,10], aspect='auto')
ax.plot(d[:,1], d[:,0], marker="+", linestyle="none", color="#999999")
plt.xlabel("Iterations")
plt.ylabel("Swarm size")
plt.tight_layout(pad=0, w_pad=0, h_pad=0)
plt.savefig("rosenbrock_de_results_log_run3.png", dpi=300)
plt.show()


