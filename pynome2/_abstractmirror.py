"""
Contains the AbstractMirror class.
"""
import abc








class AbstractMirror(abc.ABC):
    """
    This is the abstract mirror class. An interface is provided that mirrors the
    given species entry. The working directory is provided where the data files
    should be mirrored along with their required name.
    """


    #######################
    # PUBLIC - Initialize #
    #######################


    def __init__(
        self
        ):
        """
        Initializes a new abstract mirror instance.
        """
        abc.ABC.__init__(self)


    #######################
    # PUBLIC - Interfaces #
    #######################


    @abc.abstractmethod
    def mirrorFasta(
        self
        ,workingDir
        ,path
        ,meta
        ,title
        ):
        """
        This interface mirrors a specific species from a remote database, adding
        the required FASTA and GFF files with the given names to the given
        working directory. The custom mirror section of the metadata is also
        provided. NOPE

        Parameters
        ----------
        workingDir : string
                     Path to the working directory where the FASTA and GFF files
                     should be saved locally.
        path : object
               NOPE
        meta : dictionary
               The custom mirror metadata created by the crawler and intended
               for use by this mirror implementation.
        title : object
                Detailed description.

        Returns
        -------
        ret0 : bool
               True if a new FASTA file was downloaded or false otherwise.
        ret1 : bool
               True if a new GFF3 file was downloaded or false otherwise.
        """
        pass


    @abc.abstractmethod
    def mirrorGff(
        self
        ,workingDir
        ,path
        ,meta
        ,title
        ):
        """
        This interface mirrors a specific species from a remote database, adding
        the required FASTA and GFF files with the given names to the given
        working directory. The custom mirror section of the metadata is also
        provided. NOPE

        Parameters
        ----------
        workingDir : string
                     Path to the working directory where the FASTA and GFF files
                     should be saved locally.
        path : object
               NOPE
        meta : dictionary
               The custom mirror metadata created by the crawler and intended
               for use by this mirror implementation.
        title : object
                Detailed description.

        Returns
        -------
        ret0 : bool
               True if a new FASTA file was downloaded or false otherwise.
        ret1 : bool
               True if a new GFF3 file was downloaded or false otherwise.
        """
        pass
