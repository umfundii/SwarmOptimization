#
#  file:  RandomInertia.py
#
#  Random inertia class for canonical PSO.
#
#  RTK, 09-Dec-2019
#  Last update:  09-Dec-2019
#
################################################################

import random

################################################################
#  RandomInertia
#
class RandomInertia:
    """Use a random inertia value"""

    #-----------------------------------------------------------
    #  __init___
    #
    def __init__(self):
        """Constructor"""
        pass

    #-----------------------------------------------------------
    #  CalculateW
    #
    def CalculateW(self, w0, iterations, max_iter):
        """Return a weight value in the range [0.5,1)"""
        
        return 0.5 + random.random()/2.0


#  end RandomInertia.py


