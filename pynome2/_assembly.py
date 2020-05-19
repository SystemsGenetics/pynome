"""
Contains the Assembly class.
"""
from . import abstract
from . import exception








class Assembly():
    """
    This is the singleton assembly class. It is responsible for storing a list
    of all available crawler and mirror implementations. It provides method for
    crawling with all implemented crawlers along with syncing all local database
    files using the available mirrors.
    """


    #######################
    # PUBLIC - Initialize #
    #######################


    def __init__(
        self
        ):
        """
        Initializes the singleton assembly instance.
        """
        self.__crawlers = {}


    ####################
    # PUBLIC - Methods #
    ####################


    def crawl(
        self
        ):
        """
        Iterates through all registered crawler implementations and crawls their
        remote database to update the local database metadata.
        """
        for crawler in self.__crawlers.values():
            crawler.crawl()
            crawler.assemble()


    def registerCrawler(
        self
        ,crawler
        ):
        """
        Registers a new crawler implementation with the given class instance.

        Parameters
        ----------
        crawler : pynome.abstract.AbstractCrawler
                  The abstract crawler implementation that is registered.
        """
        if not isinstance(crawler,abstract.AbstractCrawler):
            raise exception.RegisterError("Given object is not Crawler instance.")
        if crawler.name() in self.__crawlers.keys():
            raise exception.RegisterError("Crawler '"+name+"' already exists.")
        self.__crawlers[crawler.name()] = crawler
