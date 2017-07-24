"""
================
Ensembl Database
================
:Author: Tyler Biggs <tyler.biggs@wsu.edu>
:Date: July 2017

.. NOTE:: Under construction.



The ensembl database module. A child class of the genome database class,
this module cotains all code directly related to connecting and parsing data
from the ensembl geneome database."""

__docformat__ = 'reStructuredText'

# Import standard modules
import itertools
from ftplib import FTP
import logging
import logging.config
# Imports from internal modules
from .genomedatabase import GenomeDatabase, GenomeEntry # import superclass

ensebml_ftp_uri = 'ftp.ensemblgenomes.org'

# TODO: Add a method to locally store genome information so that it does
#       not have to be re-downloaded or re-scraped with every run.


class EnsemblDatabase(GenomeDatabase):
    """The EnsemblDatabase class. This handles finding and downloading
    genomes from the ensembl genome database. The database url is:

        ``ftp.ensemblgenomes.org``
    
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

    def crawl_dir(self, top_dir, parsing_function):
        """Recursively crawl a target directory. Takes as an input a
        target directory and a parsing function. The ftplib.FTP.dir()
        function is used to retrieve a directory listing, line by line,
        in string format. These are appended to a newly generated list.
        Each item in this list is subject to the parsing function.

        - **parameters**::

            :param target_dir: The directory from which contents 
                               will be retrieved.

            :param parsing_function: The function to parse each result.
                Right now, this should call this function itself."""
        # TODO: Investigate how to turn this into a yield based function.
        retrived_dir_list = []  # empty list to hold the callback
        self.ftp.dir(top_dir, retrived_dir_list.append)
        print(retrived_dir_list, top_dir)
        for line in retrived_dir_list:
            if self.dir_check(line):
                # Then the line is a directory and should be crawled.
                target_dir = ''.join((top_dir, line.split()[-1] ))
                print('crawling new dir: {}'.format(target_dir))
                self.crawl_dir(target_dir, parsing_function)
            else:  # otherwise the line must be parsed.
                parsing_function(line)
        return
    """
    -----------
    FILE NAMES
    ------------
    The files are consistently named following this pattern:
    <species>.<assembly>.<sequence type>.<id type>.<id>.fa.gz

    <species>:   The systematic name of the species.
    <assembly>:  The assembly build name.
    <sequence type>:
    * 'dna' - unmasked genomic DNA sequences.
    * 'dna_rm' - masked genomic DNA.  Interspersed repeats and low
        complexity regions are detected with the RepeatMasker tool and masked
        by replacing repeats with 'N's.
    * 'dna_sm' - soft-masked genomic DNA. All repeats and low complexity regions
        have been replaced with lowercased versions of their nucleic base
    <id type> One of the following:
    * 'chromosome'     - The top-level coordinate system in most species in Ensembl
    * 'nonchromosomal' - Contains DNA that has not been assigned a chromosome
    * 'seqlevel'       - This is usually sequence scaffolds, chunks or clones.
        -- 'scaffold'   - Larger sequence contigs from the assembly of shorter
            sequencing reads (often from whole genome shotgun, WGS) which could
            not yet be assembled into chromosomes. Often more genome sequencing
            is needed to narrow gaps and establish a tiling path.
        -- 'chunk' -  While contig sequences can be assembled into large entities,
            they sometimes have to be artificially broken down into smaller entities
            called 'chunks'. This is due to limitations in the annotation
            pipeline and the finite record size imposed by MySQL which stores the
            sequence and annotation information.
        -- 'clone' - In general this is the smallest sequence entity.  It is often
            identical to the sequence of one BAC clone, or sequence region
            of one BAC clone which forms the tiling path.
    <id>:     The actual sequence identifier. Depending on the <id type> the <id>
            could represent the name of a chromosome, a scaffold, a contig, a clone ..
            Field is empty for seqlevel files
    """
    def ensemblLineParser(self, line):
        """This function parses one 'line' at a time retrieved from an ``ftp.dir()``
        command. An example of one such line:

            ``"drwxr-sr-x  2 ftp   ftp    4096 Jan 13  2015 filename"``

        This line is split by whitespace. For future reference, the indexes
        correspond (usually) to:

            + ``[0]:    the directory information.``
            + ``[1]:    the number of items therein?``
            + ``[2]:    unknown always 'ftp'``
            + ``[3]:    unknown always 'ftp'``
            + ``[4]:    the filesize in bytes, 4096 is one block, often a folder``
            + ``[5]:    Month``
            + ``[6]:    Day``
            + ``[7]:    Year``
            + ``[8]:    filename``
        
        Returns a dictionary of keywords?"""
        item = line.split()   # Split the listing by whitespace.
        line_dict = {
            'dir_info' :       item[0],
            'dir_subfolders' : item[1],
            'size' :           item[4],
            'item_name' :      item[-1]
        }
        # version_separator = '.{}'.format(self._release_number)

        parsed_name = item[-1]

        bad_words = ('chromosome', '.abinitio.')
        data_types = ('dna.toplevel.fa.gz', 'gff3.gz')

        if any( bw in parsed_name for bw in bad_words):
            return

        elif parsed_name.endswith('dna.toplevel.fa.gz'):
            add_genome(self, parsed_name,  # TODO: Rename this function? An override?
                       fasta_size=line_dict['size'],
                       fasta_uri=line_dict[])
            return

        elif parsed_name.endswith('gff3.gz'):
            add_genome(self, parsed_name,  # TODO: Rename this function? An override?
                       gff3_size=line_dict['size'],
                       gff3_uri=line_dict[])
            return

    def genome_check(self, item):
        """Checks if the incoming item, which is a single word (string),
         is a 'genome' (the type of desired data) in that it must:

            + end with fa.gz or gff3.gz
            + not have 'chromosome' in the name
            + must not have 'abinitio' in the name
        
        """
        bad_words = ('chromosome', '.abinitio.')  # These tuples could be factored out.
        data_types = ('dna.toplevel.fa.gz', 'gff3.gz')  # TODO: Fix this for the fasta finder!
        # .dna.toplevel.fa.gz
        self.logger.debug('GENOME CHECKING: {}'.format(item))
        if item.endswith(data_types) and not any(word in bad_words for word in item):
            return True
        else:
            return False

    def add_genome(self, item,  # TODO: Rename this function? An override?
                   fasta_size=None,
                   gff3_size=None,
                   fasta_uri=None,
                   gff3_uri=None):
        """Creates a new genome."""
        # species, assembly = self.parse_species_filename(item)
        genome_entry_args = {
            'genome_fasta_uri' : fasta_uri,
            'fasta_size'       : fasta_size,
            'genome_gff3_uri'  : gff3_uri,
            'gff3_size'        : gff3_size,
            'download_method'  : 'ftp ensemble'
            }
        # I don't want any values with None to pass through.
        g_args = {k : v for k, v in genome_entry_args.items() if v}
        print(g_args)
        print('Adding a new genome: {}'.format(item))
        self.save_genome(item, **g_args)

    def dir_check(self, dir_value):
        """Checks if the input: dir_value is a directory. Assumes the input 
        will be in the following format:

             ``"drwxr-sr-x  2 ftp   ftp    4096 Jan 13  2015 filename"``

        This works by checking the first letter of the input string,
        and returns True for a directory or False otherwise."""
        print(dir_value[0][0])
        if dir_value[0][0] == 'd':
            print("New Dir found")
            return True
        else:
            return False

    def _generate_uri(self):
        """Generates the uri strings needed to download the genomes
        from the ensembl database.

        .. todo:: This should take some input to generate the strings.
                  Rather than call upon the self instance variables.

        **Returns**: List of Strings of URIs for the ensembl database. eg::

            pub/fungi/release-36/gff3/
            pub/metazoa/release-36/gff3/
            ...
        """
        ensembl_data_types = ['gff3', 'fasta']
        ensembl_kingdoms = ['fungi', 'metazoa', 'plants', 'protists']
        # Unique permutations of data types and kingdoms.
        uri_gen = itertools.product(ensembl_data_types, ensembl_kingdoms)
        # For each iteration, return the desired URI.
        for item in uri_gen:
            yield '/'.join(('pub', item[1],  # the clade or kingdom
                            self._release_version,
                            item[0], '', ))  # the data type

    def _find_genomes(self,
                      parsingFunction,
                      baseURIList):
        """Private function that handles finding the list of genomes."""
        self.ftp.connect(ensebml_ftp_uri)  # connect to the ensemble ftp
        self.ftp.login()
        for uri in baseURIList:
            print("Going to start a new clade crawl with: {}".format(uri))
            self.crawl_dir(uri, parsingFunction)
        self.ftp.quit()  # close the ftp connection
        return

    def find_genomes(self):
        """OVERWRITES GENOMEDATABASE FUNCTION. Calls the _find_genomes() private
        function."""
        print("Finding Genomes. This takes approximately 45 minutes...")
        ensembleBaseURIs = [uri for uri in self._generate_uri()]
        self._find_genomes(
            parsingFunction=self.ensemblLineParser,
            baseURIList=ensembleBaseURIs,
        )
        return

    @property
    def release_version(self):
        """Release version property. Should be in the form:
            ``"release-#", "release-36"``"""
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
        self._download_genomes()
        return

    def _download_genomes(self):
        """The internal download function, specific to ensembledatabase."""
        # Find all entries in the sql database with both fasta and gff3 files.
        genome_entries = self.get_mutual_genomes()
        # Return a list of those uri values.
        pass

    def get_mutual_genomes(self):
        """Gets the genome entries that have both a fasta and gff3 uri."""
        # Get the values with both fasta and gff3 uris.
        mutual = session.query(GenomeEntry).filter(
            GenomeEntry.genome_fasta_uri,
            GenomeEntry.genome_gff3_uri).scalar() is not None
        return mutual