#
#  file:  RandomInitialize.py
#
#  Initialize a swarm uniformly within the bounds.
#
#  RTK, 07-Dec-2019
#  Last update:  09-Dec-2019
#
################################################################

import numpy as np

################################################################
#  RandomInitializer
#
class RandomInitializer:
    """Initialize a swarm uniformly"""

    #-----------------------------------------------------------
    #  __init__
    #
    def __init__(self, npart=10, ndim=3, bounds=None):
        """Constructor"""

        self.npart = npart
        self.ndim = ndim
        self.bounds = bounds


    #-----------------------------------------------------------
    #  InitializeSwarm
    #
    def InitializeSwarm(self):
        """Return a randomly initialized swarm"""

        if (self.bounds == None):
            #  No bounds given, just use [0,1)
            self.swarm = np.random.random((self.npart, self.ndim))
        else:
            #  Bounds given, use them
            self.swarm = np.zeros((self.npart, self.ndim))
            lo = self.bounds.Lower()
            hi = self.bounds.Upper()

            for i in range(self.npart):
                for j in range(self.ndim):
                    self.swarm[i,j] = lo[j] + (hi[j]-lo[j])*np.random.random()        
            self.swarm = self.bounds.Limits(self.swarm)

        return self.swarm


# end RandomInitializer.py

