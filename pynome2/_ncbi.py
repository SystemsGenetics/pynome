"""
Contains the NCBI class.
"""
import ftplib
from . import abstract
from . import core








class NCBI(abstract.AbstractCrawler):
    """
    NOPE
    """


    #######################
    # PUBLIC - Initialize #
    #######################


    def __init__(
        self
        ):
        """
        Initializes a new ensembl crawler.
        """
        abstract.AbstractCrawler.__init__(self)
        self.__ftp = None


    ####################
    # PUBLIC - Methods #
    ####################


    def crawl(
        self
        ,species=""
        ):
        """
        Implements the pynome2.abstract.AbstractCrawler interface.

        Parameters
        ----------
        species : object
                  See interface docs.
        """
        self.__ftp = ftplib.FTP("ftp.ncbi.nlm.nih.gov",timeout=10)
        self.__ftp.login()
        core.log.send("Downloading NCBI metadata...")
        self.__ftp.retrlines("RETR /genomes/genbank/assembly_summary_genbank.txt",self.__write_)


    def name(
        self
        ):
        """
        Implements the pynome2.abstract.AbstractCrawler interface.

        Returns
        -------
        ret0 : object
               See interface docs.
        """
        return "ncbi"


    #####################
    # PRIVATE - Methods #
    #####################


    def __write_(
        self
        ,text
        ):
        """
        Callback function for writing to this crawlers special text holder for
        downloading a taxonomy ID file.

        Parameters
        ----------
        text : string
               The string that is appended to this crawlers special placeholder
               text.
        """
        if text and text[0] != "#":
            parts = text.split("\t")
            print(parts[5],parts[7],parts[8],parts[15],parts[-3])
