"""
Contains the NCBI class.
"""
import ftplib
import os
import subprocess
from . import abstract
from . import core
from . import utility








class NCBI(abstract.AbstractCrawler):
    """
    This is the NCBI class. It implements the abstract crawler interface. The
    remote database is crawled in three stages.

    The first stage is downloading and parsing the taxonomy database dump. This
    allows the crawler to build a list of taxonomy IDs that are part of a valid
    division and should be added locally.

    The second stage is downloading the full assembly list and parsing it. Each
    listing is verified to be part of a desired division and then verified to
    have a proper GFF file in its remote location. If both tests pass its entry
    is added locally.
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
        self.__lines = []
        self.__safeSTIDs = set()


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
        self.__loadTaxonomy_()
        self.__ftp = ftplib.FTP(self.__FTP_HOST,timeout=10)
        self.__ftp.login()
        core.log.send("Downloading NCBI assembly summary...")
        self.__lines = []
        self.__ftp.retrlines("RETR "+self.__SUMMARY_PATH,self.__write_)
        core.log.send("Crawling NCBI assembly summary...")
        for text in self.__lines:
            if text and text[0] != "#":
                parts = text.split("\t")
                sParts = parts[7].split()
                sParts = [sParts[0]," ".join(sParts[1:])]
                if species and not species in sParts[1]:
                    continue
                if parts[6] in self.__safeSTIDs and self.__hasGff_(parts[-3]):
                    fasta = parts[-3]
                    gff = fasta + fasta[fasta.rfind("/"):] + self.__GFF_EXTENSION
                    fasta = fasta + fasta[fasta.rfind("/"):] + self.__FASTA_EXTENSION
                    self._addEntry_(
                        sParts[0]
                        ,sParts[1].split()[0]
                        ,parts[8]
                        ,parts[15]
                        ,parts[6]
                        ,"ftp_gunzip"
                        ,{"fasta": fasta, "gff": gff}
                    )


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


    def __hasGff_(
        self
        ,url
        ):
        """
        Getter method.

        Parameters
        ----------
        url : string
              The remote FTP URL which is verified to have a GFF file or not.

        Returns
        -------
        ret0 : bool
               True if the given remote FTP URL has a GFF file within it or
               false otherwise.
        """
        listing = self.__ftp.nlst(url[26:])
        for path in listing:
            if path.endswith(self.__GFF_EXTENSION):
                return True
        return False


    def __loadTaxonomy_(
        self
        ):
        """
        Synchronizes the remote taxonomy dump with the local one and then loads
        all acceptable taxonomy IDs into this crawler. Acceptable IDs are ones
        that match a given list of division IDs.
        """
        tarPath = os.path.join(self._dataDir_(),self.__TAX_NAME)
        core.log.send("Syncing NCBI taxonomy ...")
        if utility.rSync(self.__FTP_HOST+self.__TAX_DIR,tarPath):
            cmd = ["tar","-xvf",tarPath,"-C",self._dataDir_()]
            assert(subprocess.run(cmd,capture_output=True).returncode==0)
        core.log.send("Loading NCBI taxonomy ...")
        divs = []
        with open(os.path.join(self._dataDir_(),self.__DIV_NAME),"r") as ifile:
            while True:
                line = ifile.readline()
                if not line:
                    break
                parts = [l.strip() for l in line.split("|")]
                if parts[1] in self.__VALID_DIVS:
                    divs.append(parts[0])
        with open(os.path.join(self._dataDir_(),self.__NODE_NAME),"r") as ifile:
            while True:
                line = ifile.readline()
                if not line:
                    break
                parts = [l.strip() for l in line.split("|")]
                if parts[4] in divs:
                    self.__safeSTIDs.add(parts[0])


    def __write_(
        self
        ,text
        ):
        """
        Callback function for writing to this crawlers special text holder for
        downloading the full assembly list text file.

        Parameters
        ----------
        text : string
               The string that is appended to this crawlers special placeholder
               text.
        """
        self.__lines.append(text)


    #######################
    # PRIVATE - Constants #
    #######################


    #
    # string The name of the taxonomy divisions dump file.
    #
    __DIV_NAME = "division.dmp"


    #
    # The extension of FASTA files on the ncbi FTP server.
    #
    __FASTA_EXTENSION = "_genomic.fna.gz"


    #
    # The URL of the ncbi FTP server.
    #
    __FTP_HOST = "ftp.ncbi.nlm.nih.gov"


    #
    # The extension of GFF files on the ncbi FTP server.
    #
    __GFF_EXTENSION = "_genomic.gff.gz"


    #
    # string The name of the taxonomy nodes dump file.
    #
    __NODE_NAME = "node.dmp"


    #
    # string The path to the assembly summary gene bank text file iterating all
    # ncbi assemblies.
    #
    __SUMMARY_PATH = "/genomes/genbank/assembly_summary_genbank.txt"


    #
    # string The remote directory path where the taxonomy dump archive is
    # located on the ncbi FTP server.
    #
    __TAX_DIR = "/pub/taxonomy/"


    #
    # string The name of the gunzipped taxonomy dump file.
    #
    __TAX_NAME = "taxdump.tar.gz"


    #
    # list Strings that are valid three character abbreviations of division
    # types that are acceptable and whose assemblies should be added as entries.
    #
    __VALID_DIVS = ["INV","MAM","PLN","PRI","ROD","VRT"]
