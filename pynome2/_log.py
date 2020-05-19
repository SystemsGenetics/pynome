"""
Contains the Log class.
"""
import time








class Log():
    """
    This is the singleton log class. It is responsible for logging any messages
    given to it from anywhere else in the application, putting a timestamp on
    the output of every message. This is designed to be the central location for
    any standard output.
    """


    #######################
    # PUBLIC - Initialize #
    #######################


    def __init__(
        self
        ):
        """
        Initializes the singleton log instance.
        """
        pass


    ####################
    # PUBLIC - Methods #
    ####################


    def send(
        self
        ,message
        ):
        """
        Sends a new log message with the given string as the message. The output
        of the log has a timestamp added to the beginning of the output.

        Parameters
        ----------
        message : string
                  The log message.
        """
        print(time.strftime("[%D %H:%M:%S] ")+message)
