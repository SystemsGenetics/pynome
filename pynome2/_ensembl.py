"""
Contains the Ensembl class.
"""
import ftplib
import socket
from . import abstract
# For FASTA files: they ALWAYS end in *.toplevel.fa.gz
# Found in http://ftp.ensemblorg.ebi.ac.uk/pub/release-92/fasta/
#
# For GFF3 files: they ALWAYS end in *.92.gff3.gz
# Found in http://ftp.ensemblorg.ebi.ac.uk/pub/release-92/gff3/








class Ensembl(abstract.AbstractCrawler):
    """
    Detailed description.
    """


    #######################
    # PUBLIC - Interfaces #
    #######################


    def crawl(self, species=""):
        """
        Detailed description.

        Parameters
        ----------
        species : string
                  Detailed description.
        """
        self.__ftp = None
        self.__connect_()
        release_version = 0
        listing = [x.split("/").pop() for x in self.__ftp.nlst(self.__FTP_ROOT_DIR)]
        for file_ in listing:
            if file_.startswith(self.__FTP_RELEASE_BASENAME):
                version = file_[len(self.__FTP_RELEASE_BASENAME):]
                if version.isdigit():
                    version = int(version)
                    if version > release_version:
                        release_version = version
        if release_version:
            self.__crawlGff3_(
                (
                    self.__FTP_ROOT_DIR
                    + "/"
                    + self.__FTP_RELEASE_BASENAME
                    + str(release_version)
                    + self.__FTP_GFF3_DIR
                )
                ,release_version
            )
            self.__crawlFasta_(
                self.__FTP_ROOT_DIR
                + "/"
                + self.__FTP_RELEASE_BASENAME
                + str(release_version)
                + self.__FTP_FASTA_DIR
            )


    #####################
    # PRIVATE - Methods #
    #####################


    def __connect_(self):
        """
        Detailed description.
        """
        while True:
            try:
                self.__ftp = ftplib.FTP(self.__FTP_HOST,timeout=10)
                self.__ftp.login()
            except ftplib.all_errors:
                pass
            else:
                break


    def __crawlFasta_(self, directory, depth=0):
        """
        Detailed description.

        Parameters
        ----------
        directory : string
                    Detailed description.
        UNKNOWN
        """
        try:
            listing = [x.split("/").pop() for x in self.__ftp.nlst(directory)]
        except ftplib.all_errors:
            self.__connect_()
            self.__crawlFasta_(directory,depth)
            return
        except socket.timeout:
            self.__connect_()
            self.__crawlFasta_(directory,depth)
            return
        i = 1
        for file_ in listing:
            if not depth:
                print("\r                              ",end="")
                print("\r[Ensembl] Crawling FASTA %i/%i ..." % (i,len(listing)),end="")
            i += 1
            if file_.endswith(self.__FASTA_EXTENSION):
                pass
                #print(f"{directory}/{file_}")
            elif "." not in file_ and file_ not in self.__FTP_IGNORED_DIRS:
                self.__crawlFasta_(directory+"/"+file_,depth+1)
        if not depth:
            print("")


    def __crawlGff3_(self, directory, version, depth=0):
        """
        Detailed description.

        Parameters
        ----------
        directory : string
                    Detailed description.
        version : string
                  Detailed description.
        UNKNOWN
        """
        try:
            listing = [x.split("/").pop() for x in self.__ftp.nlst(directory)]
        except ftplib.all_errors:
            self.__connect_()
            self.__crawlGff3_(directory,version,depth)
            return
        except socket.timeout:
            self.__connect_()
            self.__crawlGff3_(directory,version,depth)
            return
        i = 1
        for file_ in listing:
            if not depth:
                print("\r                              ",end="")
                print("\r[Ensembl] Crawling GFF3 %i/%i ..." % (i,len(listing)),end="")
            i += 1
            if file_.endswith("."+str(version)+self.__GFF3_EXTENSION):
                pass
                #print(f"{directory}/{file_}")
            elif "." not in file_:
                self.__crawlGff3_(directory+"/"+file_,version,depth+1)
        if not depth:
            print("")


    ##############################
    # PRIVATE - Static Variables #
    ##############################


    #
    # Detailed description.
    #
    __FASTA_EXTENSION = ".dna.toplevel.fa.gz"


    #
    # Detailed description.
    #
    __FTP_FASTA_DIR = "/fasta"


    #
    # Detailed description.
    #
    __FTP_GFF3_DIR = "/gff3"


    #
    # Detailed description.
    #
    __FTP_HOST = "ftp.ensembl.org"


    #
    # Detailed description.
    #
    __FTP_IGNORED_DIRS = ["cdna","cds","dna_index","ncrna","pep"]


    #
    # Detailed description.
    #
    __FTP_RELEASE_BASENAME = "release-"


    #
    # Detailed description.
    #
    __FTP_ROOT_DIR = "/pub"


    #
    # Detailed description.
    #
    __GFF3_EXTENSION = ".gff3.gz"
