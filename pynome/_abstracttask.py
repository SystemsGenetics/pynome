"""
Contains the AbstractTask class.
"""
import abc
from . import core
import os
from . import settings








class AbstractTask(abc.ABC):
    """
    This is the abstract task class. It represents a single task to be done for
    a process type to mirror or index a specific output of data for a specific
    assembly.
    """


    def __init__(
        self
        ,dataDir
        ,rootName
        ,meta
        ):
        """
        Initializes a new implemented task.

        Parameters
        ----------
        dataDir : string
                  The data directory of the assembly for this new task. This
                  does not include the root directory path.
        rootName : string
                   The root name used for naming all output data files produced
                   by this task for its assembly.
        meta : dictionary
               The processed part of the metadata of this task's assembly.
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
        This interface executes this tasks implementation.

        Returns
        -------
        ret0 : bool
               True if this task successfully executed or false otherwise. For
               mirror tasks successful execution means a new remote file was
               downloaded to the local assembly.
        """
        pass


    @abc.abstractmethod
    def name(
        self
        ):
        """
        This interface is a getter method.

        Returns
        -------
        ret0 : string
               The name of this task implementation that must be unique among
               all registered tasks.
        """
        pass


    def _log_(
        self
        ,message
        ):
        """
        Adds the given message to the logging system. A parenthesis enclosed tag
        is included at the beginning of the message to show the user what
        assembly this task is running on.

        Parameters
        ----------
        message : string
                  Message that is sent to the logging system.
        """
        core.log.send("("+self.__dataDir+") "+message)


    def _meta_(
        self
        ):
        """
        Getter method.

        Returns
        -------
        ret0 : dictionary
               The processed part of this task's assembly's metadata.
        """
        return self.__meta


    def _rootName_(
        self
        ):
        """
        Getter method.

        Returns
        -------
        ret0 : string
               The root name that must be used for naming any output files
               produced by this task, excluding whatever extension is given to
               each output file.
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

        Returns
        -------
        ret0 : string
               The full path of the working directory of this task's assembly
               where any output file should be placed.
        """
        return os.path.join(settings.rootPath,self.__dataDir)
