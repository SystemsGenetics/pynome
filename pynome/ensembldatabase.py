# Import standard modules
import itertools
import ftplib
# Imports from this module
from .genomedatabase import GenomeDatabase  # import superclass


class EnsemblDatabase(GenomeDatabase):
    """
    @brief          Ensambl Genome Database class.
    """

    def __init__(self, release_version="release-36"):
        super(EnsemblDatabase, self).__init__()  # Call parent class init
        self._release_version = release_version
        self._ftp_genomes = []

    def _crawl_ftp(self, target_directory):
        """
        recursive function to crawl the ftp server to find genome files.
        call _ftp.sendcmd function to get the current URL
        add each file in the current directory to the _ftp_LIST dictionary
        if a new directory is found then recurse _crawlFTP()
        """

        # active_directory_list = []  # create an empty list for the callback
        # ftp.cwd(target_directory)  # change to the target ftp directory
        # ftp.dir(active_directory_list.append)

        pass

    def _generate_uri(self):
        """
        @breif      Generates the uri strings needed to download the genomes
                    from the ensembl database. Dependant on the release
                    version provided.

        @returns    List of Strings of URIs for the ensembl database. eg:

                        "TODO: example uri here"
                        "TODO: format output here"
        """
        __ensembl_data_types = ['gff3', 'fasta']
        __ensembl_kingdoms = ['fungi', 'metazoa', 'plants', 'protists']
        __ensembl_ftp_uri = 'ftp.ensemblgenomes.org'

        # Unique permutations of data types and kingdoms.
        uri_gen = itertools.product(__ensembl_data_types, __ensembl_kingdoms)

        # For each iteration, return the desired URI.
        for item in uri_gen:
            yield '/'.join((__ensembl_ftp_uri,
                            'pub',
                            item[1],
                            self._release_version,
                            item[0],
                            '',
                            ))

    def _parse_listings(self, dir_list):
        # TODO: Refactor this function into two functions. (parse, interpret)
        """
                @breif      Parses the list of files from the ftplib.FTP.dir()
                            command. Output from this command comes in the form:

                                'drwxr-sr-x    2 ftp   ftp    4096 Jan 13  2015 EB'

                @returns    binary directory: True or False

                """
        pass

    def _parse_species_filename(self, file_name):
        """<species>.<assembly>.<_version>.gff3.gz"""
        
        # Split the incoming file_name string by decimal points.
        split_name = file_name.split('.')
        species = split_name[0]
        assembly = split_name[1] + '.' + split_name[2]
        version = split_name[-3]

        return (species, assembly, version)

    def _find_genomes(self):
        """
        Private function that handles finding the list of genomes.
        """
        pass

    def find_genomes(self):
        """OVERWRITES GENOMEDATABASE FUNCTION. Calls the _find_genomes() private
        function."""

        _find_genomes()
        
        return

    @property
    def release_version(self):
        """Release version property. Should be in the form:
            "release-#", "release-36"
        """
        return self._release_version

    def download_genomes(self):
        """Downloads the genomes in the database that have both fasta and gff3 files."""
        pass
