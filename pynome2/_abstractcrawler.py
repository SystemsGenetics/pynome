"""
Contains the AbstractCrawler class.
"""








@abc.ABC
class AbstractCrawler():
    """
    Detailed description.
    """


    #######################
    # PUBLIC - Interfaces #
    #######################


    @abc.abstractmethod
    def crawl(self):
        """
        Detailed description.
        """
        pass


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


    def addEntry(self, species, genus, intraspecificName, assemblyId, taxonomyName, taxonomyId, mirrorJson):
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
        mirrorJson : string
                     Detailed description.
        """
        pass
