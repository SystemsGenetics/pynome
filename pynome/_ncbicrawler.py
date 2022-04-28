"""
Contains the NCBICrawler class.
"""
import ftplib
from . import interfaces
import os
import subprocess
from . import utility








class NCBICrawler(interfaces.AbstractCrawler):
    """
    This is the NCBI class. It implements the abstract crawler interface. The
    remote database is crawled in three stages.

    The first stage is downloading and parsing the taxonomy database dump. This
    allows the crawler to build a list of taxonomy IDs that are part of a valid
    division and should be added locally.

    The second stage is downloading the full assembly list and parsing it. Each
    listing is verified to be part of a desired division and then verified to
    have a proper GFF or GTF file in its remote location. The final test makes
    sure it is a reference or representative assembly. If all tests pass its
    entry is added locally.
    """
    __DIV_NAME = "division.dmp"
    __FASTA_EXTENSION = "_genomic.fna.gz"
    __FTP_HOST = "ftp.ncbi.nlm.nih.gov"
    __GFF_EXTENSION = "_genomic.gff.gz"
    __GTF_EXTENSION = "_genomic.gtf.gz"
    __NODE_NAME = "nodes.dmp"
    __SUMMARY_PATH = "/genomes/genbank/assembly_summary_genbank.txt"
    __TAX_DIR = "/pub/taxonomy/"
    __TAX_NAME = "taxdump.tar.gz"
    __VALID_DIVS = ["INV","MAM","PLN","PRI","ROD","VRT"]
    __VALID_CATS = ["reference genome","representative genome"]


    def __init__(
        self
        ):
        """
        Initializes a new ensembl crawler.
        """
        super().__init__()
        self.__ftp = None
        self.__lines = []
        self.__safeSTIDs = set()


    def crawl(
        self
        ,species=""
        ):
        """
        Implements the pynome.interfaces.AbstractCrawler interface.

        Parameters
        ----------
        species : object
                  See interface docs.
        """
        self.__loadTaxonomy_()
        self.__ftp = ftplib.FTP(self.__FTP_HOST,timeout=10)
        self.__ftp.login()
        self._log_("Downloading assembly summary...")
        self.__lines = []
        self.__ftp.retrlines("RETR "+self.__SUMMARY_PATH,self.__write_)
        self._log_("Crawling assembly summary...")
        for text in self.__lines:
            if text and text[0] != "#":
                parts = text.split("\t")
                if len(parts) < 16:
                    continue
                sParts = parts[7].split()
                sParts = [sParts[0]," ".join(sParts[1:])]
                if species and not species in sParts[0]+" "+sParts[1]:
                    continue
                if parts[6] in self.__safeSTIDs and parts[4] in self.__VALID_CATS:
                    (hasGff,hasGtf) = self.__hasGffGtf_(parts[-3])
                    if not hasGff and not hasGtf:
                        continue
                    fasta = parts[-3]
                    gff = ""
                    gtf = ""
                    if hasGff:
                        gff = fasta + fasta[fasta.rfind("/"):] + self.__GFF_EXTENSION
                    if hasGtf:
                        gtf = fasta + fasta[fasta.rfind("/"):] + self.__GTF_EXTENSION
                    fasta = fasta + fasta[fasta.rfind("/"):] + self.__FASTA_EXTENSION
                    introName = sParts[1].split()
                    if len(introName) > 1:
                        introName = " ".join(introName[1:])
                    else:
                        introName = ""
                    self._addEntry_(
                        sParts[0]
                        ,sParts[1].split()[0]
                        ,introName
                        ,parts[15]
                        ,parts[6]
                        ,"ncbi"
                        ,{"fasta": fasta, "gff": gff, "gtf": gtf}
                    )


    def name(
        self
        ):
        """
        Implements the pynome.interfaces.AbstractCrawler interface.

        Returns
        -------
        ret0 : object
               See interface docs.
        """
        return "ncbi"


    def __hasGffGtf_(
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
        ret1 : bool
               True if the given remote FTP URL has a GTF file within it or
               false otherwise.
        """
        (gff,gtf) = (False,False)
        dirPath = url[6+len(self.__FTP_HOST):]
        try:
            listing = self.__ftp.nlst(dirPath)
            for path in listing:
                if path.endswith(self.__GFF_EXTENSION):
                    gff = True
                if path.endswith(self.__GTF_EXTENSION):
                    gtf = True
        except:
            self._log_("Failed crawling directory '"+dirPath+"'")
        return (gff,gtf)


    def __loadTaxonomy_(
        self
        ):
        """
        Synchronizes the remote taxonomy dump with the local one and then loads
        all acceptable taxonomy IDs into this crawler. Acceptable IDs are ones
        that match a given list of division IDs.
        """
        tarPath = os.path.join(self._dataDir_(),self.__TAX_NAME)
        self._log_("Syncing taxonomy ...")
        if utility.rSync(self.__FTP_HOST+self.__TAX_DIR+self.__TAX_NAME,tarPath):
            cmd = ["tar","-xvf",tarPath,"-C",self._dataDir_()]
            assert(subprocess.run(cmd,capture_output=True).returncode==0)
        self._log_("Loading taxonomy ...")
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
