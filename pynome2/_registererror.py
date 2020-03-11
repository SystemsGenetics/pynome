"""
Contains the RegisterError class.
"""








class RegisterError(Exception):
    """
    Detailed description.
    """


    ###################
    # PUBLIC - access #
    ###################


    def __init__(self, *args):
        """
        Detailed description.

        Parameters
        ----------
        *args : tuple
                Detailed description.
        """
        Exception.__init__(*args)
