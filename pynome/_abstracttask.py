"""
Contains the AbstractTask class.
"""
import abc
from . import core
import os
from . import settings








class AbstractTask(abc.ABC):
    """
    Detailed description.
    """


    def __init__(
        self
        ,dataDir
        ,rootName
        ,meta
        ):
        """
        Detailed description.

        Parameters
        ----------
        dataDir : object
                  Detailed description.
        rootName : object
                   Detailed description.
        meta : object
               Detailed description.
        """
        super().__init__()
        self.__dataDir = dataDir
        self.__rootName = rootName
        self.__meta = meta


    @abc.abstractmethod
    def __call__(
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
        This interface is a getter method.
        """
        pass


    def _log_(
        self
        ,message
        ):
        """
        Detailed description.

        Parameters
        ----------
        message : object
                  Detailed description.
        """
        core.log.send("("+self.__dataDir+") "+message)


    def _meta_(
        self
        ):
        """
        Detailed description.
        """
        return self.__meta


    def _rootName_(
        self
        ):
        """
        Detailed description.
        """
        return self.__rootName


    def _workDir_(
        self
        ,fullPath=True
        ):
        """
        Detailed description.

        Parameters
        ----------
        fullPath : object
                   Detailed description.
        """
        return os.path.join(settings.rootPath,self.__dataDir)
