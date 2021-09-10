import numpy as np
import sys

if (len(sys.argv) == 1):
    print()
    print("problem_generator <items> <output>")
    print()
    print("  <items>  - number of items")
    print("  <output> - output file name")
    print()
    exit(0)

n = int(sys.argv[1])
w = np.random.randint(10,200, size=n)
v = np.random.randint(10,100, size=n)
m = (w*np.ones(n)).sum() - np.random.randint(0,6)

with open(sys.argv[2], "w") as f:
    f.write("%d %d\n" % (n,m))
    for i in range(n):
        f.write("%d %d\n" % (v[i], w[i]))

