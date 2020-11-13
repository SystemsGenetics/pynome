"""
Contains the AbstractProcess class.
"""
import abc








class AbstractProcess(abc.ABC):
    """
    This is the abstract mirror class. An interface is provided that mirrors the
    given species entry. The working directory is provided where the data files
    should be mirrored along with their required name. DEPRECATED_COMMENT
    """


    @abc.abstractmethod
    def indexTasks(
        self
        ):
        """
        Detailed description.
        """
        pass


    @abc.abstractmethod
    def mirrorTasks(
        self
        ):
        """
        Detailed description.
        """
        pass


    @abc.abstractmethod
    def name(
        self
        ):
        """
        Detailed description.
        """
        pass


    @abc.abstractmethod
    def taskSources(
        self
        ,task
        ):
        """
        Detailed description.

        Parameters
        ----------
        task : object
               Detailed description.
        """
        pass
