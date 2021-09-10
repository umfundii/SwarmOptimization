import numpy as np
import os
import matplotlib.pylab as plt

def get_score(fname):
    lines = [i[:-1] for i in open(fname)]
    s = lines[-3].split()
    return -float(s[2])

barbara = [get_score("results/barbara_DE/README.txt")]
barbara.append(get_score("results/barbara_GA/README.txt"))
barbara.append(get_score("results/barbara_GWO/README.txt"))
barbara.append(get_score("results/barbara_JAYA/README.txt"))
barbara.append(get_score("results/barbara_PSO/README.txt"))
barbara.append(get_score("results/barbara_RO/README.txt"))

boat = [get_score("results/boat_DE/README.txt")]
boat.append(get_score("results/boat_GA/README.txt"))
boat.append(get_score("results/boat_GWO/README.txt"))
boat.append(get_score("results/boat_JAYA/README.txt"))
boat.append(get_score("results/boat_PSO/README.txt"))
boat.append(get_score("results/boat_RO/README.txt"))

cameraman = [get_score("results/cameraman_DE/README.txt")]
cameraman.append(get_score("results/cameraman_GA/README.txt"))
cameraman.append(get_score("results/cameraman_GWO/README.txt"))
cameraman.append(get_score("results/cameraman_JAYA/README.txt"))
cameraman.append(get_score("results/cameraman_PSO/README.txt"))
cameraman.append(get_score("results/cameraman_RO/README.txt"))

fruits = [get_score("results/fruits_DE/README.txt")]
fruits.append(get_score("results/fruits_GA/README.txt"))
fruits.append(get_score("results/fruits_GWO/README.txt"))
fruits.append(get_score("results/fruits_JAYA/README.txt"))
fruits.append(get_score("results/fruits_PSO/README.txt"))
fruits.append(get_score("results/fruits_RO/README.txt"))

goldhill = [get_score("results/goldhill_DE/README.txt")]
goldhill.append(get_score("results/goldhill_GA/README.txt"))
goldhill.append(get_score("results/goldhill_GWO/README.txt"))
goldhill.append(get_score("results/goldhill_JAYA/README.txt"))
goldhill.append(get_score("results/goldhill_PSO/README.txt"))
goldhill.append(get_score("results/goldhill_RO/README.txt"))

lena = [get_score("results/lena_DE/README.txt")]
lena.append(get_score("results/lena_GA/README.txt"))
lena.append(get_score("results/lena_GWO/README.txt"))
lena.append(get_score("results/lena_JAYA/README.txt"))
lena.append(get_score("results/lena_PSO/README.txt"))
lena.append(get_score("results/lena_RO/README.txt"))

peppers = [get_score("results/peppers_DE/README.txt")]
peppers.append(get_score("results/peppers_GA/README.txt"))
peppers.append(get_score("results/peppers_GWO/README.txt"))
peppers.append(get_score("results/peppers_JAYA/README.txt"))
peppers.append(get_score("results/peppers_PSO/README.txt"))
peppers.append(get_score("results/peppers_RO/README.txt"))

zelda = [get_score("results/zelda_DE/README.txt")]
zelda.append(get_score("results/zelda_GA/README.txt"))
zelda.append(get_score("results/zelda_GWO/README.txt"))
zelda.append(get_score("results/zelda_JAYA/README.txt"))
zelda.append(get_score("results/zelda_PSO/README.txt"))
zelda.append(get_score("results/zelda_RO/README.txt"))

fig, ax = plt.subplots()
plt.plot(range(6), barbara, marker='o', color='k',linestyle='none', label='barbara')
plt.plot(range(6), boat, marker='s', color='k',linestyle='none', label='boat')
plt.plot(range(6), cameraman, marker='*', color='k',linestyle='none', label='cameraman')
plt.plot(range(6), goldhill, marker='X', color='k',linestyle='none', label='goldhill')
plt.plot(range(6), lena, marker='<', color='k',linestyle='none', label='lena')
plt.plot(range(6), fruits, marker='>', color='k',linestyle='none', label='fruits')
plt.plot(range(6), peppers, marker='P', color='k',linestyle='none', label='peppers')
plt.plot(range(6), zelda, marker='^', color='k',linestyle='none', label='zelda')
plt.ylabel("$F$")
plt.xlim((-0.5,7))
plt.legend(loc="upper right")
ax.set_xticklabels([" ", "DE","GA","GWO","Jaya","PSO","RO"])
plt.tight_layout(pad=0, w_pad=0, h_pad=0)
plt.savefig("scores.png", dpi=300)
plt.show()

