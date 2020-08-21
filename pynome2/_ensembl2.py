"""
Contains the Ensembl2 class.
"""
from . import core
from ._ensembl import Ensembl








class Ensembl2(Ensembl):
    """
    This is the ensembl2 class. It implements the abstract crawler interface,
    inheriting from the original ensembl class because ensembl splits its
    assemblies between two FTP sites.
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
        super().__init__()


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
            core.log.send("Loading Ensembl2 taxonomy ...")
            self._getTaxonomyIds_(
                self._FTP_ROOT_DIR
                + "/"
                + self._FTP_RELEASE_BASENAME
                + str(releaseVersion)
            )
            fasta = {}
            gff = {}
            for sDirName in ("fungi","metazoa","plants","protists"):
                core.log.send("Crawling Ensembl2 "+sDirName+" FASTA ...")
                f = self._crawlFasta_(
                    self._FTP_ROOT_DIR
                    + "/"
                    + self._FTP_RELEASE_BASENAME
                    + str(releaseVersion)
                    + "/"
                    + sDirName
                    + "/"
                    + self._FTP_FASTA_DIR
                    ,species
                )
                core.log.send("Crawling Ensembl2 "+sDirName+" GFF ...")
                g = self._crawlGff_(
                    self._FTP_ROOT_DIR
                    + "/"
                    + self._FTP_RELEASE_BASENAME
                    + str(releaseVersion)
                    + "/"
                    + sDirName
                    + "/"
                    + self._FTP_GFF_DIR
                    ,species
                    ,releaseVersion
                )
                fasta.update(f)
                gff.update(g)
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
        return "ensembl2"


    #########################
    # PROTECTED - Constants #
    #########################


    #
    # The URL of the FTP server.
    #
    _FTP_HOST = "ftp.ensemblgenomes.org"


    #
    # The file name of the special text file that contains all taxonomy IDs on
    # the FTP server in a release folder.
    #
    _TAXONOMY_FILE = "/species.txt"
