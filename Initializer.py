#
#  file:  Initializer.py
#
#  Base class for a swarm initializer.
#
#  RTK, 07-Dec-2019
#  Last update:  07-Dec-2019
#
################################################################

################################################################
#  Initializer
#
class Initializer:
    """Abstract base class for a swarm initializer"""

    #-----------------------------------------------------------
    #  __init__
    #
    #  Override with your own initializer.  It will be passed
    #  the number of particles, the dimension, and the bounds object.
    #
    def __init__(self, npart, ndim, bounds=None):
        """Constructor"""

        pass


    #-----------------------------------------------------------
    #  InitializeSwarm
    #
    def InitializeSwarm(self):
        """Return a randomly initialized swarm"""

        pass


# end Initializer.py

