"""
Contains the RegisterError class.
"""








class RegisterError(Exception):
    """
    This is the register error exception. This represents an error in
    registering a new crawler or mirror implementation.
    """


    #######################
    # PUBLIC - Initialize #
    #######################


    def __init__(
        self
        ,*args
        ):
        """
        Initialize a new register error exception.

        Parameters
        ----------
        *args : tuple
                Detailed description.
        """
        Exception.__init__(*args)
