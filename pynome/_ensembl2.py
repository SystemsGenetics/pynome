"""
Contains the Ensembl2 class.
"""
from ._ensembl import Ensembl
from . import core








class Ensembl2(Ensembl):
    """
    This is the ensembl2 class. It implements the abstract crawler interface,
    inheriting from the original ensembl class because ensembl splits its
    assemblies between two FTP sites.
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
        Implements the pynome.interfaces.AbstractCrawler interface.

        Returns
        -------
        ret0 : object
               See interface docs.
        """
        return "ensembl2"
