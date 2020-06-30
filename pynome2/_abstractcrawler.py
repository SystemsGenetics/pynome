"""
Contains the AbstractCrawler class.
"""
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


    #######################
    # PUBLIC - Initialize #
    #######################


    def __init__(
        self
        ):
        """
        Initializes a new abstract crawler instance.
        """
        abc.ABC.__init__(self)
        self.__entries = {}


    #######################
    # PUBLIC - Interfaces #
    #######################


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


    ####################
    # PUBLIC - Methods #
    ####################


    def assemble(
        self
        ):
        """
        Updates the directory structure and metadata JSON files of the local
        database with all entries added to this crawler, creating directories
        and files that do not exist and overwriting ones that do. This also
        clears all entries added from this crawler's crawl method.
        """
        for key in self.__entries:
            d = os.path.join(settings.rootPath,key)
            os.makedirs(d,exist_ok=True)
            with open(os.path.join(d,"metadata.json"),"w") as ofile:
                ofile.write(json.dumps(self.__entries[key],indent=4) + "\n\n")
        self.__entries = {}


    #######################
    # PROTECTED - Methods #
    #######################


    def _addEntry_(
        self
        ,genus
        ,species
        ,intraspecificName
        ,assemblyId
        ,taxonomyId
        ,mirrorType
        ,mirrorData
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
        mirrorType : string
                     The mirror type of the entry, determining which mirror
                     interface is used for downloading its data.
        mirrorData : dictionary
                     The JSON compatible data the mirror type requires for
                     downloading this entries data from its remote source.
        """
        key = os.path.join(taxonomyId,assemblyId+"-"+self.name())
        if key in self.__entries:
            core.log.send(
                "Duplicate entries '%s' found in crawler %s! Overwriting existing entry!"
                % (key,self.name())
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
            ,"mirror_type": mirrorType
            ,"mirror_data": mirrorData
        }


    def _dataDir_(
        self
        ):
        """
        Detailed description.
        """
        return os.path.join(settings.rootPath,"."+self.name())
