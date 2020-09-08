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
        This interface mirrors the FASTA file of a specific assembly from a
        remote database, adding the required FASTA file with the given name to
        the given working directory. The custom mirror section of the metadata
        is also provided.

        Parameters
        ----------
        workingDir : string
                     Path to the working directory where the FASTA file must be
                     saved locally.
        path : string
               The full file name where the remote FASTA files must be mirrored
               to within the given working directory.
        meta : dictionary
               The custom mirror metadata created by the crawler and intended
               for use by this mirror implementation.
        title : string
                The title of the assembly whose FASTA file is being mirrored.
                This can be used with log messages to identify the assembly to
                the user.

        Returns
        -------
        ret0 : bool
               True if a new FASTA file was downloaded or false otherwise.
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
        This interface mirrors the GFF file of a specific assembly from a remote
        database, adding the required GFF file with the given name to the given
        working directory. The custom mirror section of the metadata is also
        provided.

        Parameters
        ----------
        workingDir : string
                     Path to the working directory where the FASTA and GFF files
                     should be saved locally.
        path : string
               The full file name where the remote FASTA files must be mirrored
               to within the given working directory.
        meta : dictionary
               The custom mirror metadata created by the crawler and intended
               for use by this mirror implementation.
        title : string
                The title of the assembly whose FASTA file is being mirrored.
                This can be used with log messages to identify the assembly to
                the user.

        Returns
        -------
        ret0 : bool
               True if a new GFF file was downloaded or false otherwise.
        """
        pass
