"""
Contains the Log class.
"""
import time








class Log():
    """
    This is the singleton log class. It is responsible for logging any messages
    given to it from anywhere else in the application, putting a timestamp on
    the output of every message. This is designed to be the central location for
    any standard output. An echo state can be enabled or disabled, allowing the
    program to be quiet by disabling it.
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
        self.__echo = True


    ####################
    # PUBLIC - Methods #
    ####################


    def setEcho(
        self
        ,echo
        ):
        """
        Sets the echo state of this singleton log class, determining if the send
        method echos what it is given to standard output.

        Parameters
        ----------
        echo : bool
               True will make send requests be echoed or false to be silent.
        """
        self.__echo = echo


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
        if self.__echo:
            print(time.strftime("[%D %H:%M:%S] ")+message)
