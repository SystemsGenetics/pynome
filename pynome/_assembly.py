"""
Contains the Assembly class.
"""
from . import core
from . import interfaces
from . import exceptions
import json
import os
import re
from . import settings
import subprocess
import traceback








class Assembly():
    """
    This is the singleton assembly class. It is responsible for registering and
    storing a lookup table of all available crawler, process, and task
    implementations. It provides method for crawling with all implemented
    crawlers, mirroring all local assemblies, and indexing them. Indexing
    methods are provided for splitting up the work for each assembly that needs
    work into separate jobs.
    """


    def __init__(
        self
        ):
        """
        Initializes the singleton assembly instance.
        """
        self.__crawlers = {}
        self.__processes = {}
        self.__tasks = {}


    def index(
        self
        ,taxId
        ,name
        ):
        """
        Indexes the assembly with the given taxonomy ID and assembly name. If
        the indexes are already up to date for that assembly then nothing is
        done.

        Parameters
        ----------
        taxId : string
                The taxonomy ID of the assembly whose indexes are updated.
        name : string
               The name of the assembly whose indexes are updated.
        """
        dataDir = os.path.join(taxId,name)
        workDir = os.path.join(settings.rootPath,dataDir)
        if os.path.isdir(workDir):
            meta = self.__loadMeta_(workDir)
            rootName = self.__rootName_(meta)
            process = self.__processes[meta["process_type"]]
            for taskName in process.indexTasks():
                if process.hasWork(workDir,rootName,meta["processed"],taskName):
                    task = self.__tasks[taskName](dataDir,rootName,meta["process_data"])
                    #try:
                    if task():
                        process.completeTask(taskName,meta["processed"])
                        meta["processed"][taskName] = True
                        self.__saveMeta_(workDir,meta)
                    #except:
                    #    pass


    def indexSpecies(
        self
        ,species
        ):
        """
        Indexes all assemblies with the given species name. If the indexes are
        already up to date for any matched assembly then it is skipped.

        Parameters
        ----------
        species : string
                  The species name matched with assemblies to index.
        """
        if not species:
            return
        for taxId in os.listdir(settings.rootPath):
            if taxId.isdecimal():
                path = os.path.join(settings.rootPath,taxId)
                if os.path.isdir(path):
                    for assemblyName in os.listdir(path):
                        meta = self.__loadMeta_(os.path.join(settings.rootPath,taxId,assemblyName))
                        fullName = meta["genus"].lower()+" "+meta["species"].lower()
                        if not species.lower() in fullName:
                            continue
                        self.index(taxId,assemblyName)


    def listAllWork(
        self
        ):
        """
        Getter method.

        Returns
        -------
        ret0 : list
               Tuples of taxonomy ID and assembly id of all assemblies whose
               indexes require updating.
        """
        ret = []
        for taxId in os.listdir(settings.rootPath):
            if taxId.isdecimal():
                path = os.path.join(settings.rootPath,taxId)
                if os.path.isdir(path):
                    for assemblyName in os.listdir(path):
                        workDir = os.path.join(settings.rootPath,taxId,assemblyName)
                        meta = self.__loadMeta_(workDir)
                        process = self.__processes[meta["process_type"]]
                        if process.hasWork(workDir,self.__rootName_(meta),meta["processed"]):
                            ret.append((taxId,assemblyName))
        return ret


    def mirror(
        self
        ,species
        ):
        """
        Iterates through all local database folders, inspecting their metadata
        file and downloading any new data files if new versions are present on
        the remote server. Any assembly whose data is updated is marked to
        update its appropriate indexes.

        Parameters
        ----------
        species : string
                  The name of the species that is mirrored, ignoring any other
                  species on the local database. If this string is blank then
                  all species are mirrored.
        """
        for taxId in os.listdir(settings.rootPath):
            if taxId.isdecimal():
                path = os.path.join(settings.rootPath,taxId)
                if os.path.isdir(path):
                    for assemblyName in os.listdir(path):
                        dataDir = os.path.join(taxId,assemblyName)
                        workDir = os.path.join(settings.rootPath,dataDir)
                        meta = self.__loadMeta_(workDir)
                        if species:
                            fullName = meta["genus"].lower()+" "+meta["species"].lower()
                            if not species.lower() in fullName:
                                continue
                        rootName = self.__rootName_(meta)
                        process = self.__processes[meta["process_type"]]
                        for taskName in process.mirrorTasks():
                            task = self.__tasks[taskName](dataDir,rootName,meta["process_data"])
                            try:
                                if task():
                                    process.completeTask(taskName,meta["processed"])
                                    self.__saveMeta_(workDir,meta)
                            except:
                                pass


    def crawl(
        self
        ,species
        ):
        """
        Iterates through all registered crawler implementations and crawls their
        remote database to update the local database metadata.

        Parameters
        ----------
        species : string
                  The name of the species that is crawled, ignoring any other
                  species found on the remote server. If this string is blank
                  then all species are crawled.
        """
        self.__prepareDataDirs_()
        for crawler in self.__crawlers.values():
            crawler.crawl(species)
            crawler.assemble()


    def registerCrawler(
        self
        ,crawler
        ):
        """
        Registers a new crawler implementation with the given class instance.

        Parameters
        ----------
        crawler : instance
                  The abstract crawler implementation that is registered.
        """
        if not isinstance(crawler,interfaces.AbstractCrawler):
            raise exceptions.RegisterError("Given object is not Crawler instance.")
        if crawler.name() in self.__crawlers:
            raise exceptions.RegisterError("Crawler '"+name+"' already exists.")
        self.__crawlers[crawler.name()] = crawler


    def registerProcess(
        self
        ,process
        ):
        """
        Registers a new process implementation with the given class instance.

        Parameters
        ----------
        process : instance
                  The abstract process implementation that is registered.
        """
        if not isinstance(process,interfaces.AbstractProcess):
            raise exceptions.RegisterError("Given object is not Process instance.")
        if process.name() in self.__processes:
            raise exceptions.RegisterError("Process '"+name+"' already exists.")
        self.__processes[process.name()] = process


    def registerTask(
        self
        ,taskClass
        ):
        """
        Registers a new task implementation with the given class.

        Parameters
        ----------
        taskClass : class
                    The abstract crawler implementation class that is
                    registered.
        """
        if not issubclass(taskClass,interfaces.AbstractTask):
            raise exceptions.RegisterError("Given class is not Task subclass.")
        t = taskClass(None,None,None)
        if t.name() in self.__tasks:
            raise exceptions.RegisterError("Task '"+name+"' already exists.")
        self.__tasks[t.name()] = taskClass


    def __loadMeta_(
        self
        ,workDir
        ):
        """
        Getter method.

        Parameters
        ----------
        workDir : string
                  The working directory where the metadata JSON file is located.

        Returns
        -------
        ret0 : dictionary
               The metadata information for the given working directory. If the
               processed keys are not set then they are added and set to false.
        """
        with open(os.path.join(workDir,"metadata.json"),"r") as ifile:
            meta = json.loads(ifile.read())
            return meta


    def __prepareDataDirs_(
        self
        ):
        """
        Creates any of the special data directories for all implemented crawlers
        if they do not exist.
        """
        for crawler in self.__crawlers.values():
            d = os.path.join(settings.rootPath,"."+crawler.name())
            os.makedirs(d,exist_ok=True)


    def __rootName_(
        self
        ,meta
        ):
        """
        Getter method.

        Parameters
        ----------
        meta : dictionary
               Metadata of the given assembly whose root name for data files is
               returned.

        Returns
        -------
        ret0 : string
               The root name that must be used for all data files of the given
               assembly.
        """
        ret = meta["genus"]+"_"+meta["species"]
        if meta["intraspecific_name"]:
            ret += "_"+meta["intraspecific_name"]
        ret += "-"+meta["assembly_id"].replace(" ","_")
        return re.sub("[\s\\\\/]","_",ret)


    def __saveMeta_(
        self
        ,workDir
        ,meta
        ):
        """
        Saves the given assembly metadata to the given working directory.

        Parameters
        ----------
        workDir : string
                  The working directory where the given assembly metadata is
                  saved as JSON to the special "metadata.json" file.
        meta : dictionary
               The given assembly metadata that is saved to the given working
               directory as JSON.
        """
        with open(os.path.join(workDir,"metadata.json"),"w") as ofile:
            return ofile.write(json.dumps(meta,indent=4) + "\n\n")
