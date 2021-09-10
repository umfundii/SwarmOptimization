#
#  file:  QuasirandomInitializer.py
#
#  Initialize a swarm quasirandomly over the given bounds.
#
#  RTK, 07-Dec-2019
#  Last update:  12-Dec-2019
#
################################################################

import numpy as np
from math import floor

################################################################
#  QuasirandomInitializer
#
class QuasirandomInitializer:
    """Initialize a swarm quasirandomly"""

    #-----------------------------------------------------------
    #  Halton
    #
    def Halton(self, i,b):
        """Return i-th Halton number for the given base"""

        f = 1.0
        r = 0
        while (i > 0):
            f = f/b
            r = r + f*(i % b)
            i = floor(i/float(b))
        return r


    #-----------------------------------------------------------
    #  __init__
    #
    def __init__(self, npart=10, ndim=3, bounds=None, k=1, jitter=0.0):
        """Constructor"""

        self.npart = npart
        self.ndim = ndim
        self.bounds = bounds
        self.k = k
        self.jitter = jitter

        self.primes = [
             2,  3,  5,  7, 11, 13, 17, 19, 23, 29,
            31, 37, 41, 43, 47, 53, 59, 61, 67, 71,
            73, 79, 83, 89, 97,101,103,107,109,113,
           127,131,137,139,149,151,157,163,167,173,
           179,181,191,193,197,199,211,223,227,229,
           233,239,241,251,257,263,269,271,277,281,
           283,293,307,311,313,317,331,337,347,349,
           353,359,367,373,379,383,389,397,401,409,
           419,421,431,433,439,443,449,457,461,463,
           467,479,487,491,499,503,509,521,523,541,
           547,557,563,569,571,577,587,593,599,601,
           607,613,617,619,631,641,643,647,653,659]


    #-----------------------------------------------------------
    #  InitializeSwarm
    #
    def InitializeSwarm(self):
        """Return a quasirandomly initialized swarm"""

        self.swarm = np.zeros((self.npart, self.ndim))

        if (self.bounds == None):
            #  No bounds given, just use [0,1)
            lo = np.zeros(self.ndim)
            hi = np.ones(self.ndim)
        else:
            #  Bounds given, use them
            lo = self.bounds.Lower()
            hi = self.bounds.Upper()

        #  Initialize quasirandomly
        for i in range(self.npart):
            for j in range(self.ndim):
                h = self.Halton(i+self.k,self.primes[j % len(self.primes)])
                q = self.jitter*(np.random.random()-0.5)
                self.swarm[i,j] = lo[j] + (hi[j]-lo[j]) * h + q

        if (self.bounds != None):
            self.swarm = self.bounds.Limits(self.swarm)

        return self.swarm


# end QuasirandomInitializer.py

