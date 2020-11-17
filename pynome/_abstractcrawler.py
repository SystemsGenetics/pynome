"""
Contains the AbstractCrawler class.
"""
from . import core
import abc
import json
import os
import re
from . import settings








class AbstractCrawler(abc.ABC):
    """
    This is the abstract crawler class. An interface is provided that crawls its
    source and adds entries to be added to the local file structure.
    """


    def __init__(
        self
        ):
        """
        Initializes a new abstract crawler instance.
        """
        super().__init__()
        self.__entries = {}


    def assemble(
        self
        ):
        """
        Updates the directory structure and metadata JSON files of the local
        database with all entries added to this crawler, creating directories
        and files that do not exist and overwriting ones that do. If a metadata
        JSON file already exists for a written assembly, the processed data is
        preserved in the new JSON file. This also clears all entries added from
        this crawler's crawl method.
        """
        for key in self.__entries:
            d = os.path.join(settings.rootPath,key)
            os.makedirs(d,exist_ok=True)
            path = os.path.join(d,"metadata.json")
            processed = {}
            if os.path.isfile(path):
                with open(path,"r") as ifile:
                    oldmeta = json.loads(ifile.read())
                    processed = oldmeta["processed"]
            meta = self.__entries[key]
            meta["processed"] = processed
            with open(os.path.join(d,"metadata.json"),"w") as ofile:
                ofile.write(json.dumps(meta,indent=4) + "\n")
        self.__entries = {}


    @abc.abstractmethod
    def crawl(
        self
        ,species=""
        ):
        """
        This interface crawls the remote database, adding all entries it finds
        to be added to the local file database. An optional species name can be
        provided that restricts entries being added to only that species if it
        is not an empty string.

        Parameters
        ----------
        species : string
                  Species name used to restrict the entries added to only that
                  species. If this is empty then all species are added.
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
               The name of this crawler implementation that must be unique among
               all registered crawlers and is used as the root directory name
               for the local database.
        """
        pass


    def _addEntry_(
        self
        ,genus
        ,species
        ,intraspecificName
        ,assemblyId
        ,taxonomyId
        ,processType
        ,processData
        ):
        """
        Adds a database entry for this crawler to be used in assembling the
        local directories and JSON metadata.

        Parameters
        ----------
        genus : string
                The genus of the entry.
        species : string
                  The species of the entry.
        intraspecificName : string
                            The intra-specific name of the entry.
        assemblyId : string
                     The assembly ID of the entry.
        taxonomyId : string
                     The taxonomy ID of the entry.
        processType : string
                      The process type of the entry, determining which process
                      interface is used for downloading and indexing its data.
        processData : dictionary
                      The JSON compatible data the process type requires for
                      downloading and indexing this entries data from its remote
                      source.
        """
        assert(taxonomyId.isdigit())
        key = os.path.join(taxonomyId,re.sub("[\s\\\\/]","_",assemblyId+"-"+self.name()))
        self.__entries[key] =  {
            "genus": genus
            ,"species": species
            ,"intraspecific_name": intraspecificName
            ,"assembly_id": assemblyId
            ,"taxonomy": {
                "name": " ".join((p for p in (genus,species,intraspecificName) if p))
                ,"id": taxonomyId
            }
            ,"process_type": processType
            ,"process_data": processData
        }


    def _dataDir_(
        self
        ):
        """
        Getter method.

        Returns
        -------
        ret0 : string
               The full path to the special hidden data directory this crawler
               can use for any remote data files required for crawling.
        """
        return os.path.join(settings.rootPath,"."+self.name())


    def _log_(
        self
        ,message
        ):
        """
        Adds the given message to the logging system. A parenthesis enclosed tag
        is included at the beginning of the message to show the user what
        crawler the message is coming from.

        Parameters
        ----------
        message : string
                  Message that is sent to the logging system.
        """
        core.log.send("("+self.name()+") "+message)
