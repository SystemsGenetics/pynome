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
        self.__ftp = ftplib.FTP("ftp.ncbi.nlm.nih.gov",timeout=10)
        self.__ftp.login()
        core.log.send("Downloading NCBI assembly summary...")
        self.__lines = []
        self.__ftp.retrlines("RETR /genomes/genbank/assembly_summary_genbank.txt",self.__write_)
        core.log.send("Crawling NCBI assembly summary...")
        for text in self.__lines:
            if text and text[0] != "#":
                parts = text.split("\t")
                sParts = parts[7].split()
                sParts = [sParts[0]," ".join(sParts[1:])]
                if species and not species in sParts[1]:
                    continue
                if parts[6] in self.__safeSTIDs:
                    fasta = parts[-3]
                    gff = fasta + fasta[fasta.rfind("/"):] + "_genomic.gff.gz"
                    fasta = fasta + fasta[fasta.rfind("/"):] + "_genomic.fna.gz"
                    self._addEntry_(
                        sParts[0]
                        ,sParts[1]
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


    def __loadTaxonomy_(
        self
        ):
        """
        Detailed description.
        """
        tarPath = os.path.join(self._dataDir_(),"taxdump.tar.gz")
        if utility.rSync("ftp.ncbi.nlm.nih.gov/pub/taxonomy/taxdump.tar.gz",tarPath):
            cmd = ["tar","-xvf",tarPath,"-C",self._dataDir_()]
            assert(subprocess.run(cmd,capture_output=True).returncode==0)
        safe = ["INV","MAM","PLN","PRI","ROD","VRT"]
        divs = []
        with open(os.path.join(self._dataDir_(),"division.dmp"),"r") as ifile:
            while True:
                line = ifile.readline()
                if not line:
                    break
                parts = [l.strip() for l in line.split("|")]
                if parts[1] in safe:
                    divs.append(parts[0])
        with open(os.path.join(self._dataDir_(),"nodes.dmp"),"r") as ifile:
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
        downloading a taxonomy ID file.

        Parameters
        ----------
        text : string
               The string that is appended to this crawlers special placeholder
               text.
        """
        self.__lines.append(text)
