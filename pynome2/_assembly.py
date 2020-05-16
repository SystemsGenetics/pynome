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
        Initializes the initial singleton assembly instance.
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


    def registerCrawler(
        self
        ,crawler
        ,name
        ):
        """
        Registers a new crawler implementation with the given name and class
        instance.

        Parameters
        ----------
        crawler : pynome.abstract.AbstractCrawler
                  The abstract crawler implementation that is registered.
        name : string
               The name of the crawler implementation registered which must be
               unique among all other registered crawlers.
        """
        if name in self.__crawlers.keys():
            raise exception.RegisterError("Crawler '"+name+"' already exists.")
        if not isinstance(crawler,abstract.AbstractCrawler):
            raise exception.RegisterError("Given object is not Crawler instance.")
        self.__crawlers[name] = crawler
