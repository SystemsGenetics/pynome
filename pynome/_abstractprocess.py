"""
Contains the AbstractProcess class.
"""
import abc
import os








class AbstractProcess(abc.ABC):
    """
    This is the abstract mirror class. An interface is provided that mirrors the
    given species entry. The working directory is provided where the data files
    should be mirrored along with their required name. DEPRECATED_COMMENT
    """


    def completeTask(
        self
        ,taskName
        ,meta
        ):
        """
        Detailed description.

        Parameters
        ----------
        taskName : object
                   Detailed description.
        meta : object
               Detailed description.
        """
        for tn in self.indexTasks():
            if taskName in self.taskSources(tn):
                meta[tn] = False


    def hasWork(
        self
        ,workDir
        ,rootName
        ,meta
        ,taskName=None
        ):
        """
        Detailed description.

        Parameters
        ----------
        workDir : object
                  Detailed description.
        rootName : object
                   Detailed description.
        meta : object
               Detailed description.
        taskName : object
                   Detailed description.
        """
        def taskHasWork(tn):
            files = [os.path.join(workDir,rootName+ext) for ext in self.taskInputs(tn)]
            for f in files:
                if not os.path.isfile(f):
                    return False
            return not meta[tn]
        if not taskName is None:
            return taskHasWork(taskName)
        else:
            for tn in self.indexTasks():
                if taskHasWork(tn):
                    return True
            return False


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
    def taskInputs(
        self
        ,taskName
        ):
        """
        Detailed description.

        Parameters
        ----------
        taskName : object
                   Detailed description.
        """
        pass


    @abc.abstractmethod
    def taskSources(
        self
        ,taskName
        ):
        """
        Detailed description.

        Parameters
        ----------
        taskName : object
                   Detailed description.
        """
        pass
