"""This module contains the AssmeblyDatabase class.

.. module:: assemblydatabase
    :platform: Unix
    :synopsis: An abstract base class that defines an API and
    common functions for genome assembly sources.

.. moduleauthor:: Tyler Biggs <biggstd@gmail.com>
"""

# Import general python packages.
import abc

# Inter-package imports.
from pynome.assembly import Assembly


class AssemblyDatabase(abc.ABC):
    """Base class for remote genome assembly databases.

    .. warning:: This class cannot be directly instantiated.
    """
    def __init__(self, name, url, description, assemblies=None):
        """Initialization function, set up and assign attributes.
        """

        # Define the public attributes of the class.
        self.name = name
        self.url = url
        self.description = description

        # Define the private attributes / properties of the class.
        # If no assemblies are passed to the initialization function,
        # create an empty list for the assemblies to be stored.
        # Otherwise simply assign those values passed to the attribute.
        if assemblies is None:
            self.__assemblies = list()
        else:
            self.__assemblies = assemblies

    @property
    def assemblies(self):
        """A list container for assembly objects.
        """
        return self.__assemblies

    @assemblies.setter
    def assemblies(self, val):
        """The setter for the assemblies list.

        Ensures that all objects passed to / stored in this
        private attribute are instances of the Assembly class.
        """
        # If the value is not empty and is can be iterated,
        # check to see if each internal value is an Assembly object.
        # If so, assign them to the private self.__assemblies attribute.
        if val is not None and hasattr(val, '__iter__'):
            if val == [] or all(isinstance(x, Assembly) for x in val):
                self.__assemblies = list(val)

        # Otherwise, raise an error complaining about invalid attributes.
        else:
            raise AttributeError(
                '{0} assemblies must be an list containing Assembly '
                'objects.'.format(type(self).__name__))

    @abc.abstractmethod
    def crawl(self):
        """An abstract method. Child classes must define crawl functions.
        """
        pass

    def list_assemblies(self):
        """Returns a list of all assembly objects within the assemblies list.
        """
        # Return a list generator containing every object within the
        # self.__assemblies list.
        return [a for a in self.__assemblies]
