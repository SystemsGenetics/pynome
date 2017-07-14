# Import standard modules
import itertools
from ftplib import FTP
# Imports from internal modules
from .genomedatabase import GenomeDatabase  # import superclass

ensebml_ftp_uri = 'ftp.ensemblgenomes.org'


class EnsemblDatabase(GenomeDatabase):
    """
    @brief          Ensambl Genome Database class.
    """

    def __init__(self, release_version=36):
        super(EnsemblDatabase, self).__init__()  # Call parent class init
        self._release_number = None
        self.release_version = release_version
        self._ftp_genomes = []

    def _crawl_ftp(self):
        """
        recursive function to crawl the ftp server to find genome files.
        call _ftp.sendcmd function to get the current URL
        add each file in the current directory to the _ftp_LIST dictionary
        if a new directory is found then recurse _crawlFTP()
        """
        def _crawl_directory(target_dir):

            retrived_dir_list = []  # empty list to hold the callback
            # Get the directory listing for the target directory, and return it
            ftp.dir(target_dir, retrived_dir_list.append)
            # Parse this list
            
            parsed_dirs = self._parse_listings(retrived_dir_list)
            return directories, found_genomes

        base_uri_list = self._generate_uri()  # Create the generator of uris.

        ftp = FTP()  # Create the ftp class isntance
        ftp.connect(ensebml_ftp_uri)  # connect to the ensemble ftp
        ftp.login()  # login with anonomys and no password

        # iterate through those uri generated
        for uri in base_uri_list:
            # Get the directories in the base URI
            retrieved_directories = _crawl_directory(uri)

        ftp.quit()  # close the ftp connection


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
        # __ensembl_ftp_uri = 'ftp.ensemblgenomes.org'

        # Unique permutations of data types and kingdoms.
        uri_gen = itertools.product(__ensembl_data_types, __ensembl_kingdoms)

        # For each iteration, return the desired URI.
        for item in uri_gen:
            yield '/'.join(('pub',
                            item[1],  # the clade or kingdom
                            self._release_version,
                            item[0],  # the data type
                            '', ))

    def _parse_listings(self, dir_list):
        # TODO: Refactor this function into two functions? (parse, interpret)
        """
                @breif      Parses the list of files from the ftplib.FTP.dir()
                            command. Output from this command comes in the form:

                                'drwxr-sr-x    2 ftp   ftp    4096 Jan 13  2015 EB'

                @returns    binary directory: True or False
        """
        for dir_entry in dir_list:
            # Check if the entry is a directory or not
            entry_list = dir_entry.split()  # split by whitespace into a list
            # Check the first letter of the first word
            if entry_list[0][0] == 'd':  # then this is a directry
                diectory_bool = True
            else:  # otherwise check the file

            # Get the species and assembly
            # self._parse_species_filename(dir_entry)

        return

    def _parse_species_filename(self, file_name):
        """<species>.<assembly>.<_version>.gff3.gz"""
        # TODO: Generate docstring for parse_species_filename.

        # Create a separator based of the release number.
        version_separator = '.{}'.format(self._release_number)
        # Split by this separator to get the species and assembly number.
        species_assembly_list = file_name.split(version_separator)
        # The first item in the list is the species and assembly.
        species, assembly = species_assembly_list[0].split('.', 1)
        return (species, assembly)

    def _find_genomes(self):
        """
        Private function that handles finding the list of genomes.
        """
        # Start the ftp crawler
        self._crawl_ftp()
        return

    def find_genomes(self):
        """OVERWRITES GENOMEDATABASE FUNCTION. Calls the _find_genomes() private
        function."""
        self._find_genomes()
        return

    @property
    def release_version(self):
        """Release version property. Should be in the form:
            "release-#", "release-36"
        """
        return self._release_version

    @release_version.setter
    def release_version(self, value):
        """Setter for the release_version. Accepts an input integer and returns
        a string in the form: 'release-##' """
        # TODO: Add validation to ensure that the input value is an integer.
        #       Perhaps it should also be limited to the range of available
        #       release verions on the ensembl site. (1 through 36)
        self._release_number = value
        self._release_version = 'release-' + str(value)

    def download_genomes(self):
        """Downloads the genomes in the database that have both fasta and gff3 files."""
        pass
