"""The ensembl database module. A child class of the genome database class,
this module cotains all code directly related to connecting and parsing data
from the ensembl geneome database."""

# Import standard modules
import itertools
from ftplib import FTP
import logging
import logging.config
# Imports from internal modules
from .genomedatabase import GenomeDatabase, GenomeEntry # import superclass
# from .genome import Genome

ensebml_ftp_uri = 'ftp.ensemblgenomes.org'

# TODO: Add a method to locally store genome information so that it does
#       not have to be re-downloaded or re-scraped with every run.
# TODO: Redo some docstrings, add todos. There have been some refactors.


class EnsemblDatabase(GenomeDatabase):
    """The EnsemblDatabase class. This handles finding and downloading
    genomes from the ensembl genome database. The database url is:

        `ftp.ensemblgenomes.org`
    
    It does so by recursively walking the ftp directory. It only collects
    those genomes that have a ``*.gff3.gz`` or a ``*.fa.gz`` file.

    - **parameters**::

        :param release_version: The release version specific to ensemble.
                                This should be a number between 1 and 36.

    
    :Example:

    Instructions on how to use this script.

        >>> database = EnsemblDatabase()  # Initialize a database.

    # TODO: Add an example -- This will link to the sqlite server.
    
    .. seealso:: :class:`GenomeDatabase`
    """

    def __init__(self, release_version=36):
        super(EnsemblDatabase, self).__init__()  # Call parent class init
        self._release_number = None  # set by the release version setter
        self.release_version = release_version
        self._ftp_genomes = []
        self.ftp = FTP()  # the ftp instance for the database
        logging.config.fileConfig('pynome/pynomeLog.conf')
        self.logger = logging.getLogger('pynomeLog')
        # Set up the logger, and note the class initialization.

    # TODO: Change to a yield-based function?
    def _crawl_directory(self, target_dir, parsing_function):
        """Recursively crawl a target directory. Takes as an input a
        target directory and a parsing function. The ftplib.FTP.dir()
        function is used to retrieve a directory listing, line by line,
        in string format. These are appended to a newly generated list.
        Each item in this list is subject to the parsing function.

        - **parameters**::

            :param target_dir: The directory from which contents 
                               will be retrieved.

            :param parsing_function: The function to parse each result.
                Right now, this should call this function itself.

        .. todo:: Refactor so that this function takes a parsing function as
                  an argument. In doing this, an recursive ftp class will
                  likely be factored out.
        
        """
        retrived_dir_list = []  # empty list to hold the callback
        # Get the directory listing for the target directory,
        # and append it to the holder list.
        self.ftp.dir(target_dir, retrived_dir_list.append)
        # Parse this list:
        # TODO: Consider the use of yield here. ie:
        #       for item in list:
        #           yield parsing_function(item)
        for item in retrived_dir_list:  # For each line retrieved.
            parsing_function(target_dir, item, parsing_function)
            # TODO: The parsing function should probably yield calls of this 
        return

    def _ensembl_dir_parser(self, base_dir, item, parsing_function):
        """This function parses one 'line' at a time retrieved from an ftp.dir()
        command. An example of one such line:

            `drwxr-sr-x  2 ftp   ftp    4096 Jan 13  2015 filename`        

            + `[0]`:    the directory information.
            + `[1]`:    the number of items therein?
            + `[2]`:    unknown always 'ftp'
            + `[3]`:    unknown always 'ftp'
            + `[4]`:    the filesize in bytes, 4096 is one block, often a folder
            + `[5]`:    Month
            + `[6]`:    Day
            + `[7]`:    Year
            + `[8]`:    filename

        If it finds this entry to be a desired genome, by running self.genome_check(),
        it checks to see if it is a fasta, or gff3, then submits the newly created
        Genome instance to be appended to the database list.
        """
        item = item.split()   # Split the listing by whitespace.
        dir_info = item[0]    # Get the string with dir and read/write permissions.
        dir_items = item[1]   # Get the number of items within this dir.
        size = item[4]        # Get the size in Bytes of this item.
        item_name = item[-1]  # Because this should always be the last item.
        
        if self._dir_check(item):  # Then item is a directory.
            new_target_dir = ''.join((base_dir, item_name))
            self.logger.info("\nFound a new directory:\
                \n\t{}\ncrawling it.".format(new_target_dir))
            self._crawl_directory(new_target_dir, parsing_function)
            return

        elif self.genome_check(item_name):  # a genome, must be added.            
            self.logger.info('checking if this is a fasta or gff3: {}'\
                .format(item_name))

            if item_name.endswith('fa.gz'):
                fasta_uri = ''.join((base_dir, item_name))  # set the fa.gz url
                fasta_size = size
                gff3_uri, gff3_size = None, None


            elif item_name.endswith('gff3.gz'):
                gff3_uri = ''.join((base_dir, item_name))  # set the gff3.gz url
                gff3_size = size
                fasta_uri, fasta_size = None, None

            else:  # not a fasta or a gff3! we fucked up!
                # TODO: Raise an error here.
                pass

            self.add_genome(item=item_name,
                            fasta_uri=fasta_uri, 
                            fasta_size=fasta_size,
                            gff3_uri=gff3_uri,
                            gff3_size=gff3_size)

        else:
            pass  # Throw an error? I don't think this should occur.

    def add_genome(self, item, 
                   fasta_size=None,
                   gff3_size=None,
                   fasta_uri=None,
                   gff3_uri=None):
        """Creates a new genome."""

        species, assembly = self._parse_species_filename(item)

        genome_entry_args = {
            'genome_fasta_uri' : fasta_uri,
            'fasta_size'       : fasta_size,
            'genome_gff3_uri'  : gff3_uri,
            'gff3_size'        : gff3_size,
            'download_method'  : 'ftp ensemble'
            }
        # I don't want any values with None to pass through.
        g_args = {k : v for k, v in genome_entry_args.items() if v}
        self.save_genome(item, **g_args)

    def genome_check(self, item):
        """Checks if the incoming item, which is a single word (string),
         is a 'genome' (the type of desired data) in that it must:

            + end with fa.gz or gff3.gz
            + not have 'chromosome' in the name
            + must not have 'abinitio' in the name
        
        """
        bad_words = ('chromosome', 'abinitio')  # These tuples could be factored out.
        data_types = ('fa.gz', 'gff3.gz')
        self.logger.debug('GENOME CHECKING: {}'.format(item))
        if item.endswith(data_types) and \
            not any(word in bad_words for word in item):
            return True
        else:
            return False

    def _crawl_ftp(self):
        """
        Handler function to crawl the ftp server to find genome files.
        This is an internal function. It creates and connects to the ftp
        instance, generates the uris to be parsed, then initializes the 
        recursive crawler.
        """
        base_uri_list = self._generate_uri()  # Create the generator of uris.
        # ftp = FTP()  # Create the ftp class isntance
        self.ftp.connect(ensebml_ftp_uri)  # connect to the ensemble ftp
        self.ftp.login()  # login with anonomys and no password
        # iterate through those uri generated
        for uri in base_uri_list:
            # Get the directories in the base URI
            print("Going to start a new clade crawl with: {}".format(uri))
            self._crawl_directory(uri, self._ensembl_dir_parser)
        self.ftp.quit()  # close the ftp connection

    def _dir_check(self, dir_value):
        """
        Checks if the input: dir_value is a directory. Assumes the input 
        will be in the following format:

             'drwxr-sr-x'

        This works by checking the first letter of the input string,
        and returns True or False.
        """
        if dir_value[0][0] == 'd':  # Kind of a strange syntax? [0] may work?
            return True
        else:
            return False

    def _generate_uri(self):
        """
        Generates the uri strings needed to download the genomes
        from the ensembl database.
        # TODO: This should take some input to generate the strings.
                Rather than call upon the self instance variables.

        **Returns**: List of Strings of URIs for the ensembl database. eg:

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
        """This function parses a species file name, to store it in the desired
        format. Values are input in the following format.

            <species>.<assembly>.<_version>.gff3.gz
            

        """
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
        print("Finding Genomes. This takes approximately 45 minutes...")
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
