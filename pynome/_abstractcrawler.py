"""
Contains the AbstractCrawler class.
"""
from . import core
import abc
import json
import os
from . import settings








class AbstractCrawler(abc.ABC):
    """
    This is the abstract crawler class. An interface is provided that crawls its
    source and adds entries to be added to the local file structure. This class
    provides a protected function for adding entries to the local database.
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
        and files that do not exist and overwriting ones that do. This also
        clears all entries added from this crawler's crawl method.
        DEPRECATED_COMMENT
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
        ret0 : object
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
                      The mirror type of the entry, determining which mirror
                      interface is used for downloading its data.
                      DEPCRECATED_COMMENT
        processData : dictionary
                      The JSON compatible data the mirror type requires for
                      downloading this entries data from its remote source.
                      DEPCRECATED_COMMENT
        """
        assert(taxonomyId.isdigit())
        key = os.path.join(
            taxonomyId
            ,assemblyId.replace("/","|").replace("\\","|") + "-" + self.name()
        )
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
        Detailed description.

        Parameters
        ----------
        message : object
                  Detailed description.
        """
        core.log.send("("+self.name()+") "+message)
