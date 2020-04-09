"""
Contains the Assembly class.
"""
from . import abstract
from . import exception








class Assembly():
    """
    Detailed description.
    """


    #######################
    # PUBLIC - Initialize #
    #######################


    def __init__(self):
        """
        Detailed description.
        """
        self.__crawlers = {}


    ####################
    # PUBLIC - Methods #
    ####################


    def crawl(self):
        """
        Detailed description.
        """
        for crawler in self.__crawlers.values():
            crawler.crawl()


    def registerCrawler(self, crawler, name):
        """
        Detailed description.

        Parameters
        ----------
        crawler : pynome.abstract.AbstractCrawler
                  Detailed description.
        name : string
               Detailed description.
        """
        if name in self.__crawlers.keys():
            raise exception.RegisterError("Crawler '"+name+"' already exists.")
        if not isinstance(crawler,abstract.AbstractCrawler):
            raise exception.RegisterError("Given object is not Crawler instance.")
        self.__crawlers[name] = crawler
