"""
Detailed description.
"""
from ftplib import FTP
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


    @abc.abstractmethod
    def crawl(self):
        """
        Detailed description.
        """
        ftp = FTP(self.__FTP_HOST)
        ftp.login()
        release_version = 0
        listing = [x.split("/").pop() for x in ftp.nlst(self.__FTP_ROOT_DIR)]
        for file_ in listing:
            if file_.startswith(self.__FTP_RELEASE_BASENAME):
                version = file_[len(self.__FTP_RELEASE_BASENAME):]
                if version.isdigit():
                    version = int(version)
                    if version > release_version:
                        release_version = version
        if release_version:
            self.crawl_fasta(
                ftp
                ,(
                    self.__FTP_ROOT_DIR
                    + "/"
                    + self.__FTP_RELEASE_BASENAME
                    + release_version
                    + self.__FTP_FASTA_DIR
                )
            )


    #####################
    # PRIVATE - Methods #
    #####################


    def crawlFasta(self, ftp, directory):
        """
        Detailed description.

        Parameters
        ----------
        ftp : ftplib.FTP
              Detailed description.
        directory : string
                    Detailed description.
        """
        listing = [x.split("/").pop() for x in ftp.nlst(directory)]
        for file_ in listing:
            if file_.endswith(self.__FASTA_EXTENSION):
                print(f"{directory}/{file_}")
            elif "." not in file_ and file_ not in self.__FTP_IGNORED_DIRS:
                crawl_fasta(ftp,directory + "/" + file_)


    ##############################
    # PRIVATE - Static Variables #
    ##############################


    #
    # Detailed description.
    #
    __FTP_HOST = "ftp.ensembl.org"


    #
    # Detailed description.
    #
    __FTP_ROOT_DIR = "/pub"


    #
    # Detailed description.
    #
    __FTP_RELEASE_BASENAME = "release-"


    #
    # Detailed description.
    #
    __FTP_FASTA_DIRS = "/fasta"


    #
    # Detailed description.
    #
    __FTP_IGNORED_DIRS = ["cdna","cds","dna_index","ncrna","pep"]


    #
    # Detailed description.
    #
    __FASTA_EXTENSION = ".dna.toplevel.fa.gz"
