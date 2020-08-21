"""
Contains the Ensembl class.
"""
import ftplib
import socket
from . import abstract
from . import core








class Ensembl(abstract.AbstractCrawler):
    """
    This is the ensembl class. It implements the abstract crawler interface. The
    remote database is crawled directly through its ftp server to find all valid
    entries. All information can be found within those directories except for
    the taxonomy ID. The taxonomy ID is found in a special text file located in
    the root public folder.
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
        self.__text = ""
        self.__taxIds = {}


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
        self._connect_()
        releaseVersion = self._latestRelease_()
        if releaseVersion:
            core.log.send("Loading Ensembl taxonomy ...")
            self._getTaxonomyIds_(
                self._FTP_ROOT_DIR
                + "/"
                + self._FTP_RELEASE_BASENAME
                + str(releaseVersion)
            )
            core.log.send("Crawling Ensembl FASTA ...")
            fasta = self._crawlFasta_(
                self._FTP_ROOT_DIR
                + "/"
                + self._FTP_RELEASE_BASENAME
                + str(releaseVersion)
                + self._FTP_FASTA_DIR
                ,species
            )
            core.log.send("Crawling Ensembl GFF ...")
            gff = self._crawlGff_(
                self._FTP_ROOT_DIR
                + "/"
                + self._FTP_RELEASE_BASENAME
                + str(releaseVersion)
                + self._FTP_GFF_DIR
                ,species
                ,releaseVersion
            )
            self._mergeResults_(fasta,gff)


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
        return "ensembl"


    #########################
    # PROTECTED - Constants #
    #########################


    #
    # The directory on the ensembl FTP server where FASTA data is stored.
    #
    _FTP_FASTA_DIR = "/fasta"


    #
    # The directory on the ensembl FTP server where GFF data is stored.
    #
    _FTP_GFF_DIR = "/gff3"


    #
    # The URL of the FTP server.
    #
    _FTP_HOST = "ftp.ensembl.org"


    #
    # The beginning of the directory name used for releases of data on the
    # ensembl FTP server.
    #
    _FTP_RELEASE_BASENAME = "release-"


    #
    # The root public directory for the FTP server.
    #
    _FTP_ROOT_DIR = "/pub"


    #
    # The file name of the special text file that contains all taxonomy IDs on
    # the FTP server in a release folder.
    #
    _TAXONOMY_FILE = "/species_EnsemblVertebrates.txt"


    #######################
    # PROTECTED - Methods #
    #######################


    def _connect_(
        self
        ):
        """
        Connects this crawler to the ensembl FTP server, continuously retrying a
        connection until one is made successfully.
        """
        while True:
            try:
                self.__ftp = ftplib.FTP(self._FTP_HOST,timeout=10)
                self.__ftp.login()
            except ftplib.all_errors:
                pass
            else:
                break


    def _crawlFasta_(
        self
        ,directory
        ,species
        ,depth=0
        ):
        """
        Recursively crawls the given directory, calling this method on any
        subdirectories found. If the FTP connection is lost this crawler's
        connect method is called to reconnect and continue without interruption.

        Parameters
        ----------
        directory : string
                    The directory path that is recursively crawled for valid
                    FASTA files.
        species : string
                  The name of the species that is crawled, ignoring any other
                  species found on the remote server. If this string is blank
                  then all species are crawled.
        depth : int
                The current subdirectory depth of this recursive scan. Used to
                print output about progress for only the top level call of this
                method.

        Returns
        -------
        ret0 : dictionary
               A lookup table of found valid FASTA files for potential entries
               where the keys are the file name excluding its FASTA extension
               and the values are the full path to the file.
        """
        ret = {}
        try:
            listing = [x.split("/").pop() for x in self.__ftp.nlst(directory)]
        except ftplib.all_errors:
            self._connect_()
            return self._crawlFasta_(directory,species,depth)
        except socket.timeout:
            self._connect_()
            return self._crawlFasta_(directory,species,depth)
        for file_ in listing:
            if not depth:
                if species and species.lower() != file_.split("_")[1].lower():
                    continue
            if file_.endswith(self.__FASTA_EXTENSION):
                ret[file_[:-len(self.__FASTA_EXTENSION)]] = directory+"/"+file_
            elif "." not in file_ and file_ not in self.__FTP_IGNORED_DIRS:
                ret.update(self._crawlFasta_(directory+"/"+file_,species,depth+1))
        return ret


    def _crawlGff_(
        self
        ,directory
        ,species
        ,version
        ,depth=0
        ):
        """
        Recursively crawls the given directory, calling this method on any
        subdirectories found. If the FTP connection is lost this crawler's
        connect method is called to reconnect and continue without interruption.

        Parameters
        ----------
        directory : string
                    The directory path that is recursively crawled for valid
                    GFF3 files.
        species : string
                  The name of the species that is crawled, ignoring any other
                  species found on the remote server. If this string is blank
                  then all species are crawled.
        version : string
                  The release number of the release directory that is being
                  scanned. This is needed for GFF3 because the release number is
                  part of its valid file name extension.
        depth : int
                The current subdirectory depth of this recursive scan. Used to
                print output about progress for only the top level call of this
                method.

        Returns
        -------
        ret0 : dictionary
               A lookup table of found valid GFF3 files for potential entries
               where the keys are the file name excluding its GFF3 extension and
               the values are the full path to the file.
        """
        ret = {}
        try:
            listing = [x.split("/").pop() for x in self.__ftp.nlst(directory)]
        except ftplib.all_errors:
            self._connect_()
            return self._crawlGff_(directory,species,version,depth)
        except socket.timeout:
            self._connect_()
            return self._crawlGff_(directory,species,version,depth)
        for file_ in listing:
            if not depth:
                if species and species.lower() != file_.split("_")[1].lower():
                    continue
            ending = "."+str(version)+self.__GFF_EXTENSION
            if file_.endswith(ending):
                ret[file_[:-len(ending)]] = directory+"/"+file_
            elif "." not in file_:
                ret.update(self._crawlGff_(directory+"/"+file_,species,version,depth+1))
        return ret


    def _getTaxonomyIds_(
        self
        ,directory
        ):
        """
        Downloads and parses the given taxonomy ID file, populating this
        crawlers lookup dictionary of taxonomy IDs.

        Parameters
        ----------
        directory : string
                    The directory on the ensembl FTP server where the special
                    taxonomy ID file is located.
        """
        self.__text = ""
        self.__taxIds = {}
        self.__ftp.retrlines("RETR "+directory+self._TAXONOMY_FILE,self.__write_)
        for line in self.__text.split("\n")[1:]:
            parts = line.split("\t")
            if len(parts)>=5:
                self.__taxIds[parts[1]] = parts[3]


    def _latestRelease_(
        self
        ):
        """
        Getter method.

        Returns
        -------
        ret0 : int
               The latest release number of all scanned release directories or 0
               if no release directories were found.
        """
        ret = 0
        listing = [x.split("/").pop() for x in self.__ftp.nlst(self._FTP_ROOT_DIR)]
        for file_ in listing:
            if file_.startswith(self._FTP_RELEASE_BASENAME):
                version = file_[len(self._FTP_RELEASE_BASENAME):]
                if version.isdigit():
                    version = int(version)
                    if version > ret:
                        ret = version
        return ret


    def _mergeResults_(
        self
        ,fasta
        ,gff
        ):
        """
        Merges the given FASTA and GFF3 dictionaries of found possible entries,
        adding an entry to this crawler for any key that both dictionaries
        contain.

        Parameters
        ----------
        fasta : dictionary
                The FASTA lookup dictionary generated by this crawler's crawl
                FASTA method.
        gff : dictionary
              The GFF lookup dictionary generated by this crawler's crawl GFF
              method.
        """
        for key in fasta:
            if key in gff:
                parts = key.split(".")
                names = parts.pop(0).split("_") + [""]
                taxKey = "_".join((n.lower() for n in names if n))
                if taxKey in self.__taxIds:
                    self._addEntry_(
                        names[0]
                        ,names[1]
                        ,names[2]
                        ,".".join(parts)
                        ,self.__taxIds[taxKey]
                        ,"ftp_gunzip"
                        ,{"fasta": self._FTP_HOST+fasta[key], "gff": self._FTP_HOST+gff[key]}
                    )


    #######################
    # PRIVATE - Constants #
    #######################


    #
    # The extension of FASTA files that should be flagged as a possible entry
    # for this crawler.
    #
    __FASTA_EXTENSION = ".dna.toplevel.fa.gz"


    #
    # A list of directory names that this crawler will ignore when crawling the
    # ensembl FTP server.
    #
    __FTP_IGNORED_DIRS = ["cdna","cds","dna_index","ncrna","pep"]


    #
    # The extension of GFF files that should be flagged as a possible entry for
    # this crawler.
    #
    __GFF_EXTENSION = ".gff3.gz"


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
        self.__text += text+"\n"
