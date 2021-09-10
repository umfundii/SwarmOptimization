#
#  file:  Done.py
#
#  Base class to use to apply custom notions of "Done".
#
#  RTK, 07-Dec-2019
#  Last update:  07-Dec-2019
#
################################################################

import numpy as np

################################################################
#  Done
#
class Done:
    """Customize 'done' idea"""

    #-----------------------------------------------------------
    #  __init__
    #
    def __init__(self):
        """Constructor"""

        pass


    #-----------------------------------------------------------
    #  Done
    #
    def Done(self, gbest, gpos=None, pos=None, max_iter=None, iteration=None):
        """Return True if done"""

        return False


#  end Done.py

