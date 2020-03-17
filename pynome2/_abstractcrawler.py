"""
Contains the AbstractCrawler class.
"""
import abc








class AbstractCrawler(abc.ABC):
    """
    Detailed description.
    """


    #######################
    # PUBLIC - Interfaces #
    #######################


    @abc.abstractmethod
    def crawl(self, species=""):
        """
        Detailed description.

        Parameters
        ----------
        species : string
                  Detailed description.
        """
        abc.ABC.__init__(self)


    ####################
    # PUBLIC - Methods #
    ####################


    def assemble(self, rootPath):
        """
        Detailed description.

        Parameters
        ----------
        rootPath : string
                   Detailed description.
        """
        pass


    #######################
    # PROTECTED - Methods #
    #######################


    def addEntry(self, species, genus, intraspecificName, assemblyId, taxonomyName, taxonomyId, mirrorData):
        """
        Detailed description.

        Parameters
        ----------
        species : string
                  Detailed description.
        genus : string
                Detailed description.
        intraspecificName : string
                            Detailed description.
        assemblyId : string
                     Detailed description.
        taxonomyName : string
                       Detailed description.
        taxonomyId : string
                     Detailed description.
        mirrorData : dictionary
                     Detailed description.
        """
        pass
