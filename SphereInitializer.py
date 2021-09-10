#
#  file:  SphereInitializer.py
#
#  Initialize a swarm over a hypersphere within the bounds.
#
#  RTK, 12-Dec-2019
#  Last update:  19-May-2020
#
################################################################

import numpy as np
from math import floor

################################################################
#  SphereInitializer
#
class SphereInitializer:
    """Initialize a swarm on a hypersphere"""

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

        radius = 0.5
        for i in range(self.npart):
            p = np.random.normal(size=self.ndim)
            self.swarm[i] = radius + radius* p / np.sqrt(np.dot(p,p))
        self.swarm = np.abs(hi-lo)*self.swarm + lo

        if (self.bounds != None):
            self.swarm = self.bounds.Limits(self.swarm)

        return self.swarm


# end SphereInitializer.py

