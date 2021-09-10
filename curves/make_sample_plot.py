import numpy as np

np.random.seed(73939133)
x = np.linspace(1,3,10)
y = 1.5*x**2 - 3*x + 4.4
y = y + 0.5*(np.random.random(len(y))-0.5)*y

with open("sample.txt","w") as f:
    f.write("p[0]*x**2 + p[1]*x + p[2]\n")
    for i in range(len(x)):
        f.write("%0.16f  %0.16f\n" % (y[i],x[i]))

