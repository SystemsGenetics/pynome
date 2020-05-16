"""
Contains the AbstractCrawler class.
"""
import abc
import json








class AbstractCrawler(abc.ABC):
    """
    This is the abstract crawler class. An interface is provided that crawls its
    source and adds entries to be added to the local file structure. This class
    provides a protected function for adding entries to the local database.
    """


    #######################
    # PUBLIC - Interfaces #
    #######################


    @abc.abstractmethod
    def crawl(
        self
        ,species=""
        ):
        """
        This interface Crawls the remote database, adding all entries it finds
        to be added to the local file database. An optional species name can be
        provided that restricts entries being added to only that species if it
        is not an empty string.

        Parameters
        ----------
        species : string
                  Species name used to restrict the entries added to only that
                  species. If this is empty then all species are added.
        """
        abc.ABC.__init__(self)


    ####################
    # PUBLIC - Methods #
    ####################


    def assemble(
        self
        ):
        """
        Updates the directory structure and metadata JSON files of the local
        database with all entries added to this crawler, creating directories
        and files that do not exist and overwriting ones that do.
        """
        pass


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
        print(
            json.dumps(
                {
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
                ,indent=4
            )
            + "\n\n"
        )
