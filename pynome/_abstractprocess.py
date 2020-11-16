"""
Contains the AbstractProcess class.
"""
import abc
import os








class AbstractProcess(abc.ABC):
    """
    This is the abstract process class. This provides a list of tasks used for
    mirroring and indexing an assembly. Interfaces are provided for getting the
    list of tasks for mirroring and indexing. Interfaces are also provided for
    getting the input files and task dependencies on other tasks.
    """


    def completeTask(
        self
        ,taskName
        ,meta
        ):
        """
        Completes the given task of the given assembly, marking all dependency
        tasks as needing work.

        Parameters
        ----------
        taskName : string
                   The name of the task which has completed.
        meta : dictionary
               The processed part of the given assembly whose tasks are marked
               as work needed for all dependencies of the given task.
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
        Getter method.

        Parameters
        ----------
        workDir : string
                  The full path working directory for the given assembly.
        rootName : string
                   The root name used for all data files of the given assembly.
        meta : dictionary
               The processed dictionary part of the given assembly's metadata.
        taskName : object
                   None to check all tasks of this process of the given assembly
                   or a task name to only check that specific task while
                   ignoring all others.

        Returns
        -------
        ret0 : bool
               True the given assembly has work or false otherwise. If a task
               name is given then only that task is checked for it needing to be
               executed again and all other tasks for this process is ignored.
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
        This interface is a getter method.

        Returns
        -------
        ret0 : list
               String names of tasks that are used for this process
               implementation to index its assembly data. Tasks are done in
               order of the returned list.
        """
        pass


    @abc.abstractmethod
    def mirrorTasks(
        self
        ):
        """
        This interface is a getter method.

        Returns
        -------
        ret0 : list
               String names of tasks that are used for this process
               implementation to mirror its assembly data. Tasks are done in
               order of the returned list.
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
               The name of this process implementation that must be unique among
               all registered processes.
        """
        pass


    @abc.abstractmethod
    def taskInputs(
        self
        ,taskName
        ):
        """
        This interface is a getter method.

        Parameters
        ----------
        taskName : string
                   The task name whose input file requirements are returned.

        Returns
        -------
        ret0 : list
               Extensions of files, using the root name as its base, that are
               required for the given task to be executed.
        """
        pass


    @abc.abstractmethod
    def taskSources(
        self
        ,taskName
        ):
        """
        This interface is a getter method.

        Parameters
        ----------
        taskName : string
                   The task name whose task dependencies are returned.

        Returns
        -------
        ret0 : list
               Names of tasks which must cause the given task to be executed
               again if any of them are executed.
        """
        pass
