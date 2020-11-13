"""
Contains the Ensembl class.
"""
from . import core
import ftplib
from . import interfaces
import socket








class Ensembl(interfaces.AbstractCrawler):
    """
    This is the ensembl class. It implements the abstract crawler interface. The
    remote database is crawled directly through its ftp server to find all valid
    entries. All information can be found within those directories except for
    the taxonomy ID. The taxonomy ID is found in a special text file located in
    the root public folder.
    """
    __CDNA_EXTENSION = ".cdna.all.fa.gz"
    _FTP_FASTA_DIR = "/fasta"
    _FTP_GFF_DIR = "/gff3"
    _FTP_HOST = "ftp.ensembl.org"
    _FTP_RELEASE_BASENAME = "release-"
    _FTP_ROOT_DIR = "/pub"
    _TAXONOMY_FILE = "/species_EnsemblVertebrates.txt"
    __FASTA_EXTENSION = ".dna.toplevel.fa.gz"
    __FTP_IGNORED_DIRS = ["cds","dna_index","ncrna","pep"]
    __GFF_EXTENSION = ".gff3.gz"


    def __init__(
        self
        ):
        """
        Initializes a new ensembl crawler.
        """
        super().__init__()
        self.__ftp = None
        self.__text = ""
        self.__taxIds = {}


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
        self._connect_()
        releaseVersion = self._latestRelease_()
        if releaseVersion:
            self._log_("Loading taxonomy ...")
            self._getTaxonomyIds_(
                self._FTP_ROOT_DIR
                + "/"
                + self._FTP_RELEASE_BASENAME
                + str(releaseVersion)
            )
            self._log_("Crawling FASTA ...")
            (fasta,cdna) = self._crawlFasta_(
                self._FTP_ROOT_DIR
                + "/"
                + self._FTP_RELEASE_BASENAME
                + str(releaseVersion)
                + self._FTP_FASTA_DIR
                ,species
            )
            self._log_("Crawling GFF ...")
            gff = self._crawlGff_(
                self._FTP_ROOT_DIR
                + "/"
                + self._FTP_RELEASE_BASENAME
                + str(releaseVersion)
                + self._FTP_GFF_DIR
                ,species
                ,releaseVersion
            )
            self._mergeResults_(fasta,cdna,gff)


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
        return "ensembl"


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
        DEPRECATED_COMMENT

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
        fasta = {}
        cdna = {}
        try:
            listing = [x.split("/").pop() for x in self.__ftp.nlst(directory)]
        except ftplib.all_errors:
            self._connect_()
            return self._crawlFasta_(directory,species,depth)
        except socket.timeout:
            self._connect_()
            return self._crawlFasta_(directory,species,depth)
        for file_ in listing:
            if (
                ( not depth and not file_.endswith("_collection") )
                or ( depth == 1 and directory.endswith("_collection") )
            ):
                if species:
                    names = file_.split("_")
                    fullName = names[0].lower()+" "+names[1].lower()
                    if not species.lower() in fullName:
                        continue
            if file_.endswith(self.__FASTA_EXTENSION):
                fasta[file_[:-len(self.__FASTA_EXTENSION)]] = directory+"/"+file_
            elif file_.endswith(self.__CDNA_EXTENSION):
                cdna[file_[:-len(self.__CDNA_EXTENSION)]] = directory+"/"+file_
            elif "." not in file_ and file_ not in self.__FTP_IGNORED_DIRS:
                (f,c) = self._crawlFasta_(directory+"/"+file_,species,depth+1)
                fasta.update(f)
                cdna.update(c)
        return (fasta,cdna)


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
            if (
                ( not depth and not file_.endswith("_collection") )
                or ( depth == 1 and directory.endswith("_collection") )
            ):
                if species:
                    names = file_.split("_")
                    fullName = names[0].lower()+" "+names[1].lower()
                    if not species.lower() in fullName:
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
        ,cdna
        ,gff
        ):
        """
        Merges the given FASTA and GFF3 dictionaries of found possible entries,
        adding an entry to this crawler for any key that both dictionaries
        contain. DEPRECATED_COMMENT

        Parameters
        ----------
        fasta : dictionary
                The FASTA lookup dictionary generated by this crawler's crawl
                FASTA method.
        cdna : object
               Detailed description.
        gff : dictionary
              The GFF lookup dictionary generated by this crawler's crawl GFF
              method.
        """
        for key in fasta:
            if key in cdna and key in gff:
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
                        ,"ensembl"
                        ,{
                            "fasta": "ftp://"+self._FTP_HOST+fasta[key]
                            ,"cdna": "ftp://"+self._FTP_HOST+cdna[key]
                            ,"gff": "ftp://"+self._FTP_HOST+gff[key]
                        }
                    )


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
