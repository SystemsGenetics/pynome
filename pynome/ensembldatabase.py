# Import standard modules
import itertools
from ftplib import FTP
# Imports from internal modules
from .genomedatabase import GenomeDatabase  # import superclass
from .genome import Genome

ensebml_ftp_uri = 'ftp.ensemblgenomes.org'


class EnsemblDatabase(GenomeDatabase):
    """
    @brief          Ensambl Genome Database class.
    """

    def __init__(self, release_version=36):
        super(EnsemblDatabase, self).__init__()  # Call parent class init
        self._release_number = None  # set by the release version setter
        self.release_version = release_version
        self._ftp_genomes = []
        self.ftp = FTP()  # the ftp instance for the database

    def _crawl_directory(self, target_dir):
        """Recursively crawl a target directory! More to come soon!
        """
        retrived_dir_list = []  # empty list to hold the callback
        # Get the directory listing for the target directory,
        # and append it to the holder list.
        self.ftp.dir(target_dir, retrived_dir_list.append)
        # Parse this list:
        for item in retrived_dir_list:  # For each line retrieved.
            item = item.split()  # split the list by whitespace
            if self._dir_check(item) == True:  # check if it is a directory
                # Create the new target directory by joining the old
                # and the new, which is the last listed item.
                new_target_dir = ''.join((target_dir, item[-1]))
                print("Found a new directory:\n\t{}\ncrawling it.".format(new_target_dir))
                self._crawl_directory(new_target_dir)  # crawl that dir
            elif self.genome_check(item[-1]):  # that item is not a dir, and must be parsed.
                print('genome found: {}'.format(item))
                self.add_genome(item)  # if so, add a genome
                # TODO: Parse the item and find if it is a genome.
                #       if so, then create the genome, and append it
                #       and its ftp uri to the class genome list.
        return

    def add_genome(self, item):
        """Creates a new genome from a dir line list, separated by whitespace"""
        # Did we find a fasta or a gff3?
        filename = item[-1]
        print('checking if this is a fasta or gff3: {}'.format(filename))
        if filename.endswith('fa.gz'):
            print('found a new fasta!\n\t{}'.format(filename))
            # set the fa.gz url
        elif filename.endswith('gff3.gz'):
            # set the gff3.gz url
            print('found a new gff3!\n\t{}'.format(filename))
        else:  # not a fasta or a gff3! we fucked up!
            print("BAD BAD, error. Should never happen. (not really that bad?)")
            return 
        new_genome = Genome()  # create the new genome
        # get the items species and assembly:
        species, assembly = self._parse_species_filename(item[-1])
        # set the assembly version, taxonomic name and the uri we found it at
        new_genome.assembly_version = assembly
        new_genome.taxonomic_name = species
        # TODO: get the uri we found this item at.

    def genome_check(self, item):
        """Checks if the incoming item, which is a dir line item separated by
        whitespace, is a 'genome' in that it must:
            + end with fa.gz or gff3.gz
            + not have 'chromosome' in the name
            + must not have 'abinitio' in the name"""
        bad_words = ('chromosome', 'abinitio')
        # print('GENOME CHECKING: {}'.format(item))
        if item.endswith(('fa.gz', 'gff3.gz')) and \
            not any(word in bad_words for word in item):
            return True
        else:
            return False

    def _crawl_ftp(self):
        """
        recursive function to crawl the ftp server to find genome files.
        """
        base_uri_list = self._generate_uri()  # Create the generator of uris.
        # ftp = FTP()  # Create the ftp class isntance
        self.ftp.connect(ensebml_ftp_uri)  # connect to the ensemble ftp
        self.ftp.login()  # login with anonomys and no password
        # iterate through those uri generated
        for uri in base_uri_list:
            # Get the directories in the base URI
            print("Going to start a new clade crawl with: {}".format(uri))
            retrieved_directories = self._crawl_directory(uri)
        self.ftp.quit()  # close the ftp connection

    def _dir_check(self, dir_value):
        """
        @brief      Checks if the input: dir_value is a directory. Assumes
                    the input will be in the following format:
                        'drwxr-sr-x  2 ftp   ftp    4096 Jan 13  2015 filename'
                    This works by checking the first letter of the input string,
                    and returns True or False.
        """
        if dir_value[0][0] == 'd':
            return True
        else:
            return False



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
