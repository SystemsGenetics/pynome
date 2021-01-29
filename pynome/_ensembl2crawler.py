"""
Contains the Ensembl2Crawler class.
"""
from ._ensemblcrawler import EnsemblCrawler








class Ensembl2Crawler(EnsemblCrawler):
    """
    This is the ensembl2 crawler class. It implements the abstract crawler
    interface, inheriting from the original ensembl class because ensembl splits
    its assemblies between two FTP sites.
    """
    _FTP_HOST = "ftp.ensemblgenomes.org"
    _TAXONOMY_FILE = "/species.txt"


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
            fasta = {}
            cdna = {}
            gff = {}
            for sDirName in ("fungi","metazoa","plants","protists"):
                self._log_("Crawling "+sDirName+" FASTA ...")
                (f,c) = self._crawlFasta_(
                    self._FTP_ROOT_DIR
                    + "/"
                    + self._FTP_RELEASE_BASENAME
                    + str(releaseVersion)
                    + "/"
                    + sDirName
                    + self._FTP_FASTA_DIR
                    ,species
                )
                self._log_("Crawling "+sDirName+" GFF ...")
                g = self._crawlGff_(
                    self._FTP_ROOT_DIR
                    + "/"
                    + self._FTP_RELEASE_BASENAME
                    + str(releaseVersion)
                    + "/"
                    + sDirName
                    + self._FTP_GFF_DIR
                    ,species
                    ,releaseVersion
                )
                fasta.update(f)
                cdna.update(c)
                gff.update(g)
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
        return "ensembl2"
