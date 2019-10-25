"""
todo
"""
from .singleton import singleton






def register_crawler(path):
    """
    todo
    """
    # Dummy wrapper function that returns the crawler.
    def wrapper(function):
        # Register the crawler function and return it.
        Assembly().register_crawler(function,path)
        return function
    return wrapper






class RegisterError(Exception):
    """
    todo
    """

    def __init__(self,*args):
        """
        todo
        """
        Exception.__init__(self,*args)





@singleton
class Assembly():
    """
    todo
    """

    def __init__(self):
        """
        todo
        """
        self.__paths = {}

    def register_crawler(self,function,path):
        """
        todo
        """
        # Make sure the given path is not already registered with a crawler.
        if path in self.__paths.keys():
            raise RegisterError(f"Assembly path '{path}' already exists.")
        # Register the given crawler to the given path.
        self.__paths[path] = function

    def crawl(self):
        """
        todo
        """
        for crawler in self.__paths.values(): crawler()






# Import all crawlers AFTER the register function and Assembly class are defined.
from .crawl import ensembl
